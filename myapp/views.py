from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import registerForm
from .models import Course, CourseSchedule, StudentRegistration,Student
from django.contrib import messages
from django.db.models import Q
from .models import Notification

# User sign-up
def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Student instance
            Student.objects.create(user=user)
            login(request, user)
            return redirect('user_login')
        else:
            messages.error(request, "Please check your details and try again.")
    else:
        form = registerForm()
    return render(request, 'myapp/register.html', {'form': form})

# User login
def user_login(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'myapp/home.html')

def custom_logout(request):
    logout(request)
    return redirect('user_login')

@login_required 
def search(request):
    query = request.GET.get('query', '')
    student = request.user.student
    completed_courses = student.completed_courses.all() 
    if query:
        courses = Course.objects.filter(
            Q(code__icontains=query) | 
            Q(name__icontains=query) | 
            Q(instructor__icontains=query) 
        ).exclude(id__in=completed_courses.values('id'))
    else:
        courses = Course.objects.none()

    return render(request, 'myapp/search.html', {
        'courses': courses,
        'query': query
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    spots_taken = StudentRegistration.objects.filter(course=course).count()
    available_spots = course.capacity - spots_taken 
    context = {'course': course, 'available_spots': available_spots}
    return render(request, 'myapp/course_detail.html', context)

# Course schedule
def course_schedule(request, course_id):
    course = get_object_or_404(Course, pk=course_id) 
    try:
        schedule = CourseSchedule.objects.get(course=course)
    except CourseSchedule.DoesNotExist:
        messages.error(request, "No schedule available for this course.")
        return redirect('course_detail', course_id=course_id)
    
    context = {
        'course': course, 
        'schedule': schedule,
        'available_spots': course.capacity - StudentRegistration.objects.filter(course=course).count()
    }
    return render(request, 'myapp/course_schedule.html', context) 

# Register course
@login_required
def register_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    student = request.user.student

    if request.method == 'POST':
        # Check if the student has completed the prerequisites
        prerequisites = course.prerequisites.all()
        completed_courses = student.completed_courses.all()
        missing_prerequisites = [prerequisite for prerequisite in prerequisites if prerequisite not in completed_courses]

        if missing_prerequisites:
            messages.error(request, "You have not completed all the prerequisites for this course.")
            return redirect('course_detail', course_id=course_id)

        # Check for overlapping schedules
        try:
            course_schedule = CourseSchedule.objects.get(course=course)
        except CourseSchedule.DoesNotExist:
            messages.error(request, "The course schedule is not available.")
            return redirect('course_detail', course_id=course_id)

        student_registrations = StudentRegistration.objects.filter(student=student).select_related('course__courseschedule')

        for registration in student_registrations:
            registered_course_schedule = registration.course.courseschedule
            if (course_schedule.days == registered_course_schedule.days and
                not (course_schedule.endTime <= registered_course_schedule.startTime or
                     course_schedule.startTime >= registered_course_schedule.endTime)):
                messages.error(request, f"Schedule conflict: You are already registered for another course at the same time ({registration.course.name}).")
                return redirect('course_detail', course_id=course_id)

        # Check if there are available spots
        if course.available_spots > 0:
            StudentRegistration.objects.create(student=student, course=course)
            course.available_spots -= 1
            course.save()
            messages.success(request, "Successfully registered for the course.")
            return redirect('schedule')
        else:
            messages.error(request, "No available spots for this course.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('course_detail', course_id=course_id)

@login_required
def schedule(request):
    student = request.user.student
    registrations = StudentRegistration.objects.filter(student=student).select_related('course', 'course__courseschedule')

    courses_with_schedules = [{
        'course': myapp.course,
        'schedule': myapp.course.courseschedule
    } for myapp in registrations if hasattr(myapp.course, 'courseschedule')]

    return render(request, 'myapp/schedule.html', {
        'courses_with_schedules': courses_with_schedules
    })



def available_courses(request):
    student = request.user.student
    completed_courses = student.completed_courses.all()
    available_courses = Course.objects.filter(
        prerequisites__in=completed_courses
    ).distinct()
    return render(request, 'courses/available_courses.html', {'courses': available_courses})


def home(request):
    notifications = Notification.objects.filter(active=True).order_by('-date_created')
    return render(request, 'home.html', {'notifications': notifications})




def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': all_courses})



@login_required
def profile(request):
    student = get_object_or_404(Student, user=request.user)
    completed_courses = student.completed_courses.all()
    return render(request, 'myapp/profile.html', {
        'student': student,
        'completed_courses': completed_courses
    })

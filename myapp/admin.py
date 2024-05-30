from django.contrib import admin
from .models import CustomUser, Student, Course, CourseSchedule, StudentRegistration
from .models import Notification

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(CourseSchedule)
admin.site.register(StudentRegistration)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor')
    filter_horizontal = ('prerequisites',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'date_created', 'active', 'deadline_date']
    list_filter = ['active', 'date_created']
    search_fields = ['message']




class CompletedCoursesInline(admin.TabularInline):
    model = Student.completed_courses.through
    extra = 1
    verbose_name = "Completed Course"
    verbose_name_plural = "Completed Courses"



class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('completed_courses',)    
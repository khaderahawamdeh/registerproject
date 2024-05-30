from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  
     pass

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_courses = models.ManyToManyField('Course', related_name='completed_by_students', blank=True)

    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='prerequisite_for')
    available_spots = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def update_available_spots(self):
        spots_taken = StudentRegistration.objects.filter(course=self).count()
        self.available_spots = self.capacity - spots_taken
        self.save()

class CourseSchedule(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    days = models.CharField(max_length=50)
    startTime = models.TimeField()
    endTime = models.TimeField()
    roomNo = models.CharField(max_length=20)

class StudentRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')



class Notification(models.Model):
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deadline_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification created on {self.date_created.strftime('%Y-%m-%d')} - Active: {self.active}"

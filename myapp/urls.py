from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('search/', views.search, name='search'),
    path('home/', views.home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/register/', views.register_course, name='register_course'),  
    path('course/<int:course_id>/schedule/', views.course_schedule, name='course_schedule'),
    path('schedule/', views.schedule, name='schedule'),
    path('courses/', views.courses, name='courses'),
    path('profile/', views.profile, name='profile'),
]

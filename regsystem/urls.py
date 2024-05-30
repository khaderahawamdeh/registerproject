
from django.urls import path, include
from django.contrib import admin
from myapp.views import user_login  
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    path('', user_login, name='login'),  
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('', include('myapp.urls')),

]


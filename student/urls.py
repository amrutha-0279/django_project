from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='courses'),
    
    path('signup/<int:course_id>/', views.signup_course, name='signup_course'),
    path('my-courses/', views.my_courses, name='my_courses'),

    
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),

    
    path('change-password/', views.change_password, name='change_password'),
    path('signup-course/<int:course_id>/', views.signup_course, name='signup_course'),
    path('profile/',views.profile,name='profile'),
]

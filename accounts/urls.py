from django.urls import path
from .import views
urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('forgot_password/',views.ForgotPassword,name='forgot'),
    path('verify/<str:token>/', views.verify, name='verify'),
    path('logout/', views.logout_view, name='logout'),
    path('set_new_password/',views.set_new_password,name='set_new_password'),
     
]
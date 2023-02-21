from django.urls import path


from account import views
from account.views import *


urlpatterns = [
     path('', views.home,name="home"),
     path('login/', views.LoginForm,name="LoginForm"),
     path('register/', views.RegisterForm,name="RegisterForm"),
     path('dashboard/',views.dashboard,name="dashboard"),
     path('userdetails/<str:pk>/', views.userdetails,name="userdetails"),
     path('logout/', views.logoutuser, name ='logoutuser'),

     ]
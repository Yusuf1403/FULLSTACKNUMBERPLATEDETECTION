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

     path('user_records',UserRecordsListView.as_view(), name='user_records'),
     path('user_record_create',UserRecordsCreateView.as_view(), name='user_record_create'),
     path('user_record_update/<int:pk>/',views.UserRecordUpdate, name='user_record_update'),
     path('user_record_delete/<int:pk>/',views.UserRecordDelete, name='user_record_delete'),

     ]
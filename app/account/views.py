from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login, logout
from account.forms import UserRegisterForm, UserEditForm
from django.contrib import messages

from account.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    context={}
    return render(request,"account/home.html",context)

def LoginForm(request):
    try:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username , password = password)     
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse("<h1>Registered email or Password is incorrect !!!</h1>")
              
    except Exception as e:
        print(e)                

    context={}
    return render(request,"account/LoginForm.html",context)

def RegisterForm(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account is created for ' , username)

            return redirect('LoginForm')  
    else:
        form = UserRegisterForm()

    context = {}   
    context.update({'form1':form}) 
    return render(request, 'account/registerPage.html',context)

from django.db.models import Q

@login_required
def dashboard(request):
    search_post = request.GET.get('search')
    if search_post:
        users = User.objects.filter(Q(email__icontains=search_post) | Q(name__icontains=search_post) | Q(user_type__icontains=search_post)).order_by('-created_at')
    else:
        users = User.objects.all().order_by('-created_at')
    context={'request':request,'users':users}
    return render(request,"account/UserDashboard.html",context)

@login_required
def userdetails(request,pk):
    userdetail=User.objects.get(id=pk)    
    registerform=UserEditForm(instance=userdetail)
    if request.method=='POST':
        registerform=UserEditForm(request.POST,request.FILES,instance=userdetail)
        if registerform.is_valid():
            registerform.save()
            return redirect('dashboard')
        else:
            messages.warning(request,f'Username or Password is incorrect !!! ')


    context={'userdetail':userdetail,'registerform':registerform,'files':request.FILES}
    return render(request,"account/userdetailsform.html",context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')

from .models import *
from django.shortcuts import render
from django.db.models import Q  # New
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView,DeleteView

class UserRecordsListView(ListView):
    model = UserRecord
    template_name = 'account/user_record_list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        search_post = request.GET.get('search')
        if search_post:
            posts = UserRecord.objects.filter(Q(created_by__email__icontains=search_post) | Q(license_plate_text__icontains=search_post)).order_by('-created_at')
        else:
            # If not searched, return default posts
            posts = UserRecord.objects.filter(created_by=request.user).order_by('-created_at')
        return posts

from django.urls import reverse
class UserRecordsCreateView(CreateView):
    model = UserRecord
    template_name = 'account/user_records.html'
    fields="__all__"

    def get_success_url(self):
        return reverse('user_records')

from django.shortcuts import get_object_or_404

from .forms import *
from django.utils import timezone

def UserRecordUpdate(request,pk):
    instance = get_object_or_404(UserRecord, id=pk)
    recordform=UserRecordForm(instance=instance)
    if request.method=='POST':
        recordform=UserRecordForm(request.POST, request.FILES, instance=instance)
        if recordform.is_valid():
            recordform.save()
            instance.updated_at=timezone.now()
            instance.save()
            return redirect('user_records')
    
    context={'recordform':recordform,'record':instance}
    return render(request,"account/user_record_update.html",context)


def UserRecordDelete(request,pk):
    userdetails=UserRecord.objects.get(id=pk)
    if request.method == 'POST':
        userdetails.delete()
        return redirect('user_records')
    return render(request,'account/delete.html', {'object': userdetails})

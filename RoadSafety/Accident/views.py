from django.shortcuts import render
from . import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, HttpResponse, redirect




# Create your views here.
def index(request):
    return render (request,'index.html')

def Login(request):
    return render(request,'login.html')

def stdash(request):
    users=request.user.id
    userObj=User.objects.get(id=users)
    return render(request,"userdash.html",{'users':userObj})

def registerr(request):
    return render(request,'register.html')

def signout(request):
      logout(request)
      return redirect('home')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            else:
                return redirect('user_dash')
        else:
            return redirect('Login')
    return redirect('Login')

#register view
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # gender = request.POST['gender']
        # education = request.POST['education']
        # phone = request.POST['phone']
        if User.objects.filter(username=username).exists():
            messages.info(request,"user already exist")
            return render(request,'Login')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"email already taken")
            return render(request,'Login')
        else:
          user=User.objects.create_user(username=username,email=email,password=password)
          user.save()
        return redirect('Login')
    else:
     return render(request,'Login')


def staff_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # gender = request.POST['gender']
        # education = request.POST['education']
        # phone = request.POST['phone']
        if User.objects.filter(username=username).exists():
            messages.info(request,"user already exist")
            return render(request,'staff_register.html')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"email already taken")
            return render(request,'staff_register.html')
        else:
          user=User.objects.create_user(username=username,email=email,password=password)
          user.is_staff=True
          user.save()
         
        return redirect('Login')
    else:
     return render(request,'staff_register.html')
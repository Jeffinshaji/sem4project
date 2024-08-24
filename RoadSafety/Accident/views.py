from django.shortcuts import render
from . import views
# Create your views here.
def index(request):
    return render (request,'index.html')
def about(request):
    return render (request,'about.html')
def service(request):
    return render (request,'service.html')

def team(request):
    return render (request,'team.html')
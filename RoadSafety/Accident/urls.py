from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('about',views.about,name='about'),
    path('service',views.service,name='service'),
    path('team',views.team,name='team'),
    path('user_Login',views.user_Login,name='Login'),
   ]

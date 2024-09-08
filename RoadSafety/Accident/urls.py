from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name='home'),
    path('user_login',views.user_login,name='user_login'),
    path('Login',views.Login,name='Login'),
    path("userdash", views.stdash, name = 'user_dash'),
    path('signout',views.signout, name="signout"),
    path("register",views.registerr,name='register'),
    path('user_register',views.user_register,name='user_register'),
   ]

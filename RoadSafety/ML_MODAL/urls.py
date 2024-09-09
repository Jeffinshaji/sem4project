from django.urls import path,include
from . import views


urlpatterns = [
    # path('predict_route',views.predict_route,name='predict_route'),
    path('predict/', views.predict_accident, name='predict_accident'),
]
from . import views
from django.urls import path

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('dashboard', views.Dashboard, name='dashboard'),
    path('login', views.Login, name='login'),
    path('register', views.Register, name='register'),
    path('test', views.test, name='test'),
]

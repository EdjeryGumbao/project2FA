from . import views
from django.urls import path

urlpatterns = [
    path('', views.dummyDashboard, name='dummydashboard'),
    path('dashboard', views.dummyDashboard, name='dummydashboard'),
    path('dummylogout', views.dummylogout, name='dummylogout'),
    path('test', views.dummytest, name='dummytest'),
]
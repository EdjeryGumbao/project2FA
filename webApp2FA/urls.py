# default modules
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('login', views.login_user, name='login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register', views.register_user, name='register_user'),

    path('add_website', views.add_website, name='add_website'),
    # path('websiteAction', views.websiteAction, name='websiteAction'),

    path('profile', views.profile, name='profile'),
    path('gallery', views.gallery, name='gallery'),

    # path('base', views.base, name='base'),
]
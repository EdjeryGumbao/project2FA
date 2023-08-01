# default modules
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),

    path('profile', views.profile, name='profile'),
    path('gallery', views.gallery, name='gallery'),
    path('intrudergallery', views.intrudergallery, name='intrudergallery'),

    # path('base', views.base, name='base'),
]
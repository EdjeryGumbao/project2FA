from django.shortcuts import render, redirect
from .models import DummyUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from webApp2FA.models import WebsiteList

from cameraApp.camera import VideoCamera
from cameraApp.views import index as cameraIndex

website_url = 'http://127.0.0.1:8000/dummy/'

def dummyDashboard(request):
    context={} # This is a dictionary, You can add DB tables values here later

    if request.session.get('message') is not None:
        context['alert_error'] = request.session['message']
        del request.session['message']

    if request.method == 'POST':

        # User Registration
        if request.POST['button'] == 'signup': 
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                new_DummyUser = DummyUser(Email=email, Password=make_password(password))
                new_DummyUser.save()
                # request.session['auth'] = True # turn this on if you want auto log in after registration
                context['alert_error'] = 'Successfully Registered'
            else:
                context['alert_error'] = 'Error: Passwords do not match.'
        
        # User Log in
        elif request.POST['button'] == 'login':
            email = request.POST['email']
            password = request.POST['password']
            
            try:
                user = DummyUser.objects.get(Email=email)
                    
                if user and check_password(password, user.Password):
                    try:
                        website = WebsiteList.objects.filter(websiteUrl=website_url, username=email).first()
                        print(website)
                        if website:
                            return cameraIndex(request, email, website_url)
                        else:     
                            request.session['auth'] = True
                            context['alert_error'] = 'Successfully Logged in'
                    except WebsiteList.DoesNotExist:
                        request.session['auth'] = True
                        context['alert_error'] = 'Successfully Logged in'
                else:
                    context['alert_error'] = 'Error: Passwords do not match.'
            except DummyUser.DoesNotExist:
                context['alert_error'] = 'Error: Email does not exist!'

    return render(request, 'Dashboard.html', context)

def login(request, name):
    print('logging in')
    context={} # This is a dictionary, You can add DB tables values here later
    currentUser = request.session.get('currentUser')
    # print (currentUser)
    # print (name)
    if name == currentUser:
        # print('correct in')
        request.session['auth'] = True
        request.session['message'] = 'Successfully Logged in'
    else:
        print('error in logging in')
        request.session['message'] = 'Error: Face authentication failed.'
        
    return redirect('dummydashboard')

def dummytest(request):
    authenFace(request)
    # return render(request, 'test.html')

def authenFace(request):
    return cameraIndex(request)

def dummylogout(request):
    dummySessionList = ['auth', 'currentUser', 'message', 'match_value', 'website_url', 'image_path', 'filename']
    remove_sessions_from_list(request, dummySessionList)
    request.session['message'] = 'You are now logged out'
    return redirect('dummydashboard')

def remove_sessions_from_list(request, session_key_list):
    for session_key in session_key_list:
        if session_key in request.session:
            del request.session[session_key]
    request.session.save()
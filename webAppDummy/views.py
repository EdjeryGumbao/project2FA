from django.shortcuts import render, redirect
from .models import DummyUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from cameraApp.views import index as cameraIndex
from webApp2FA.models import WebsiteList

website_url = 'dummy'

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
                        website = WebsiteList.objects.get(websiteUrl=website_url, username=email)
                        if website:
                            return cameraIndex(request, email)
                    except WebsiteList.DoesNotExist:
                        request.session['auth'] = True
                        request.session['message'] = 'Successfully Logged in'
                    
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
    request.session.clear()  # Remove all session data
    if name == currentUser:
        # print('correct in')
        request.session['auth'] = True
        request.session['message'] = 'Successfully Logged in'
        print(request.session['auth'])
    else:
        print('error in')
        request.session['message'] = 'Error: Face authentication failed.'
        
    return redirect('dummydashboard')
    

def dummytest(request):
    authenFace(request)
    # return render(request, 'test.html')

def authenFace(request):
    return cameraIndex(request)


def dummylogout(request):
    request.session.clear()  # Remove all session data
    request.session['message'] = 'You are now logged out'
    return redirect('dummydashboard')
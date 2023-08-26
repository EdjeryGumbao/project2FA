from django.shortcuts import render, redirect

from django.http.response import StreamingHttpResponse
from django.http import HttpResponseRedirect
from cameraApp.camera import VideoCamera 

import cv2
import os

from django.contrib.auth.models import User
from webApp2FA.models import FailedAuthen
from webApp2FA.models import WebsiteList  # Import your model

from django.utils import timezone
from django.core.files import File
from datetime import datetime

def index(request, currentUser, website_url):
    request.session['currentUser'] = currentUser
    request.session['website_url'] = website_url
    return render(request, 'index.html')

def gen(request, camera):
    global match, image_path, filename
    while True:
    # while True:
        ret, frame = camera.get_frame(request)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        match_value = request.session.get('match_value')  # Returns None if the key is not found
        if match_value is not None:
            match = request.session['match_value']

        else:
            image_path = request.session['image_path']
            filename = request.session['filename']
            
            # if os.path.exists(image_path):
            #     print('the temp pic exist is cameraApp')

            match = None

def unique_users_for_username(username):
    unique_user_ids = WebsiteList.objects.filter(username=username).values('userID').distinct()
    unique_users = User.objects.filter(id__in=unique_user_ids)
    return unique_users

def delete_file(file_name):
    try:
        # Get the absolute path of the current file
        current_file_path = os.path.abspath(__file__)

        # Get the directory name of the current file
        current_directory = os.path.dirname(current_file_path)

        # Get the directory name of the parent directory (your_app directory)
        app_directory = os.path.dirname(current_directory)

        image_path = os.path.join(app_directory, "media" , "intruderimages", filename)

        # if os.path.exists(image_path):
        #     print(image_path + ' exist!')

        os.remove(image_path)
        print(f"{image_path} has been deleted.")
    except OSError as e:
        print(f"Error deleting {image_path}: {e}")

def authenFace(request):
    currentUser = request.session['currentUser']
    website_url = request.session['website_url']
    
    unique_users = unique_users_for_username(currentUser)
    print(unique_users) # i stopped here, continue this later, eat first

    from webAppDummy.views import login as dummyLogin
    from django.core.files.uploadedfile import SimpleUploadedFile

    if match is not None:
        delete_file(filename)
        return dummyLogin(request, match)
    else:
        for user in unique_users:
            failed_authen = FailedAuthen()
            failed_authen.userID = user
            failed_authen.FailedAuthenImage = filename
            failed_authen.save()
            # delete_file(filename)
        return dummyLogin(request, match)

def video_feed(request):
    currentUser = request.session['currentUser']
    website_url = request.session['website_url']
    return StreamingHttpResponse(gen(request, VideoCamera(request, currentUser, website_url)), content_type='multipart/x-mixed-replace; boundary=frame')
    
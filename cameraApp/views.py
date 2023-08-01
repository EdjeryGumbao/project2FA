from django.shortcuts import render, redirect

from django.http.response import StreamingHttpResponse
from django.http import HttpResponseRedirect
from cameraApp.camera import VideoCamera 

def index(request, currentUser):
    request.session['currentUser'] = currentUser
    return render(request, 'index.html')

def gen(request, camera):
    global match
    while request.session.get('match_value') is None:
        frame = camera.get_frame(request)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    match = request.session['match_value']
    print(match)

def authenFace(request):
    from webAppDummy.views import login as dummyLogin
    return dummyLogin(request, match)

def video_feed(request):
    currentUser = request.session.get('currentUser')
    return StreamingHttpResponse(gen(request, VideoCamera(request, currentUser)), content_type='multipart/x-mixed-replace; boundary=frame')
    
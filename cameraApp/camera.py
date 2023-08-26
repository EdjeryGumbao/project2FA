import cv2
import os
import face_recognition
import numpy as np
from webApp2FA.models import WebsiteList, UserImage

import os
from django.conf import settings
from django.utils import timezone

import threading
from deepface import DeepFace

def get_selfieimage_path(image_filename):
    # Construct the absolute file path to the image
    media_root = settings.MEDIA_ROOT
    selfieimage_path = os.path.join(media_root, 'selfieimage', image_filename)
    return selfieimage_path

class VideoCamera(object):
    def __init__(self, request, currentUser, website_url):
        self.video = cv2.VideoCapture(0)
        self.currentUser = currentUser
        self.request = request
        self.match_value = None
        self.website_url = website_url
        self.image_path = None
        self.filename = None

        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))

        def set_camera_resolution(cap, width, height):
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Set the desired resolution (e.g., 640x480)
        desired_width = 340
        desired_height = 280

        # Set the camera resolution to the desired values
        set_camera_resolution(self.video, desired_width, desired_height)
        self.website = WebsiteList.objects.filter(websiteUrl=self.website_url, username=self.currentUser).first()
        
        try:
            user_image = UserImage.objects.get(userID=self.website.userID)
            path = user_image.userImage.url.lstrip('/')  # example: 'cameraApp/images/ed.png' 'media/selfieimages/ed_EYWq4vT.png'
        except UserImage.DoesNotExist:
            user_image = None
            path = ''

        print(path)
        images = []
        self.classNames = []

        self.curImg = cv2.imread(path)
        images.append(self.curImg)

        self.classNames.append(os.path.splitext(os.path.basename(path))[0])

        print(self.classNames)  # Output: ['image1']
        print(len(images))  # Output: 1
            
        def findEncodings(images):  
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        self.encodeListKnown = findEncodings(images)

    def capture_and_save_image(self, frame):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        self.filename = f"{self.website.userID}_temp_image_{timestamp}.png"
        print(self.filename)

        # Get the absolute path of the current file
        current_file_path = os.path.abspath(__file__)

        # Get the directory name of the current file
        current_directory = os.path.dirname(current_file_path)

        # Get the directory name of the parent directory (your_app directory)
        app_directory = os.path.dirname(current_directory)

        self.image_path = os.path.join(app_directory, "media" , "intruderimages", self.filename)
        print("Current directory:", self.image_path)

        # Capture and save the image using OpenCV
        success = cv2.imwrite(self.image_path, frame)
        print(f"Photo pic: {success}")
        return self.filename, self.image_path

    def __del__(self):
        self.video.release()

    def check_face(self, frame):
        global face_match
        # try:
        #     if DeepFace.verify(frame, self.curImg.copy())['verified']:
        #         face_match = True
        #     else:
        #         face_match = False
        # except ValueError:
        #     face_match = False
        
    # This function is used in views
    def get_frame(self, request):
        success, self.image = self.video.read()
        taken = None

        # if taken == None:
        #     taken = cv2.imwrite(, self.image)

        if self.image_path == None:
            print('taking pic')
            request.session['filename'], request.session['image_path'] = self.capture_and_save_image(self.image)

        facesCurFrame = face_recognition.face_locations(self.image)
        encodesCurFrame = face_recognition.face_encodings(self.image,facesCurFrame)

        for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                request.session['match_value'] = None
                
                y1, x2, y2, x1 = faceloc
                cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)


                
                if matches[matchIndex]:
                    try:
                        threading.Thread(target=self.check_face, args=(self.image.copy(),)).start()
                        
                        cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        text = "Ready"
                        cv2.putText(self.image, text, (520, 340), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        request.session['match_value'] = self.currentUser
                    except ValueError:
                        print(f"Error: {ValueError}")
                        cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        request.session['match_value'] = None

                    # name = self.classNames[matchIndex].upper()

                    # print(name)
                    # cv2.rectangle(self.image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    # cv2.putText(self.image, self.currentUser, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


                    # from webAppDummy.views import login as dummyLogin
                    # return dummyLogin(self.request, name)

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.png', self.image)

        return ret, jpeg.tobytes()
    
    # def get_match_value(self, value):
    #     self.match_value = value
    #     return value
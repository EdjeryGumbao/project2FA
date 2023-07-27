
import cv2
import os
import face_recognition
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))

        def set_camera_resolution(cap, width, height):
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Set the desired resolution (e.g., 640x480)
        desired_width = 340
        desired_height = 280

        # Set the camera resolution to the desired values
        set_camera_resolution(self.video, desired_width, desired_height)

        path = 'cameraApp/images'
        images = []
        self.classNames = []
        myList = os.listdir(path)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        self.encodeListKnown = findEncodings(images)

    def __del__(self):
        self.video.release()
        
    # This function is used in views
    def get_frame(self):
        success, self.image = self.video.read()

        facesCurFrame = face_recognition.face_locations(self.image)
        encodesCurFrame = face_recognition.face_encodings(self.image,facesCurFrame)

        for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)
                
                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceloc
                    cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(self.image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(self.image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.png', self.image)

        return jpeg.tobytes()
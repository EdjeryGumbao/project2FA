import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'cameraApp/images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

def markAttendance(name):
    with open('Attendance.csv', 'r') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,1,1)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceloc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Remove this line to draw on the original image
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name)
    
    
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

################################### backup #############################
# import cv2
# import os

# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()
        
#     # This function is used in views
#     def get_frame(self):
#         success, self.image = self.video.read()

#         # Convert the image to grayscale
#         gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

#         # Construct the full path to the Haar Cascades XML file
#         cascade_filename = 'haarcascade_frontalface_default.xml'
#         cascade_path = os.path.join(os.path.dirname(__file__), 'opencv', cascade_filename)

#         # Load the face detection model (Haar Cascades)
#         face_cascade = cv2.CascadeClassifier(cascade_path)

#         # Detect faces in the image
#         faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         # Draw rectangles around the detected faces
#         for (x, y, w, h) in faces:
#             cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Flip the frame horizontally
#         frame_flip = cv2.flip(self.image, 1)

#         # Encode the frame as JPEG
#         ret, jpeg = cv2.imencode('.jpg', frame_flip)

#         return jpeg.tobytes()
################################### backup #############################

# import os

# def check_file_exists(file_path):
#     current_directory = os.path.dirname(__file__)
#     full_path = os.path.join(current_directory, file_path)
#     return os.path.exists(full_path)

# # Usage example
# file_path = 'openCV/haarcascade_frontalface_default.xml'
# if check_file_exists(file_path):
#     print(f"The file '{file_path}' exists in the current directory.")
# else:
#     print(f"The file '{file_path}' does not exist in the current directory.")


# import os
# import cv2

# def draw_rectangle_on_faces(cascade_filename):
#     # Construct the full path to the Haar Cascades XML file
#     cascade_path = os.path.join(os.path.dirname(__file__), 'opencv', cascade_filename)

#     # Load the face detection model (Haar Cascades)
#     face_cascade = cv2.CascadeClassifier(cascade_path)
    
#     # Open the default camera
#     cap = cv2.VideoCapture(0)
    
#     while True:
#         # Capture a frame from the camera
#         ret, frame = cap.read()
        
#         if not ret:
#             break
        
#         # Convert the frame to grayscale for face detection
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
#         # Detect faces in the frame
#         faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
#         # Draw rectangles around the detected faces
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
#         # Display the frame with rectangles
#         cv2.imshow('Camera', frame)
        
#         # Exit the loop when 'q' key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     # Release the video capture and close the OpenCV windows
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     # Use the relative path to the Haar Cascades XML file
#     cascade_filename = 'haarcascade_frontalface_default.xml'
    
#     draw_rectangle_on_faces(cascade_filename)




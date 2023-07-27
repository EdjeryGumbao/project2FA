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



# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime

# class FaceRecognition:
#     def __init__(self):
#         self.path = 'cameraApp/images'
#         self.images = []
#         self.classNames = []
#         self.myList = os.listdir(self.path)
#         print(self.myList)

#         for cl in self.myList:
#             curImg = cv2.imread(f'{self.path}/{cl}')
#             self.images.append(curImg)
#             self.classNames.append(os.path.splitext(cl)[0])

#         self.encodeListKnown = self.findEncodings(self.images)

#     def findEncodings(self, images):
#         encodeList = []
#         for img in images:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             encode = face_recognition.face_encodings(img)[0]
#             encodeList.append(encode)
#         return encodeList

#     def recognize_faces(self, frame):
#         imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#         for encodeFace, faceloc in zip(encodesCurFrame, facesCurFrame):
#             matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
#             print(faceDis)
#             matchIndex = np.argmin(faceDis)

#             if matches[matchIndex]:
#                 name = self.classNames[matchIndex].upper()
#                 print(name)
#                 y1, x2, y2, x1 = faceloc
#                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                 cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#         return frame

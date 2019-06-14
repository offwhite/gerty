#!/usr/bin/env python
import cv2
import sys
import numpy as np
import os

detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
font = cv2.FONT_HERSHEY_SIMPLEX

video_capture = cv2.VideoCapture(0)

running = True
img_index = 0
while running:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # recognise face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        if (confidence < 100):
            name =  "Person "+str(id+1)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            name = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(
                    frame, str(name), (x+5,y-5), font, 1, (255,255,255), 2
                   )

        cv2.putText(
                    frame, str(confidence), (x+0,y+h+30), font, 1, (255,255,0), 2
                   )

    # Display the resulting frame
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)

    # handle inputs
    if key == ord('c'):
        # Draw a rectangle around the faces
        face_index = 0
        for (x, y, w, h) in faces:
            # save face
            print(face_index)
            face = frame[y:y+h, x:x+w]
            cv2.imwrite("faces/unknown/face_"+str(img_index)+"."+str(face_index)+".jpg", face)
            img_index+=1
            face_index+=1
            print('saved')

    if key == ord('q'):
        print("\n [INFO] Exiting Program and cleanup stuff")
        video_capture.release()
        cv2.destroyAllWindows()
        running = False

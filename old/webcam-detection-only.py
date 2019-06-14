#!/usr/bin/env python
import cv2
import sys

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

running = True
img_index = 0
while running:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)

    # handle inputs
    if key == ord('c'):
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            # save face
            face = frame[y:y+h, x:x+w]
            cv2.imwrite("faces/face"+str(img_index)+".jpg", face)
            img_index+=1
            print('saved')

    if key == ord('q'):
        video_capture.release()
        cv2.destroyAllWindows()
        running = False

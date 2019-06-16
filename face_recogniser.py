import numpy as np
import os

class Recogniser:
    def __init__(self, cv2, db):
        self.cv2 = cv2
        self.db = db
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        self.recognizer = self.cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')

    def call(self, frame):
        faces = []
        grey = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in self.detected_faces(grey):
            self.cv2.rectangle(frame, (x-5, y-5), (x+w+5, y+h+5), (255, 255, 255), 1)
            id, distance = self.recognizer.predict(grey[y:y+h,x:x+w])
            confidence = format(round(100 - distance))
            faces.append((x, y, w, h, id, confidence))

        return faces

    def detected_faces(self, grey):
        return self.detector.detectMultiScale(
            grey,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=self.cv2.CASCADE_SCALE_IMAGE
        )

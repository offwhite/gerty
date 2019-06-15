import numpy as np
import os

class Recogniser:
    def __init__(self, cv2, db):
        self.cv2 = cv2
        self.db = db
        self.recognizer = self.cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')

    def call(self, frame, faces):
        recognised_faces = []
        for (x, y, w, h) in faces:
            # recognise face
            gray = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2GRAY)
            id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])

            percentage = format(round(100 - confidence))

            recognised_faces.append((x, y, w, h, id, percentage))

        return recognised_faces

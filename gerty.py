#!/usr/bin/env python

import cv2
import vision

class Gerty:
    def __init__(self, cv2):
        self.vision = vision.Vision(cv2)
        self.cv2 = cv2
        self.debug = True
        self.show_upei = False

    def start(self):
         print("[INFO] Starting Gerty - press 'q' to quit")
         self.running = True
         while self.running:
            (self.frame, self.faces) = self.vision.call()
            self.process_frame()

    def process_frame(self):
        if(self.debug):
            self.cv2.imshow('View', self.frame)
        if(self.show_upei):
          self.cv2.imshow('Unit Primary Emotional Interface', self.upei())
        key = self.cv2.waitKey(1)
        self.handle_input(key)

    def handle_input(self, key):
        if key == ord('q'):
            self.stop()

        if key == ord('c'):
            print('testing')

    def stop(self):
        print("\n[INFO] Exiting Gerty")
        self.vision.stop()
        self.cv2.destroyAllWindows()
        self.running = False

    def upei(self):
        # these images should be loaded into memory on load
        exp = 'neutral'
        left = 500
        for (x, y, w, h, id, conf) in self.faces:
            left = x
            if(int(conf) < 50):
                exp = 'confused'
            else:
                exp = 'happy'

        if(left < 200): exp = 'look_right'
        elif(left > 900): exp = 'look_left'
        image = self.cv2.imread('unit_primary_emotional_interface/'+exp+'.jpg', 1)
        return image
app = Gerty(cv2)
app.start()

#!/usr/bin/env python

import cv2
import vision
import upei
import db

class Gerty:
    def __init__(self, cv2):
        self.db = db.Database()
        self.vision = vision.Vision(cv2, self.db)
        self.upei = upei.Upei(cv2)
        self.cv2 = cv2
        self.debug = True
        self.show_upei = False
        self.framerate = 2 # number of frames per second

    def start(self):
         print("[INFO] Starting Gerty - press 'q' to quit")
         self.running = True

         while self.running:
            self.process_frame()

    def process_frame(self):
        (self.frame, self.faces) = self.vision.call()
        if(self.debug):
            self.cv2.imshow('View', self.frame)
        if(self.show_upei):
          self.cv2.imshow('Unit Primary Emotional Interface', self.render_upei())

        key = self.cv2.waitKey(round(1000 / self.framerate))
        self.handle_keyboard_input(key)

    def render_upei(self):
        exp = 'neutral'
        left = 500
        for (x, y, w, h, id, conf) in self.faces:
            left = x
            if(int(conf) < self.vision.recognition_threshold):
                exp = 'sad'
            else:
                exp = 'happy'

        if(left < 200): exp = 'look_right'
        elif(left > 900): exp = 'look_left'
        return self.upei.image(exp)

    def handle_keyboard_input(self, key):
        if (key == ord('q') or key == ord('x')):
            self.stop()

        if key == ord('c'):
            print('testing')

        if key == ord('d'):
            self.debug = (self.debug == False)

        if key == ord('s'):
            self.set_user()

        if key == ord('u'):
            print(self.db.all('users'))

        if key == ord('t'):
            self.vision.train()

    def set_user(self):
        id = input('Id: ')
        name = input('Name: ')
        if(name == 'delete'):
            return self.db.execute('delete from users where id = '+id)
        self.db.execute('update users set name="'+name+'" where id = '+id)
        self.vision.user_list = None

    def stop(self):
        print("\n[INFO] Exiting Gerty")
        self.vision.stop()
        self.cv2.destroyAllWindows()
        self.running = False


app = Gerty(cv2)
app.start()

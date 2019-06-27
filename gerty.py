#!/usr/bin/env python

from subprocess import call
import cv2
import vision
import upei
import db
import short_term_memory

class Gerty:
    def __init__(self, cv2):
        self.db = db.Database()
        self.stm = short_term_memory.StmUnit(self.db)
        self.vision = vision.Vision(cv2, self.db, self.stm)
        self.upei = upei.Upei(cv2)
        self.cv2 = cv2
        self.debug = True
        self.show_upei = True
        self.framerate = 2 # number of frames per second
        self.prev_users_in_room = {}
        self.users_in_room = {}

    def start(self):
        self.say("waking up")
        print("[INFO] Starting Gerty - press 'q' to quit")
        self.running = True

        while self.running:
            self.process_frame()

    def process_frame(self):
        print('[INFO] processing frame')
        (self.frame, self.faces) = self.vision.call()
        if(self.debug):
            self.cv2.imshow('View', self.frame)
        if(self.show_upei):
            self.cv2.imshow('Unit Primary Emotional Interface', self.render_upei())

        key = self.cv2.waitKey(round(1000 / self.framerate))
        self.handle_keyboard_input(key)
        self.react_to_users()

    def react_to_users(self):
        new_users = self.stm.new_users()
        for id in new_users:
            name = self.stm.users_name(id)
            self.say('hello '+name)

    def say(self, string):
        call(["python3", "speak.py", string])

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
            self.say('testing the longer words in a sentence')
            self.say('this is a different sentence.')

        if key == ord('d'):
            self.debug = (self.debug == False)

        if key == ord('s'):
            self.set_user_name()

        if key == ord('u'):
            print(self.db.all('users'))

        if key == ord('t'):
            self.vision.train()

    def set_user_name(self):
        id = input('Id: ')
        name = input('Name: ')
        if(name == 'delete'):
            return self.db.execute('delete from users where id = '+id)
        self.db.execute('update users set name="'+name+'" where id = '+id)
        self.vision.user_list = None

    def stop(self):
        print("\n[INFO] Exiting Gerty")
        self.say('Goodbye')
        self.vision.stop()
        self.cv2.destroyAllWindows()
        self.running = False


app = Gerty(cv2)
app.start()

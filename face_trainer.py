import numpy as np
from PIL import Image
import os
import time

# handed an image of unrecognised face
# 1. store that image
# 2. check how many we have of that id
# 3. if enough, run training
class Trainer:
    def __init__(self, cv2, db, stm):
        self.cv2 = cv2
        self.db = db
        self.stm = stm
        self.path = 'faces'
        self.recognizer = self.cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.images_required = 30
        self.user_id = None

    def call(self, frame, face):
        self.set_user_id()

        (x,y,w,h) = face
        face_image = frame[y:y+h, x:x+w]
        self.save_image(face_image)

        if(self.image_count > self.images_required):
            self.train()
            self.create_user()

    def save_image(self, image):
        now = str(round(time.time() * 1000))
        path = "faces/"+str(self.user_id)+"/"+str(now)+".png"
        self.cv2.imwrite(path, image)
        self.image_count += 1

    def set_user_id(self):
        if(self.user_id != None):
            return self.user_id
        existing_users = self.db.all('users')
        self.user_id = len(existing_users)

        # create dir for this user
        dir_name = 'faces/'+str(self.user_id)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        else:
            print('[INFO] Training folder already found')

        self.image_count = len([os.path.join(dir_name,f) for f in os.listdir(dir_name)])

    def training_images(self):
        files = []
        for r, d, f in os.walk(self.path):
            for file in f:
                if '.png' in file:
                    files.append(os.path.join(r, file))
        return files

    def create_user(self):
        self.db.insert('users', {'id': self.user_id, 'name': 'User '+str(self.user_id), 'permissions': 0})
        self.stm.see_user(self.user_id)
        self.user_id = None

    def train(self):
        images = self.training_images()
        print('[INFO] Training against '+str(len(images))+' images')

        faceSamples=[]
        ids = []
        for image_path in images:
            PIL_img = Image.open(image_path).convert('L') # grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(image_path.split('/')[-2])
            faceSamples.append(img_numpy)
            ids.append(id)

        self.recognizer.train(faceSamples, np.array(ids))
        self.recognizer.write('trainer/trainer.yml')
        print('[INFO] Training Complete')

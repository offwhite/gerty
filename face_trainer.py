import numpy as np
from PIL import Image
import os
import time

# handed an image of unrecognised face with an id
# store that image, check how many we have of that id
# if enough, run training
class Trainer:
    def __init__(self, cv2):
        self.cv2 = cv2
        self.path = 'faces'
        self.unknown_dir = 'faces/unknown'
        self.recognizer = self.cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.images_required = 20

    def call(self, frame, face, id):
        self.unknown_images = [os.path.join(self.unknown_dir,f) for f in os.listdir(self.unknown_dir)]
        (x,y,w,h) = face
        face_image = frame[y:y+h, x:x+w]
        self.save_image(face_image, id)

        if(len(self.unknown_images) > self.images_required):
          self.train()

    def save_image(self, image, id):
        existing_count = len(self.unknown_images)
        self.cv2.imwrite("faces/unknown/"+str(id)+"."+str(existing_count)+".jpg", image)

    def training_images(self):
        files = []
        for r, d, f in os.walk(self.path):
            for file in f:
                if '.jpg' in file:
                    files.append(os.path.join(r, file))
        return files

    def save_unrecognised(self):
        id = input('enter id: ')
        now = str(round(time.time() * 1000))
        index = 0
        for imagePath in self.unknown_images:
            os.rename(imagePath, self.path+'/'+str(id)+'/'+str(id)+'.'+now+'.'+str(index)+'.jpg')
            index+=1

    def train(self):
        self.save_unrecognised()
        images = self.training_images()
        print(images)
        print('[INFO] Training against '+str(len(images))+' images')

        faceSamples=[]
        ids = []
        for imagePath in images:
            PIL_img = Image.open(imagePath).convert('L') # grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[0])
            faceSamples.append(img_numpy)
            ids.append(id)


        self.recognizer.train(faceSamples, np.array(ids))
        self.recognizer.write('trainer/trainer.yml')
        print('[INFO] Training Complete')

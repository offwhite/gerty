# on call, read the view, detect and recognise faces, return frame
import face_recogniser
import face_trainer

class Vision:

    def __init__(self, cv2, db):
        self.recogniser = face_recogniser.Recogniser(cv2, db)
        self.trainer = face_trainer.Trainer(cv2, db)
        self.cv2 = cv2
        self.db = db
        self.video = cv2.VideoCapture(0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.recognition_threshold = 60
        self.user_list = None
        self.training_enabled = False
        self.trainer.train()

    def call(self):
        ret, self.frame = self.video.read()
        faces = self.faces()
        return (self.frame, faces)

    def faces(self):
        faces = self.recogniser.call(self.frame)
        for (x, y, w, h, id, confidence) in faces:
            if(int(confidence) > self.recognition_threshold):
                name = self.name(id)
                color = (0,255,0)
            else:
                name = 'probably '+self.name(id)
                color = (0,0,255)
                if(self.training_enabled):
                    self.train_face((x, y, w, h))

            self.render_text(str(name), x, y-10, color)
            self.render_text(str(confidence), x, y+h+30, color)
        return faces

    def name(self, id):
        if(len(self.users()) <= id):
            return 'not in db: ' + str(id)
        return self.users()[id]

    def users(self):
        if(self.user_list != None):
            return self.user_list

        users = {}
        for (id, name, permissions, last_seen_at) in self.db.all('users'):
            users[id] = name
        self.user_list = users
        print('[INFO] Users set')
        print(users)
        return users

    def train_face(self, face):
        self.trainer.call(self.frame, face)

    def train(self):
        self.trainer.train()

    def render_text(self, text, x, y, color):
        self.cv2.putText(self.frame, text, (x,y), self.font, 1, color, 1)

    def stop(self):
        self.video.release()

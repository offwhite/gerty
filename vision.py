# on call, read the view, detect and recognise faces, return frame
import face_detector
import face_recogniser
import face_trainer

class Vision:

    def __init__(self, cv2):
        self.detector = face_detector.Detector(cv2)
        self.recogniser = face_recogniser.Recogniser(cv2)
        self.trainer = face_trainer.Trainer(cv2)
        self.cv2 = cv2
        self.video = cv2.VideoCapture(0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.recognition_threshold = 45
        self.names = ['James','Dave','?','?','?']

    def call(self):
        ret, self.frame = self.video.read()
        self.faces = self.detector.call(self.frame, True)
        recognised_faces = self.recognise_faces()
        return (self.frame, recognised_faces)

    def recognise_faces(self):
        recognised_faces = self.recogniser.call(self.frame, self.faces)
        #print('[INFO] {} faces found  '.format(recognised_faces), end='\r')
        for (x, y, w, h, id, confidence) in recognised_faces:
            if(int(confidence) > self.recognition_threshold):
                name = self.names[id]
                color = (0,255,0)
            else:
                name = 'Unknown'
                color = (0,0,255)
                self.train_face((x, y, w, h), id)

            self.render_text(str(name), x+5, y-5, color)
            self.render_text(str(confidence), x+5, y+h+30, color)
        return recognised_faces

    def train_face(self, face, id):
        self.trainer.call(self.frame, face, id)

    def render_text(self, text, x, y, color):
        self.cv2.putText(self.frame, text, (x,y), self.font, 1, color, 2)

    def stop(self):
        self.video.release()

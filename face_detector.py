
class Detector:
    def __init__(self, cv2):
        self.cv2 = cv2
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    def call(self, frame, mark_faces = False):
        faces = self.detector.detectMultiScale(
            self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2GRAY),
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=self.cv2.CASCADE_SCALE_IMAGE
        )
        if(mark_faces):
            self.mark_faces(faces, frame)
        return faces

    def mark_faces(self, faces, frame):
        for (x, y, w, h) in faces:
            self.cv2.rectangle(frame, (x-1, y-1), (x+w+1, y+h+1), (255, 255, 255), 2)

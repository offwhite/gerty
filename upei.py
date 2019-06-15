

class Upei:
    def __init__(self, cv2):
        self.cv2 = cv2
        self.load_expressions()

    def load_expressions(self):
        self.expressions = {}
        available_expressions = ['cry','confused','happy','look_left',
         'look_right','neutral','sad','surprised',
         'very_happy','very_sad']
        for expression in available_expressions:
            img = self.cv2.imread('unit_primary_emotional_interface/'+expression+'.jpg', 1)
            img = self.cv2.resize(img, (1800, 1125), interpolation = self.cv2.INTER_AREA)
            self.expressions[expression] = img

    def image(self,expression):
        return self.expressions[expression]

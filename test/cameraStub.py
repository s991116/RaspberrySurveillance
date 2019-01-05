import cv2

class CameraStub:
    def __init__(self, images):
        self.imagenames = images
        self.imageNumber = 0

    def warmup(self):
        return

    def getNextImage(self):
        image =  cv2.imread(self.imagenames[self.imageNumber], cv2.IMREAD_UNCHANGED)
        self.imageNumber += 1
        if(len(self.imagenames) == self.imageNumber):
            self.imageNumber = 0
        return image
  
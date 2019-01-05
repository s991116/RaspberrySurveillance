from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import logging
import cv2
import imutils

logger = logging.getLogger(__name__)

class SurveillanceCamera:
    def __init__(self, conf):
        self.conf = conf
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = tuple(conf["resolution"])
        self.camera.framerate = conf["fps"]
        self.rawCapture = PiRGBArray(self.camera, size=tuple(conf["resolution"]))

    def warmup(self):
        # allow the camera to warmup, then initialize the average frame, last
        # uploaded timestamp, and frame motion counter
        logger.info("camera warming up...")
        time.sleep(self.conf["camera_warmup_time"])
    
    def getNextImage(self):
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        frame = self.rawCapture.array
        frame = cv2.flip(frame, -1)            
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        return frame
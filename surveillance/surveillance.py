# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import dropbox
import imutils
import json
import cv2
import logging

logger = logging.getLogger(__name__)

class Surveillance:
    def __init__(self, conf, camera):
        self.min_area = conf["min_area"]
        self.delta_thres = conf["delta_thresh"]
        self.camera = camera
        self.camera.warmup()
        self.avg = None
        logger.info("Surveilance initialized")

    def setBackground(self):
        # for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image and initialize
        # the timestamp and occupied/unoccupied text
        frame = self.camera.getNextImage()

        gray = self._blurImage(frame)

        logger.info("starting background model...")
        self.avg = gray.copy().astype("float")

    def _blurImage(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def detectChange(self):
        # for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image and initialize
        # the timestamp and occupied/unoccupied text
        frame = self.camera.getNextImage()

        gray = self._blurImage(frame)

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, self.delta_thres, 255,
            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        frameChanged = False
        for c in cnts:
            # if the contour is too small, ignore it
            logger.info("Change/contour detected")
            if cv2.contourArea(c) >= self.min_area:
                logger.info("Change/contour bigger than minimum")
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frameChanged = True

        return frameChanged, frame

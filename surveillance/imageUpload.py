import datetime
import cv2
import logging

logger = logging.getLogger(__name__)

class ImageUpload:
    def __init__(self, conf, uploadProvider):
        self.conf = conf
        self.uploadProvider = uploadProvider
        self.lastUploaded = datetime.datetime.now()
        self.motionCounter = 0

    def Upload(self, frame, frameChanged):
        if frameChanged:
            self.timestamp = datetime.datetime.now()
            # check to see if enough time has passed between uploads
            if (self.timestamp - self.lastUploaded).seconds >= self.conf["min_upload_seconds"]:
                logger.info("Time for new upload")
                # increment the motion counter
                self.motionCounter += 1

                # check to see if the number of frames with consistent motion is
                # high enough
                if self.motionCounter >= self.conf["min_motion_frames"]:
                    logger.info("Enough continous frames with changes")
                    # check to see if dropbox sohuld be used
                    try:
                        self.uploadProvider.Upload(frame, self.timestamp)
                    except Exception as e:
                        logger.warning("Unable to upload image. Exception: " + e)

                    # update the last uploaded timestamp and reset the motion
                    # counter
                    self.lastUploaded = self.timestamp
                    self.motionCounter = 0

        # otherwise, the room is not occupied
        else:
            self.motionCounter = 0

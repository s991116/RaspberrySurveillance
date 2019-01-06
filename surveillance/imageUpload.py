import dropbox
import datetime
import cv2
import logging
from pyimagesearch.tempimage import TempImage

logger = logging.getLogger(__name__)

class ImageUpload:
    def __init__(self, conf):
        self.conf = conf
        # check to see if the Dropbox should be used
        if self.conf["use_dropbox"]:
            # connect to dropbox and start the session authorization process
            self.client = dropbox.Dropbox(self.conf["dropbox_access_token"])
            logger.info("Dropbox account linked")
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
                    if self.conf["use_dropbox"]:
                        # write the image to temporary file
                        t = TempImage()
                        cv2.imwrite(t.path, frame)

                        # upload the image to Dropbox and cleanup the tempory image
                        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        logger.info("[UPLOAD] {}".format(ts))
                        path = "/{base_path}/{timestamp}.jpg".format(
                            base_path=self.conf["dropbox_base_path"], timestamp=ts)
                        self.client.files_upload(open(t.path, "rb").read(), path)
                        t.cleanup()
        
                    # update the last uploaded timestamp and reset the motion
                    # counter
                    self.lastUploaded = self.timestamp
                    self.motionCounter = 0

        # otherwise, the room is not occupied
        else:
            self.motionCounter = 0

import dropbox
import cv2
from pyimagesearch.tempimage import TempImage
import logging

logger = logging.getLogger(__name__)

class DropboxProvider:
    def __init__(self, conf):
        self.conf = conf
        # check to see if the Dropbox should be used
        if self.conf["use_dropbox"]:
            # connect to dropbox and start the session authorization process
            self.client = dropbox.Dropbox(self.conf["dropbox_access_token"])
            logger.info("Dropbox account linked")

    def Upload(self, frame, timestamp):
        if self.conf["use_dropbox"]:
            # write the image to temporary file
            t = TempImage()
            cv2.imwrite(t.path, frame)

            # upload the image to Dropbox and cleanup the tempory image
            ts = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            logger.info("[UPLOAD] {}".format(ts))
            path = "/{base_path}/{timestamp}.jpg".format(
                base_path=self.conf["dropbox_base_path"], timestamp=ts)
            self.client.files_upload(open(t.path, "rb").read(), path)
            t.cleanup()

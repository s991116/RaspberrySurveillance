from surveillance.surveillanceCamera import SurveillanceCamera
from surveillance.imageUpload import ImageUpload
from surveillance.dropboxProvider import DropboxProvider
from surveillance.surveillance import Surveillance
from loggingConfig import setup_logging
import argparse
import warnings
import json
import logging

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
ap.add_argument("-l", "--logging", required=False,
	help="path to the YAML loggingconfiguration file")
ap.add_argument("-t", "--token", required=False,
        help="Token for Dropbox upload")
args = vars(ap.parse_args())

if args["logging"] is not None:
	setup_logging(args["logging"])
else:
	setup_logging()
logger = logging.getLogger(__name__)

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

if args["token"] is not None:
	conf["dropbox_access_token"] = args["token"]

camera = SurveillanceCamera(conf)
dropboxProvider = DropboxProvider(conf)
imageUpload = ImageUpload(conf, dropboxProvider)

s = Surveillance(conf, camera)

s.setBackground()

while(True):
	changed, frame = s.detectChange()
	if(changed):
		logger.info("Detected frame change")
		imageUpload.Upload(frame, changed)

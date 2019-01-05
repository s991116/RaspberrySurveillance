from surveillance.surveillanceCamera import SurveillanceCamera
from surveillance.imageUpload import ImageUpload
from surveillance.surveillance import Surveillance
from loggingConfig import setup_logging
import argparse
import warnings
import json
import logging

setup_logging()
logger = logging.getLogger(__name__)

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

camera = SurveillanceCamera(conf)
imageUpload = ImageUpload(conf)
s = Surveillance(conf, camera)

s.setBackground()
while(True):
	changed, frame = s.detectChange()
	if(changed):
		logger.info("Detected frame change")
		imageUpload.Upload(frame, changed)

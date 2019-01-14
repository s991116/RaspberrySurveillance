from surveillance.surveillanceCamera import SurveillanceCamera
from surveillance.imageUpload import ImageUpload
from surveillance.dropboxProvider import DropboxProvider
from surveillance.mongoProvider import MongoProvider
from surveillance.dataUpload import DataUpload

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
args = vars(ap.parse_args())

if args["logging"] is not None:
	print("Loggingfile:" + args["logging"])
	setup_logging(args["logging"])
else:
	setup_logging()
logger = logging.getLogger(__name__)

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

camera = SurveillanceCamera(conf)
mongoProvider = MongoProvider(conf["mongodb_connection"])
dataUpload = DataUpload(mongoProvider)

dropboxProvider = DropboxProvider(conf)
imageUpload = ImageUpload(conf, dropboxProvider, dataUpload)

s = Surveillance(conf, camera)

s.setBackground()
while(True):
	changed, frame = s.detectChange()
	if(changed):
		logger.info("Detected frame change")
		imageUpload.Upload(frame, changed)

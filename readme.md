# Camera Surveillance 
## with Raspberry, OpenCV and Raspberry Camera

To start surveillance: python run_surveillance.py -c conf.json
conf.json is configuration to use.

To run test, from project-folder run: python -m unittest discover -v

Parameters in configurationfile:
{
	"show_video": false,
	"use_dropbox": true,
	"dropbox_access_token": "xxxx",
	"dropbox_base_path": "dropbox path/folder",
	"min_upload_seconds": 3.0,
	"min_motion_frames": 8,
	"camera_warmup_time": 2.5,
	"delta_thresh": 5,
	"resolution": [640, 480],
	"fps": 16,
	"min_area": 500
}

##External modules:
dnspython
pyaml

##Startup script
A template startupscript could look like this

#!/bin/bash
source /home/pi/.virtualenvs/cv/bin/activate
cd /home/pi/projects/RaspberrySurveillance/
python run_surveillance.py -c conf.json -t <Dropbox token>a -l loggingErrorConfig.yaml &

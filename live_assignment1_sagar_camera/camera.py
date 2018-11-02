"""
FILE_NAME: camera.py
TITLE:live  image capturing picamera which accept time interval to  capture image via json file  and  start running at boot
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:17/10/2018 10:00  
DATE_OF_LAST_UPDATION:17/10/2018 14:41 
PYTHON_VERSION:2.7.0
"""
import json
import picamera
import time
from datetime import datetime
import logging
import logging.handlers as handlers


#creating log file
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("camera.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# to open json file to accpet time interval to capture image
try:
	with open("/home/pi/Desktop/live_assignment1/time_interval.json")as interval:
		time_interval_to_cap_picture=json.load(interval)
	sleep_value=time_interval_to_cap_picture["time_to_wait_to_capture_pic"]
except ValueError:
	logger.error("Decoding of json failed")
	print("Decoding of json failed")
	exit()
except FileNotFoundError:
	logger.error("Wrong file or file path provided for json file")
	print("Wrong file or file path")
	exit()
except IOError:
	logger.error("io error occured while reading json file")
	print("io error occured")
	exit()
while 1:
        try:
                with picamera.PiCamera() as camera_object:
                        currenttime=datetime.now()  #to accept todays date in tuple format
                        pic_time=currenttime.strftime("%Y%m%d%H%m%S")  #using strftime function we can modify date time according to need
                        camera_object.resolution=(1280,720)  #set resolutiom
                        camera_object.capture("/home/pi/Desktop/live_assignment1/captured_image/%s_picamera_image.jpg"%str(pic_time)) #captured image and stored it at specified location
                        logger.info("image captured :%s and saved at specified location"%pic_time)
                        print("image captured :%s and saved at specified location"%pic_time)
                time.sleep(sleep_value)  #to wait to complete interval
        except picamera.PiCameraAlreadyRecording:
                logger.error("camera problem raise please check connectivity ,resource etc")
                print("Raised when start_recording() or record_sequence() are called against a port which already has an active recording.")
                exit()
        except picamera.PiCameraRuntimeError:
                logger.error("camera problem raise please check connectivity ,resource etc")
                print("Raised when an invalid sequence of operations is attempted with a PiCamera object.")
                exit()
        except picamera.PiCameraError:
                logger.error("camera problem raise please check connectivity ,resource etc")
                print("pi camera error raised")
                exit()	
        except picamera.PiCameraValueError:
                logger.error("camera problem raise please check connectivity ,resource etc")
                print("invalid value is fed to a PiCamera object.")
                exit() 
        except :
                logger.error("camera problem raise please check connectivity ,resource etc")
                print("camera exception genrated")                
                exit()
		
	

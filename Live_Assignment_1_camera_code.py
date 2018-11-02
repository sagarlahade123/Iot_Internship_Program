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

date=time.strftime("%x")
print(date)

#create log file
logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("/home/pi/Desktop/Bhagyashri/camera/camera.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)



#logging.basicConfig(filename="/home/pi/Desktop/Bhagyashri/Camera_log_file.log",level=logging.INFO,format='%(asctime)s\t%(levelname)s\t%(message)s')


# to open json file to accpet time interval to capture image
try:
	with open("/home/pi/Desktop/Bhagyashri/camera/camera_json_file.json","r")as interval:
		time_interval_to_cap_picture=json.load(interval)
	sleep_value=time_interval_to_cap_picture["camera_time_interval"]
except ValueError:
	logger.error("Reading from json file failed")
	print("Reading from json file failed")
	exit()
except:
	logger.error("Wrong file or file path provided for json file")
	print("Wrong file or file path")
	exit()

while 1:
        try:
                with picamera.PiCamera() as camera_object:
                        #to accept todays date in tuple format
                        currenttime=datetime.now()
                        #using strftime function we can modify date time according to need
                        pic_time=currenttime.strftime("%Y%m%d%H%m%S") 
                        #captured image and stored it at specified location
                        camera_object.capture("/home/pi/Desktop/Bhagyashri/camera/Captured_pics/%s_picamera_image.jpg"%str(pic_time)) 
                        logger.info("Image captured :%s "%pic_time)
                        print("Image captured :%s "%pic_time)
                #to wait to complete interval
                time.sleep(sleep_value)  
  
        except :
                logger.error("Camera problem raise please check connectivity ,resource etc")
                print("Camera exception generated")             
                exit()
		
	

"""
    File name: REST_upload.py
    Program title: Upload data from sqlite to IoT server
    Author: Bhagyashri Patil
    Date created: 24/10/2018
    Date last modified: 1/11/2018
    Python Version: 3.7.0
"""
#import libraries of python
import json
import requests
import sqlite3
import time
import logging
import logging.handlers as handlers


#creating log file
logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("IotSense_REST_Upload.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)





#Infinity loop to continuously upload data from sqlite table of tempreture and pressure sensor
while True:
        #Make connection with database
        connection = sqlite3.connect("Sensor_Data.db")
        logger.info("Connected with database")

        #Make cursor to execute query
        cursur1=connection.cursor()
        cursur1.execute("select * from Table1;")
        rows=cursur1.fetchall()

        connection.close()
        #print(rows)

        for row in rows:
                ID=row[0]
                sensor_name=row[1]
                tempreture=row[2]
                humidity=row[3]
                pressure=row[4]
                date_time=row[5]
                device_id=row[6]
                
                if device_id=="5bcdd46385223831aa13af01":

                        #Dictionary in IoTsense format
                        data_temp_POST={
                                "Device_ID":device_id,
                                "Sensor_Name":sensor_name,
                                "Sensor_value":pressure,
                                "Date_Time":date_time
                                }
                elif device_id=="5bcdd47885223831aa13af02":
                        # Dictionary in IoTsense format
                        data_temp_POST = {
                                "Device_ID": device_id,
                                "Sensor_Name": sensor_name,
                                "Sensor_value": humidity,
                                "Date_Time": date_time

                                }
                elif device_id=="5bcdd43585223831aa13aefc":
                        # Dictionary in IoTsense format
                        data_temp_POST = {
                                "Device_ID": device_id,
                                "Sensor_Name": sensor_name,
                                "Sensor_value": tempreture,
                                "Date_Time": date_time
                                }
                else:
                        print("Not a tempreture,Pressure or Humidity sensor")
                        logger.error("Not a tempreture,Pressure or Humidity sensor")
                        
                data_device_id={"deviceId":device_id}
                data_device_id.__setitem__("data",data_temp_POST)
                print(data_device_id)

                #By loading content from JSON file post data to server
                with open("REST_json.json","r+")as file:
                        data=json.load(file)
                        API_url=data["URL"]
                        print(API_url)
                        try:
                                #Create request to post data
                                request_of_server = requests.post(url = API_url, json=data_device_id)
                                print(request_of_server)
                
                                #If post successfully then delete row and post next
                                if request_of_server.status_code==200:
                                        
                                        connection = sqlite3.connect("Sensor_Data.db")
                                        cursur1=connection.cursor()

                                        cursur1.execute("delete from Table1 where Id=%s"%ID)
                                        connection.commit()
                                        connection.close()
                                        print("Record deleted after upload on IoTsense")
                                        logger.info("Record deleted after upload on IoTsense")
                                        time.sleep(20)
                                        
                        except :
                                print("Failed to process your request")
                                logger.error("Failed to process your request")
                
        connection.close()

                







        
"""
#If there is nothing in database
if rows==None:
        print("Data not available in database")
        logger.info("Data not available in database")
        time.sleep(30)
        exit()
        
print(rows)

#Assign row values to new variables used in dictionary which later uploaded on server
ID=row[0]
sensor_name=row[1]
tempreture=row[2]
humidity=row[3]
pressure=row[4]
date_time=row[5]
device_id=row[6]

if device_id=="5bcdd46385223831aa13af01":

        #Dictionary in IoTsense format
        data_temp_POST={
                "Device_ID":device_id,
                "Sensor_Name":sensor_name,
                "Sensor_value":pressure,
                "Date_Time":date_time
                }
elif device_id=="5bcdd47885223831aa13af02":
        # Dictionary in IoTsense format
        data_temp_POST = {
                "Device_ID": device_id,
                "Sensor_Name": sensor_name,
                "Sensor_value": humidity,
                "Date_Time": date_time

                }
elif device_id=="5bcdd43585223831aa13aefc":
        # Dictionary in IoTsense format
        data_temp_POST = {
                "Device_ID": device_id,
                "Sensor_Name": sensor_name,
                "Sensor_value": tempreture,
                "Date_Time": date_time
                }
else:
        print("Not a tempreture,Pressure or Humidity sensor")
        logger.error("Not a tempreture,Pressure or Humidity sensor")

data_device_id={"deviceId":device_id}
data_device_id.__setitem__("data",data_temp_POST)
print(data_device_id)

#By loading content from JSON file post data to server
with open("sensor_data_json.json","r+")as file:
        data=json.load(file)
        API_url=data["URL"]
        print(API_url)

        try:
                #Create request to post data
                request_of_server = requests.post(url = API_url, json=data_device_id)
                print(request_of_server)
	
                #If post successfully then delete row and post next
                if request_of_server.status_code==200:
                        cursur1.execute("delete from Table1 where Id=%s"%ID)
                        connection.commit()
                        print("Record deleted after upload on IoTsense")
                        time.sleep(20)
        except :
                print("Failed to process your request")
"""

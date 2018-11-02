"""
    File name: humidity.py
    Program title:Take data from SenseHat and pass data to sqlite table of humidity sensor
    Author: Bhagyashri Patil
    Date created: 24/10/2018
    Date last modified: 1/11/2018
    Python Version: 3.7.0
"""

#import libraries of python
import datetime
import json
import sqlite3
import time
import logging
import logging.handlers as handlers
from sense_hat import SenseHat

#Accese data time
date_time=datetime.datetime.utcnow().isoformat()
print(date_time)

#create log file
logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("Device_log.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

#Get humidity data from SenseHat
sense = SenseHat()
sense.clear()
humidity_SenseHat = sense.get_humidity()
print("Humidity from SenseHat:"+str(humidity_SenseHat))

try:
    # Make connection with database
    connection = sqlite3.connect("Sensor_Data.db")
    print("Database created successfully")
    logger.info("Database created successfully")
    #Make cursor
    cur=connection.cursor()
    
except:
    print("Failed to connect to database")
    logger.error("Failed to connect to database")
    connection.close()

try:
    #Read JSON file for deviceID and Interval
    with open("sensor_data_json.json","r")as file:
        data=json.load(file)
        Device_ID_Humidity=data["device_ID3"]
        Interval_for_Humidity=data["interval_for_humidity"]
        print("Device ID of humidity sensore:"+str(Device_ID_Humidity))
        print("Time interval for humudity sensor to sleep:"+str(Interval_for_Humidity))
        print("Inserting sensor data to database table wait for interval time.And check the database")
except:
    print("Failed to read JSON file")
    logger.error("Failed to read JSON file")

#loop for inserting data to sqlite table continuosly according to the interval time
try:
    while True:
            connection = sqlite3.connect("Sensor_Data.db")
            # Make cursor to execute query
            cursur1 = connection.cursor()	
            cursur1.execute("insert into Table1(Sensor_Name ,Tempreture,Humidity ,Pressure ,Date_Time ,Device_id)values(?,?,?,?,?,?)",("Humidity_sensor","NA",humidity_SenseHat,"NA",date_time,Device_ID_Humidity))
            logger.info("Humidity data inserted successfully to database")
            connection.commit()
            cursur1.close()
            connection.close()
            time.sleep(Interval_for_Humidity)
except:
    print("Problem to insert data into table.Check the query")
    logger.error("Problem to insert data into table.Check the query")


        

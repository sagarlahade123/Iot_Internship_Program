"""
    File name: pressure.py
    Program title:Take data from SenseHat and pass data to sqlite table of pressure sensor
    Author: Bhagyashri Patil
    Date created: 24/10/2018
    Date last modified: 25/10/2018
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

#create log file
logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("Device_log.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)



#Get pressure data from SenseHat
sense = SenseHat()
sense.clear()
pressure_Sensehat = sense.get_pressure()
print("Pressure from SenseHat:"+str(pressure_Sensehat))

try:
    # Make connection with database
    connection = sqlite3.connect("Sensor_Data.db")
    #Create table query for sqlite to create table
    sql_query="create table if not exists Table2(Id integer primary key autoincrement,Sensor_Name text,Tempreture int,Humidity real,Pressure int,Date_Time string,Device_id int);"
    print(sql_query)
    cur.execute(sql_query)
    connection.commit()
    
   
except:
    print("Failed to connect to database")
    logger.error("Failed to connect to database")

try:
    #Read JSON file for deviceID and Interval
    with open("MQTT_json.json","r")as file:
        data=json.load(file)
        Device_ID_Pressure=data["device_ID2"]
        Interval_for_Pressure=data["interval_for_pressure"]
        print("Device ID of pressure sensore:"+str(Device_ID_Pressure))
        print("Time interval for pressure sensor to sleep:"+str(Interval_for_Pressure))
        print("Inserting sensor data to database table wait for interval time.And check database")
except:
    print("Failed to read JSON file")
    logger.error("Failed to read JSON file")

#loop for inserting data to sqlite table continuosly according to the interval time
try:
    while True:
            connection = sqlite3.connect("Sensor_Data.db")
            cursur1=connection.cursor()
            cursur1.execute("insert into Table2(Sensor_Name ,Tempreture,Humidity ,Pressure ,Date_Time ,Device_id)values(?,?,?,?,?,?)",("Pressure_sensor","NA","NA",pressure_Sensehat,date_time,Device_ID_Pressure))
            logger.info("Data inserted successfully")
            connection.commit()
            cursur1.close()
            connection.close()
            time.sleep(Interval_for_Pressure)
except:
    print("Problem to insert data into table.Check the query")
    logger.error("Problem to insert data into table.Check the query")
	

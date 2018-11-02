"""
    File name: Tempreture.py
    Program title:Take data from SenseHat and pass data to sqlite table of tempreture sensor
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


#create log file
logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("Device_log.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


#Log_Filename = "Device_log.log"
#logging.basicConfig(filename=Log_Filename,level=logging.INFO)


#Accese data time
date_time=datetime.datetime.utcnow().isoformat()
print(date_time)

#Make connection with database
connection = sqlite3.connect("Sensor_Data.db")
print("Database created successfully")
cur=connection.cursor()

Sensor_Name="Tempreture Sensor"
#Get tempreture data from SenseHat
sense = SenseHat()
sense.clear()
tempreture_Sensehat = sense.get_temperature()
print("Tempreture from SenseHat:"+str(tempreture_Sensehat))


try:

    #Create table query for sqlite to create table
    sql_query="create table if not exists Table1(Id integer primary key autoincrement,Sensor_Name text,Tempreture int,Humidity real,Pressure int,Date_Time string,Device_id int);"
    print(sql_query)
    cur.execute(sql_query)
    connection.commit()
    print("Table created successfully")
    logger.info("Table created successfully")
except:
    print("Problem while creating table.Please check syntax")
    logger.error("Problem while creating table.Please check syntax")
    connection.close()
try:
    #Read JSON file
    with open("sensor_data_json.json","r")as file:
        data=json.load(file)
        Device_ID_Temp=data["device_ID1"]
        Interval_for_Tempreture =data["interval_for_tempreture"]
        print("Device ID of Tempreture sensore:"+str(Device_ID_Temp))
        print("Time interval for tempreture sensor to sleep:" + str(Interval_for_Tempreture))
        print("Inserting sensor data to database table wait for interval time.And check database")
except:
    print("Failed to read JSON file content")
    logger.error("Failed to read JSON file content")
#loop for inserting data continuously accorting to interval time
try:
    while True:
        connection = sqlite3.connect("Sensor_Data.db")
        #Make cursor to execute query
        cursur1=connection.cursor()
        cursur1.execute("insert into Table1(Sensor_Name ,Tempreture,Humidity ,Pressure ,Date_Time ,Device_id)values(?,?,?,?,?,?)",(Sensor_Name,tempreture_Sensehat,"NA","NA",date_time,Device_ID_Temp))
        logger.info("Tempreture data inserted successfully to database")
        connection.commit()
        cursur1.close()
        connection.close()
        time.sleep(Interval_for_Tempreture)

       
    
except:
    print("Problem to insert data into table.Check the query")
    logger.error("Problem to insert data into table.Check the query")



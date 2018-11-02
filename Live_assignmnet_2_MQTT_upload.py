"""
    File name: MQTT_upload.py
    Program title: Upload data from sqlite to IoT server
    Author: Bhagyashri Patil
    Date created: 24/10/2018
    Date last modified: 2/11/2018
    Python Version: 3.7.0
"""
#import libraries of python
import json
import requests
import sqlite3
import time
import logging
import logging.handlers as handlers
import paho.mqtt.client as mqtt

#define host URL and port of server
host="iotsense.centralindia.cloudapp.azure.com"
port=1883
topic="/api/dump"
data_upload={}

#create MQTT client
client_tempreture =mqtt.Client("5bdbfb6b85223831aa178030")
client_pressure =mqtt.Client("5bdc10d385223831aa1780d9")
client_humidity=mqtt.Client("5bdc330a85223831aa1781f1")



#creating log file
logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("IotSense_MQTT_Upload.log",when='midnight',interval=1)
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
        cursur1.execute("select * from Table2;")
        rows=cursur1.fetchall()
        if not rows:
                print("Database is empty please insert data first to upload")
                logger.info("Database is empty please insert data first to upload")
                connection.close()
                exit()

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
                
                        
                        
                if device_id=="5bdc10d385223831aa1780d9":
                        #Dictionary in IoTsense format
                        data_upload={
                                "Device_ID":device_id,
                                "Sensor_Name":sensor_name,
                                "Sensor_value":pressure,
                                "Date_Time":date_time
                                }
                elif device_id=="5bdc330a85223831aa1781f1":
                        # Dictionary in IoTsense format
                        data_upload= {
                                "Device_ID": device_id,
                                "Sensor_Name": sensor_name,
                                "Sensor_value": humidity,
                                "Date_Time": date_time
                                }
                elif device_id=="5bdbfb6b85223831aa178030":
                        # Dictionary in IoTsense format
                        data_upload= {
                                "Device_ID": device_id,
                                "Sensor_Name": sensor_name,
                                "Sensor_value": tempreture,
                                "Date_Time": date_time
                                }
                else:
                        
                        print("Not a tempreture,Pressure or Humidity sensor")
                        logger.error("Not a tempreture,Pressure or Humidity sensor")
                        
                #convert data to string using dumps() function for upload
                Data_MQTT_upload=json.dumps(data_upload)

                #By loading content from JSON file post data to server
                with open("MQTT_json.json","r+")as file:
                        data=json.load(file)
                        API_url=data["URL"]
                        #print(API_url)
                    
                        try:
                                if device_id=="5bdbfb6b85223831aa178030":
                                        #create connection with client
                                        client_tempreture.connect(host,port)
                                        #publish data to IoTsense
                                        result_publish=client_tempreture.publish(topic,Data_MQTT_upload)
                                        print("Tempreture data published to topic successfully")
                                        logger.info("Tempreture data published to topic successfully")
                                        #If upload successfully then delete row and post next
                                        if result_publish.is_published()==True:
                                                connection = sqlite3.connect("Sensor_Data.db")
                                                cursur1=connection.cursor()
                                                cursur1.execute("delete from Table2 where Id=%s"%ID)
                                                connection.commit()
                                                connection.close()
                                                print("Record deleted after upload on IoTsense")
                                                logger.info("Record deleted after upload on IoTsense")
                                                time.sleep(20)
                                elif device_id=="5bdc10d385223831aa1780d9":
                                        #creat connection with client
                                        client_pressure.connect(host,port)
                                        #publish data to IoTsense
                                        result_publish=client_pressure.publish(topic,Data_MQTT_upload)
                                        print("Pressure data published to topic successfully")
                                        logger.info("Pressure data published to topic successfully")
                                        #If upload successfully then delete row and post next
                                        if result_publish.is_published()==True:
                                                connection = sqlite3.connect("Sensor_Data.db")
                                                cursur1=connection.cursor()
                                                cursur1.execute("delete from Table2 where Id=%s"%ID)
                                                connection.commit()
                                                connection.close()
                                                print("Record deleted after upload on IoTsense")
                                                logger.info("Record deleted after upload on IoTsense")
                                                time.sleep(20)
                                            
                                elif device_id=="5bdc330a85223831aa1781f1":
                                        #creat connection with client
                                        client_humidity.connect(host,port)
                                        #publish data to IoTsense
                                        result_publish=client_humidity.publish(topic,Data_MQTT_upload)
                                        print("Humidity data published to topic successfully")
                                        logger.info("Humidity data published to topic successfully")
                                        #If upload successfully then delete row and post next
                                        if result_publish.is_published()==True:
                                                connection = sqlite3.connect("Sensor_Data.db")
                                                cursur1=connection.cursor()
                                                cursur1.execute("delete from Table2 where Id=%s"%ID)
                                                connection.commit()
                                                connection.close()
                                                print("Record delete after upload on IoTsense")
                                                logger.info("Record deleted after upload on IoTsense")
                                                time.sleep(20)
                                else:
                                        print("Not a tempreture,Pressure or Humidity sensor")
                                        logger.error("Not a tempreture,Pressure or Humidity sensor")

                        except :
                             
                                print("Failed to process your request")
                                logger.error("Failed to process your request")
                
        connection.close()

                








"""
FILE_NAME:upload.py
TITLE:upload data present in sqlite database to iot sense
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:24/10/2018 10:00  AM
DATE_OF_LAST_UPDATION:24/10/2018 12:28 PM
PYTHON_VERSION:3.7.0
"""
import  datetime
import sqlite3
import  json
import time
import logging
import traceback
import logging.handlers as handlers
import paho.mqtt.client as mqtt

#creating log file
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("IotSense_upload.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
#creating boolean variable to keep traack weather database is connected or not
sqlite_connection=False


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

#reading url to upload from json file
try:
    with open("devicedata.json") as json_data:
        jsondata=json.load(json_data)
        url_to_upload=jsondata["url"]
except:
    logger.info("error while reading json file")
    print("error while reading json file")

#inserting all rows from sqlite db to their specified device on iotsense gateway
while True:
        #making connection with sqlite database
    try:
        connection = sqlite3.connect("PracticeDb.db")
        logger.info("connection to sqlite completed")
        print("made connection to sqlite db")
        sqlite_connection=True
        cursor1 = connection.cursor()
    except:
        logger.info("error while making sqlite connection")
        print("error while making sqlite connection ")

    try:
        #fetching data from sqlite db to send
        number_of_row_query="select count(*) from sensordata"
        cursor1.execute(number_of_row_query)
        result_of_number_of_row_query=cursor1.fetchone()
        number_of_row=result_of_number_of_row_query[0]
        print(number_of_row)
        if number_of_row==0:
            print("no data to upload")
            logger.info("No data to upload")
            connection.close()
            sqlite_connection=False
            print("sqlite connection closed")
            logger.info("sqlite connection closed")
            time.sleep(30)
            continue

        sql_query="select * from sensordata"
        cursor1.execute(sql_query)
        data=cursor1.fetchall()  #data will contain all rows of sqlite database
        try:
            #sending rows to iotsense gateway
            while True:
                for data_to_send in data:
                    print(data_to_send)
                    row_id=data_to_send[0]
                    sensor_name=data_to_send[1]
                    sensor_value=data_to_send[2]
                    humidity=data_to_send[3]
                    date_and_time=data_to_send[4]
                    deviceId=data_to_send[5]

                    if humidity=="NA":
                        data_of_sensor={
                                            "sensor_name":sensor_name,
                                            "sensor_value":sensor_value,
                                            "date_and_time":date_and_time
                                        }
                    else:
                        data_of_sensor={
                                            "sensor_name":sensor_name,
                                            "humidity":humidity,
                                            "date_and_time":date_and_time
                                        }
                    data_to_iotsense=json.dumps(data_of_sensor)
                    while True:
                        
                        
                            if sqlite_connection==True:
                                #making mqtt client reference
                                client = mqtt.Client(deviceId)
                                client.on_connect = on_connect
                                #connecting to iotsense using mqtt
                                client.connect(url_to_upload, 1883, 60)

                                result_of_publish=client.publish("/api/dump", data_to_iotsense)
                                client.loop()
                                if result_of_publish.is_published() == True:
                                    print("row id: %d data sent successfully"%row_id)
                                    logger.info("row id: %d data sent successfully to iot sense gateway"%row_id)
                                    delete_query="delete from sensordata where id=%s"%row_id
                                    cursor1.execute(delete_query)
                                    connection.commit()
                                    print("row id: %d data deleted successfully"%row_id)
                                    logger.info("row id: %d data deleted successfully"%row_id)
                                    connection.close()
                                    logger.info("sqlite connection clolsed")
                                    print("sqlite connection clolsed")
                                    sqlite_connection=False
                                    time.sleep(2)  #interval to upload
                                    break
                                else:
                                    print("mqtt send fail... so goes into sleep for 30 sec")
                                    logger.info("mqtt send fail... so goes into sleep for 30 sec")
                                    connection.close()
                                    logger.info("sqlite connection clolsed")
                                    print("sqlite connection clolsed")
                                    sqlite_connection=False
                                    time.sleep(30)
                                    print("starting another attempt to send data ")
                                    logger.info("starting another attempt to send data")
                                    continue
                            else:
                                #making connection with sqlite database
                                try:
                                    connection = sqlite3.connect("PracticeDb.db")
                                    logger.info("connection to sqlite completed")
                                    print("made connection to sqlite db")
                                    sqlite_connection=True
                                    cursor1 = connection.cursor()
                                    continue
                                except:
                                    logger.info("error while making sqlite connection")
                                    print("error while making sqlite connection ")
                        
                break        
        except:
            print("exception genrated while data sending towards iotsense gateway:")
            logger.error("exception genrated while data sending towards iotsense gateway:")
            print(traceback.format_exc())
    except:
        print("exception genrated in main logic:")
        logger.error("exception genrated")
        print(traceback.format_exc())
        
     

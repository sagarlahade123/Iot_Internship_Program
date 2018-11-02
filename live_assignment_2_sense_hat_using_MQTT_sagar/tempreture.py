"""
FILE_NAME:tempreture.py
TITLE:send tempreture data to iot sense with fixed interval of time
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:24/10/2018 10:00  AM
DATE_OF_LAST_UPDATION:24/10/2018 12:28 PM
PYTHON_VERSION:3.7.0
"""
import  datetime
import sqlite3
import  json
import time
from sense_hat import SenseHat
import logging
import logging.handlers as handlers

#creating sensehat reference
sense=SenseHat()
#creating log file
logger=logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("IotSense.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
current_date=datetime.datetime.utcnow().isoformat()
#reading tempreture sensor device id and its interval from json file
try:
    with open("devicedata.json") as json_data:
        jsondata=json.load(json_data)
        device_id=jsondata["tempreture_device_id"]
        interval=jsondata["tempreture_time_interval"]
except:
    logger.info("error while reading json file")
    print("error while reading json file")

#inserting tempreture data to sqlite db with fixed interval
while True:
    #making connection with sqlite database
    try:
        connection = sqlite3.connect("PracticeDb.db")
        cursor1=connection.cursor()
    except:
        logger.info("error while making sqlite connection")
        print("error while making sqlite connection ")
    try:
        temperature=round(sense.get_temperature(),2)
        tuple_data=("tempreture_sensor",temperature,"NA",current_date,device_id)
        print(tuple_data)
        insert_query="insert into sensordata(sensor_name,sensor_value,humidity,date,deviceid) values(?,?,?,?,?) "
        cursor1.execute(insert_query,tuple_data)
        connection.commit()
        cursor1.execute("select max(id) from sensordata")
        row_id=cursor1.fetchone() #fetchone function return result in tuple format
        row_id=row_id[0]
        print(row_id)
        logger.info("row id: %d tempreture  data:%s inserted"%(row_id,temperature))
        print("row id:%d  tempreture data:%s inserted"%(row_id,temperature))
        connection.close()
        time.sleep(interval)
    except:
        logger.error("error while inserting tempreture data")
        print("error while inserting tempreture data")

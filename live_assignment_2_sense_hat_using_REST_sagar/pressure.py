"""
FILE_NAME:pressure.py
TITLE:send pressure data to iot sense with fixed interval of time
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:24/10/2018 10:00  AM
DATE_OF_LAST_UPDATION:24/10/2018 12:28 PM
PYTHON_VERSION:3.7.0
"""
from  sense_hat import SenseHat 
import  datetime
import sqlite3
import  json
import time
import logging
import logging.handlers as handlers

#creating log file
logger=logger=logging.getLogger("log")
logger.setLevel(logging.INFO)
logHandler=handlers.TimedRotatingFileHandler("IotSense.log",when='midnight',interval=1)
logHandler.setLevel(logging.INFO)
formatter =logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

#taking reference of SenseHat
sense=SenseHat()
current_date=datetime.datetime.utcnow().isoformat()
#reading pressure device id and pressure insert interval
try:
    with open("devicedata.json") as json_data:
        jsondata=json.load(json_data)
        device_id=jsondata["pressure_device_id"]
        interval=jsondata["pressure_time_interval"]
except:
    logger.info("error wjile reading json file in pressure.py")
    print("error wjile reading json file in pressure.py")


#inserting pressure data into sqlite table  with fixed interval
while True:
    #making connection and creating table
    try:
        connection = sqlite3.connect("PracticeDb.db")
        cursor1=connection.cursor()
        sql_query="create table if not exists sensordata(id integer primary key autoincrement,sensor_name text,sensor_value real,humidity real,date text,deviceid text )"
        cursor1.execute(sql_query)
        connection.commit()
    except:
        logger.info("error while creating table or making connection to sqlite")
        print("error while creating table or making connection to sqlite")
    try:
        pressure=round(sense.get_pressure(),2)
        tuple_data=("pressure_sensor",pressure,"NA",current_date,device_id)
        print(tuple_data)
        insert_query="insert into sensordata(sensor_name,sensor_value,humidity,date,deviceid) values(?,?,?,?,?) "
        cursor1.execute(insert_query,tuple_data)
        connection.commit()
        cursor1.execute("select max(id) from sensordata")
        row_id=cursor1.fetchone() #fetchone function return result in tuple format
        row_id=row_id[0]
        print(row_id)
        logger.info("row id: %d pressure  data:%s inserted"%(row_id,pressure))
        print("row id:%d  pressure data:%s inserted"%(row_id,pressure))
        connection.close()
        time.sleep(interval)
    except:
        logger.error("error while inserting pressure data")
        print("error while inserting pressure data")



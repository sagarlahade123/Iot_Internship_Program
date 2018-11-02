"""
    File name: SQLITE_JASON_FILE.py
    Program title: Read data from sqlite DB and generate JSON file
    Author: Bhagyashri Patil
    Date created: 8/10/2018
    Date last modified: 10/10/2018
    Python Version: 3.7.0
"""

#Import libaries
import sqlite3
import json
import openpyxl
from openpyxl import load_workbook

try:
    # Connecting to sqlite database
    connection = sqlite3.connect("SensorData.db")

    # loading excel workbook
    workbook = load_workbook("workBook2.xlsx")

    #getting all sheet names present in workbook into sheet_name_reference
    sheet_name = workbook.get_sheet_names()  # to use in next function

    #creating cursor to execute query
    cursor_ = connection.cursor()

    #following query will give number of rows present in database
    cursor_.execute("select count(*) from %s " % sheet_name[0])
    result_row_query = cursor_.fetchone()  #fetch row one by one
    number_of_rows = result_row_query[0]  # to get only count of rows result_row_query[0]
    print( number_of_rows )

    dictionary = {}
    counter = 1                 #counter for JSON file name

    #following query will give all rows present in database
    cursor_.execute("select * from %s " % (sheet_name[0])+"limit 5")
    for i in range(number_of_rows):

        result_select_query = cursor_.fetchone()  # getting one by one all rows
        row_item_index = 1 #to iterate over each row element
        #print(cursor_.description)
        for column_name in cursor_.description:  # contains all column names
            if column_name[0] != "ID":
                dictionary[column_name[0]] = result_select_query[row_item_index]
                row_item_index = row_item_index + 1

        with open("SQL_JSON%d.json" %counter, "w+") as JsonFile:
            json.dump(dictionary, JsonFile, indent=2)
        counter = counter+ 1

#code for exception handling
except FileNotFoundError:
    print("Wrong file or file path is given. please enter correct excel file name along with its path")
except RuntimeError:
    print("some software or hardware problem arises in system ")
except Exception:
    pass
   #print("database can be empty,please check it ")
else:
    print("program executed successfully")
finally:
    connection.close()

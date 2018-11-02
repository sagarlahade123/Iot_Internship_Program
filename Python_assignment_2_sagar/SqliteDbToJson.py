"""
FILE_NAME:SqliteDbToJson.py
TITLE:CREATING JSON FILES FOR EACH ROW PRESENT IN SQLITE DATABASE
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:09/10/2018 10:00 AM
DATE_OF_LAST_UPDATION:10/10/2018 10:28 AM
PYTHON_VERSION:3.7.0
"""
import sqlite3
import json
import openpyxl
from openpyxl import load_workbook

try:
    # Connecting to sqlite database
    connection = sqlite3.connect("C:/Users/Admin/Desktop/PythonAssignment2/DataBase/SensorData.db")
    # loading excel workbook
    workbook = load_workbook("C:/Users/Admin/Desktop/PythonAssignment2/ExcelSheetToAcceptData/sensordata.xlsx")
    #getting all sheet names present in workbook into sheet_name_reference
    sheet_name_reference = workbook.get_sheet_names()  # to use in next function
    #creating cursor toexecute query
    cursor_ = connection.cursor()
    #following query will give number of rows present in database
    cursor_.execute("select count(*) from %s " % sheet_name_reference[0])
    result_of_count_of_row_query = cursor_.fetchone()  # cursor.fetchone() return number of rows in database in tuple format like(4,)
    number_of_rows = result_of_count_of_row_query[0]  # to get only count of rows result_of_count_of_row_query[0]
    dictionary_To_Create_Json_File = {}
    counter_to_append_with_json_File_Name = 1
    #following query will give all rows present in database
    cursor_.execute("select * from %s " % (sheet_name_reference[0]))
    for i in range(number_of_rows):

        result_of_select_query = cursor_.fetchone()  # getting one by one all rows present in database
        row_element_index = 1 #to iterate over each row element
        FileNameToWrite = "json" + str(counter_to_append_with_json_File_Name)
        for column_name in cursor_.description:  # return all column names at index 0
            if column_name[0] != "ID":
                dictionary_To_Create_Json_File[column_name[0]] = result_of_select_query[row_element_index]
                row_element_index = row_element_index + 1
        "following line will  open file in W+ mode if not exist creates automatically"
        with open("C:/Users/Admin/Desktop/PythonAssignment2/OutputJsonFiles/%s.json" % FileNameToWrite, "w+") as JsonFile:
            json.dump(dictionary_To_Create_Json_File, JsonFile, indent=2)
        counter_to_append_with_json_File_Name = counter_to_append_with_json_File_Name+ 1
except FileNotFoundError:
    print("Wrong file or file path is given. please enter correct excel file name along with its path")
else:
    print("program executed successfully")
finally:
    connection.close()
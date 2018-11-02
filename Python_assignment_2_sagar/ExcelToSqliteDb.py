"""
FILE_NAME:ExcelToSqliteDb.py
TITLE:CREATING SQLITE DATABASE FROM GIVEN EXCEL WORKBOOK
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:09/10/2018 10:00 AM
DATE_OF_LAST_UPDATION:10/10/2018 10:28 AM
PYTHON_VERSION:3.7.0
"""
import sqlite3
import openpyxl
from openpyxl import load_workbook
import re

try:
    flag_to_avoid_first_row=0
    # Connecting to sqlite database
    connection = sqlite3.connect("C:/Users/Admin/Desktop/PythonAssignment2/DataBase/SensorData.db")

    """this Validate function will convert invalidate string into valid sql string ,which we will used while creating database and 
       while inserting data into the sdatabase 
    """
    def validate(text_to_validate, lower=1):

        text_to_validate = str(text_to_validate)
        if lower == 1 and text_to_validate != None:
            text_to_validate = text_to_validate.strip().lower()#strip functio is used to remove frontspace and backspace attached to string and lower to convert it into lowercase
            text_to_validate = re.sub(r'[^\w _-]+', '', text_to_validate) #regular expression to catch except a-z A-Z 0-9 and _characters and convert it into ''
            text_to_validate = re.sub(r'[- ]+', '_', text_to_validate)#regular expression to catch all space and underscore and replace it with underscore
        return text_to_validate

    # loading excel workbook
    workbook = load_workbook("C:/Users/Admin/Desktop/PythonAssignment2/ExcelSheetToAcceptData/sensordata.xlsx")
    #getting all sheet names present in workbook into sheets
    sheets = workbook.get_sheet_names()
    # Creating tables from excel sheets ,first row as a column name
    for sheet in sheets:
        worksheet = workbook[sheet] #loading worksheets one by one
        COLUMNS = [] #this COLUMNS list is used to store all column names, which are created from first row of excel sheet
        create_table_query = 'CREATE TABLE  IF NOT EXISTS ' + str(validate(sheet)) + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
        """
        Following for loop is used to complete create table query
        """
        for row in next(worksheet.rows):
            create_table_query += ', ' + validate(row.value) + ' REAL'
            COLUMNS.append(validate(row.value))#append one by one all columns to COLUMNS list
        create_table_query += ');'#create table query is completed
        connection.execute(create_table_query)#create table query get executed here
        list_to_create_tuple = []#this list_to_create_tuple list is used to store entire sheet rows , each row as a tuple
        # inserting entire sheet into list_to_create_tuple list as a tuple
        for rows in worksheet:
            if flag_to_avoid_first_row==0:
                flag_to_avoid_first_row=1
                continue
            tuple_row=[]#to store entire row as a list elements to tuple_row
            for row in rows:
                tuple_row.append(str(row.value).strip()) if str(row.value).strip() != 'None' else tuple_row.append('')
            list_to_create_tuple.append(tuple(tuple_row))#append entire row as a tuple to list_to_create_tuple as a list element
        #Following insert_query1 and insert_query2 is used create 'insert' statement
            insert_query1 = 'INSERT INTO ' + str(validate(sheet)) + '('
            insert_query2 = ''
        #Following for loop is used to complete insert query statement

        for column in COLUMNS:
            insert_query1 += column + ', '
            insert_query2 += '?, '
        insert_query1 = insert_query1[:-2] + ') VALUES(' #insert_query1[:-2] is used to remove extra comma and space
        insert_query2 = insert_query2[:-2] + ')' #insert_query2[:-2] is used to remove extra comma and space
        insQuery = insert_query1 + insert_query2#query get prepred here
        connection.executemany(insQuery, list_to_create_tuple)# executing insert query on many rows which are stored in list_to_create_tuple
        connection.commit()#to apply modification on sqlite database

except FileNotFoundError:
    print("Wrong file or file path is given. please enter correct excel file name along with its path")
else:
    print("program executed successfully")
finally:
    connection.close()
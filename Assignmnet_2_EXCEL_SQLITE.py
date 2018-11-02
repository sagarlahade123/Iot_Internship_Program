"""
    File name: EXCEL_SQLITE_FILE.py
    Program title: Read data from excel file save into sqlite DB
    Author: Bhagyashri Patil
    Date created: 8/10/2018
    Date last modified: 10/10/2018
    Python Version: 3.7.0
"""
#Import libraries
import sqlite3
import openpyxl
from openpyxl import load_workbook
import re



# This validate function will convert invalidate string into valid sql string ,which we will used while creating database and
# while inserting data into the sdatabase
def validate(text_to_validate, lower=1):
    text_to_validate = str(text_to_validate)
    if lower == 1 and text_to_validate != None:
        text_to_validate = text_to_validate.strip().lower()
        text_to_validate = re.sub(r'[^\w _-]+', '',
                                  text_to_validate)  # regular expression to catch except a-z A-Z 0-9 and _characters and convert it into ''
        text_to_validate = re.sub(r'[- ]+', '_',
                                  text_to_validate)  # regular expression to catch all space and dash and replace it with underscore
    return text_to_validate




try:
    # Connecting to sqlite database
    connection = sqlite3.connect("SensorData.db")


    flag=0

    # loading excel workbook
    workbook = load_workbook("workBook2.xlsx")

    #getting all sheet names present in workbook into sheets
    sheets = workbook.get_sheet_names()

    # Creating tables from excel sheets ,first row as a column name
    for sheet in sheets:
        worksheet = workbook[sheet] #loading worksheets one by one
        COLUMNS = [] #It used to strore all coumn name
        create_table= 'CREATE TABLE  IF NOT EXISTS ' + str(validate(sheet)) + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'


       #Loop for create table query
        for row in next(worksheet.rows):
            create_table+= ', ' + validate(row.value) + ' int'
            COLUMNS.append(validate(row.value))#append one by one all columns to COLUMNS list
        create_table += ');'
        connection.execute(create_table)
        row_tuple_list = [] #this list use to store the rows of sheet

        # inserting entire sheet into list_to_create_tuple list as a tuple
        for rows in worksheet:
            if flag==0:
                flag=1
                continue
            tuple_row=[]#to store entire row as a list elements to tuple_row
            for row in rows:
                tuple_row.append(str(row.value).strip()) if str(row.value).strip() != 'None' else tuple_row.append('')
            row_tuple_list.append(tuple(tuple_row))#append entire row as a tuple to list_to_create_tuple as a list element

        #Following insert_query1 and insert_query2 is used create 'insert' statement
            insert_query1 = 'INSERT INTO ' + str(validate(sheet)) + '('
            insert_query2 = ''

        #Following for loop is used to complete insert query statement
        for column in COLUMNS:
            insert_query1 += column + ', '
            insert_query2 += '?, '
        insert_query1 = insert_query1[:-2] + ') VALUES(' #insert_query1[:-2] is used to remove extra comma and space
        insert_query2 = insert_query2[:-2] + ')'         #insert_query2[:-2] is used to remove extra comma and space
        insQuery = insert_query1 + insert_query2

        connection.executemany(insQuery, row_tuple_list)# executing insert query on many rows which are stored in list_to_create_tuple
        print(row_tuple_list)
        #make finalchnges to DB
        connection.commit()

#code for exception handling
except FileNotFoundError:
    print("Wrong file or file path is given. please enter correct excel file name along with its path")
except RuntimeError:
    print("some problem arises in system ")
except Exception:
    print(" table/database already exists in database ")
else:
    print("program executed successfully")
finally:
    connection.close()

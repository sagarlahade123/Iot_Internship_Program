"""
    File name: EXCEL_file.py
    Program title: Read data from excel file perform calculations and generate new excel file
    Author: Bhagyashri Patil
    Date created: 4/10/2018
    Date last modified: 5/10/2018
    Python Version: 3.7.0
"""

#Importing the required libraries
import xlrd
import json
import xlwt


#Create new excel file
wb=xlwt.Workbook()
New_Sensore_Data=wb.add_sheet("New_Sensore_Sheet")

#Open the excel file
workbook=xlrd.open_workbook("workbook.xlsx")

#Open the sheet
worksheet=workbook.sheet_by_name("SensorSheet")

#Extract value of perticular cell in sheet
print("Value at row 3 and column 10:{0}".format(worksheet.cell(2,9).value))

#Print available sheets in excel file
sheet_count=workbook.nsheets
print("The total no. of sheets available in excel file are :{0}".format(sheet_count))

#To print the total rows and columns in table
print("Total no of rows in table are :{0}\nTotal no of columns in table are :{0}".format(worksheet.nrows,worksheet.ncols))

#Load the JSON file
with open("excel_JSON_file.json","r+") as file:
   JSON_data=json.load(file)
   file.seek(0)
   #print(file.read())
column = worksheet.row_values(0, 0,None)
print(column)
col=0
for i in column:
    print(i)
    New_Sensore_Data.write(0,col,i)
    col=col+1

#Logic for accept value from excel sheet calculate new value and put it in new sheet
for p in range(0,10):
    sensor_key="sensor"+str(p+1)
    print(sensor_key)
    #New_Sensore_Data.write()
    if JSON_data[sensor_key][0]==1:
        for k in range(1,worksheet.nrows):
            z=worksheet.cell_value(k,p)
            y=JSON_data[sensor_key][1]
            m=JSON_data[sensor_key][2]
            new_value=(z*y)+m
            #print(new_value)
            print("New_Sensore_Value :"+str(new_value))

            New_Sensore_Data.write(k, p, new_value)
            wb.save("workbook1.xls")

    else:
        print("No change sensor data keep as it is.")
        for k in range(1, worksheet.nrows):
            z = worksheet.cell_value(k,p)
            new_value=z
            #print(new_value)
            New_Sensore_Data.write(k, p, new_value)
            wb.save("workbook1.xls")
"""
 File name: Fibonnaci_Sequence.py
    Program title: Generate fibonnaci series of user required elements
    Author: Bhagyashri Patil
    Date created: 11/10/2018
    Date last modified: 11/10/2018
    Python Version: 3.7.0
"""

#Initialise the varianles required
num1=1
num2=1
count=0
Series_Length=input("Enter the length up to which you want fibonnaci series:")


#Loop o print fibonnaci series
while int(count)<int(Series_Length):
    print(str(num1), end='  \n')
    num3 = num1 + num2
    #Update values
    num1 = num2
    num2 = num3
    count += 1

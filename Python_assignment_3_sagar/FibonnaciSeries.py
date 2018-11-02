"""
FILE_NAME:FibonnaciSeries.py
TITLE:This program accept number of elements user want in Fibonnaci Series and genrate Fibonnaci series Which Contain number of elements Specified by user
DEVLOPED_BY:sagar
DATE_OF_CREATION:11/10/2018 11:20 AM
DATE_OF_LAST_UPDATION:11/10/2018 11:57 AM
PYTHON_VERSION:3.7.0
"""
#Following Line accept Number Of Elements user want in his Fibonnaci series
number_of_elements_in_series=int(input("Enter number of elements you want in series:\t"))
"""
Following fibonnaci_series_genretor function accept index of Fibonnaci series Element ang genrate that Fibonnaci element and returns it  
"""
def fibonnaci_series_genretor(element):
    if element==1 or element==2:#as first two element of Fibonnaci Series are one
        return 1
    else:
        return fibonnaci_series_genretor(element-1)+fibonnaci_series_genretor(element-2)#this line get last two element from series and add's them and return it as a current element
for index_of_element in range(1,number_of_elements_in_series+1):#this loop runs upto the number of element user want in his Fibonnaci series
    print(str(fibonnaci_series_genretor(index_of_element))+"\t",end="")#print genrated fibonnaci element at particular index

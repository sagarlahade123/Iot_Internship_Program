"""
FILE_NAME:frequency_of_words.py
TITLE:Accepting input from user and print its word frequency
DEVLOPED_BY:SAGAR
DATE_OF_CREATION:11/10/2018 17:00  PM
DATE_OF_LAST_UPDATION:11/10/2018 17:28 AM
PYTHON_VERSION:3.7.0
"""
input_string=input("Enter string to get frequency count of word in it:") #this line accept input from user for frequency count
word_list=input_string.rstrip()#rstrip function remove back space from string
word_list=word_list.split()#spilit function devides string into diffrent words

dictionary_to_store_word_and_frequency={} #to  store word as a key and corresponding frequency as value
for word in word_list:#run over all words present in wordlist
    if word in dictionary_to_store_word_and_frequency:#if word present in dictionary increment it by one
        dictionary_to_store_word_and_frequency[word]=dictionary_to_store_word_and_frequency[word]+1
    else:
        dictionary_to_store_word_and_frequency[word]=1 #if word comes first time set it to one

sorted_keys=sorted(dictionary_to_store_word_and_frequency)#sorted(dictinaory _object) it will co
                                    #sorted() return sorted iterable list on keys
length_of_dictionary=len(dictionary_to_store_word_and_frequency)#calculate number of elements present in dictionary

for i in range(length_of_dictionary):#loop runs uto the number of elements present in dictinory
    print(str(sorted_keys[i]+":"+str(dictionary_to_store_word_and_frequency[sorted_keys[i]]))) #getting sorted key from list and getting its value from dictionary and printing it



"""
 File name: Freq_Count_Words.py
    Program title: Count frequency of words in statement
    Author: Bhagyashri Patil
    Date created: 11/10/2018
    Date last modified: 11/10/2018
    Python Version: 3.7.0
"""
#take input from user
statement=input("Enter string:")
list_of_split_words=[]

#split function split statement according to sapce
list_of_split_words=statement.split()

#count holds the no of frequency of each word
wordfreq=[list_of_split_words.count(p) for p in list_of_split_words]

# Python zip function takes iterable elements as input, and returns iterator.
list_of_words=dict(zip(list_of_split_words,wordfreq))
print(list_of_words)

#sort the list of words by keys
sorted_data=sorted(list_of_words.keys())

#calculate length of list_of_words
length=list_of_words.__len__()
print(length)

#Loop to print words and their count as key value pair
for i in range(int(length)):
    print(str(sorted_data[i])+":"+str(list_of_words[sorted_data[i]]))
    #print(dictionary.values())
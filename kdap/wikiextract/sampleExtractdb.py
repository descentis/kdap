#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:01:20 2019

@author: descentis
"""

import sqlite3
import ast

conn = sqlite3.connect('/home/descentis/research/KML/nidhi_database/articleDescdb.db')																			#connecting to database  
print("Connection made")
#conn.execute("drop table article_desc;")                                                                           #dropped the existing table with same name
#conn.execute("create table article_desc(article_nm text,vital_article text,level text,class text,topic text);");   #cretaed table article_desc
#print("table article_desc created")
#conn.execute("create table wiki_project(article_nm text,project text;")                                            #created table wiki_projet
#print("table wiki_project created")


def display_data(query):
    cursor = conn.execute(query)
    displayList = []
    for row in cursor:
         displayList.append(row)
    return displayList

def insert_article_data(csvfile):
    line_no = 0                                                                                      #variable to count number of lines
    for line in open(csvfile, encoding='latin-1'):                                                   #opens csv file and loop to fetch each line in file
        line_no = line_no + 1
        if line_no==1:
            continue
        else:
            query = "insert into article_desc(article_nm,vital_article,level,class,topic) values("   #string variable 'query' to store mysql query, creating insert query
            arr = line.split('@$@')                                                                  #spliting the file line fetched based on the deliminator '@$@'
            for i in range(0, 5):                                                                    #loop to fetch each value obtained after spliting the line
                if i == 0:
                    query = query + '"' + arr[i] + '"'
                else:
                    query = query + ',"' + arr[i] + '"'
            query = query + ");"
            print(line_no)
            conn.execute(query)                                                                      #executing query                                                                              #saving changes by every 1000 lines in database
    print("all data inserted")
    conn.commit()

def insert_wiki_project(csvfile):
    line_no = 0                                                                                      #variable to count number of lines
    for line in open(csvfile, encoding='latin-1'):                                                   #opens csv file, and loop to fetch each line in file
        line_no = line_no + 1
        if line_no==1 or line_no==3:
            continue
        else:
            arr=line.split('@$@')                                                                           #splites the value in the csv file based on the deliminator"@$@"
            title = arr[0]
            temp = arr[5]                                                                                   #accessing the last value in the line , wikipedia projects, they are in the form an array

            if temp.startswith('NA'):                                                                       #if wikipedia project name not available
                    query = "insert into wiki_project(article_nm,project) values('" + title + "',NULL);"    #creating insert query
                    conn.execute(query)                                                                     #executing insert query
            else:                                                                                           #if wikipedia project name avaialble
                    arr2=ast.literal_eval(temp)                                                             #converting it into array
                    if arr2==[]:                                                                            #if array is empty
                        query = "insert into wiki_project(article_nm,project) values('"+ title + "',NULL);" #creating insert query
                        conn.execute(query)                                                                 #executing insert query
                    else:                                                                                   #if array contains values
                        for val in arr2:
                            vali=val.replace("'","\\'")
                            query="insert into wiki_project(article_nm,project) values('"+title+"','"+vali+"');" #creating insert query
                            conn.execute(query)                                                                  #executing insert query
            print(line_no)                                                                                       #save changes to database after executing every 1000 lines
    print("all data inserted")
    conn.commit()                                                                                                # saving the changes in the database




#insert_article_data('articleDesc.csv')                                          #this function call insert the table article_desc with article  data like(article name,vital article,level,topic ,class)
#print('Data inserted in articledesc')

#insert_wiki_project('articleDesc.csv')                                          #this function call would insert all the data in table wiki_project with article data like (article name , and project category)
#print("Data inserted in wiki_project")

'''
print("First 10 values in wiki_project")
display_data("select *from wiki_project limit 10;")                              #will displays first 10 values present in the table wiki_project

print("\nFirst 10 values in article_desc")
display_data("select *from article_desc limit 10;")                              #will display first 10 values present in table article_desc

print("Operation performed successfully")
'''

#faList = display_data("select article_nm from article_desc where class = 'B';")
#faList = display_data("select article_id,article_nm,class from article_desc where article_nm = 'Lionel Messi';")
#faList = display_data("select article_nm,project from wiki_project where article_nm = 'Lionel Messi';")
#faList = display_data("select article_id, article_nm from article_desc where class = 'FA';")
#k = display_data("select *from wiki_project where project='india';")
#football = display_data("select article_nm,project from wiki_project where project='football';")
#biography = display_data("select article_nm,project from wiki_project where project='biography';")
#countries = display_data("select article_nm,project from wiki_project where project='countries';")
faList = display_data("select article_nm from article_desc where class = 'FA';")

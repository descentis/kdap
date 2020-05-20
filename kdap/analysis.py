#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:56:26 2019

@author: descentis
"""
import xml.etree.ElementTree as ET
import math
import glob
import numpy as np
from multiprocessing import Process, Lock, Manager
from datetime import datetime
import re
import string
import os
import mwparserfromhell
from nltk.tokenize import word_tokenize
import copy
from kdap.converter.wikiConverter import wikiConverter
import wikipedia
import sqlite3
from bx.misc.seekbzip2 import SeekableBzip2File
from internetarchive import download
from pyunpack import Archive
from os.path import expanduser
from kdap.wikiextract.wikiExtract import wikiExtract
from mwviews.api import PageviewsClient
from kdap.converter.qaConverter import qaConverter
from kdap.wikiextract.knolml_wikiextractor import QueryExecutor
from collections import Counter 
import kdap.wiki_graph.graph_creater as gc
import kdap.converter.wiki_clean as wikiClean

class instances(object):
    

    def __init__(self,instance, title):
        #self.test = 'jsut to check the instances class'
        #print(self.test)
        #print(instance.tag)        
        self.instanceId = instance.attrib['Id']
        self.instanceType = instance.attrib['InstanceType']
        self.instanceTitle = title
        if(instance.attrib.get('RevisionId')!=None):
            self.revId = instance.attrib['RevisionId']
        self.instance_attrib = {}
        for ch1 in instance:
            if 'TimeStamp' in ch1.tag:
                self.instance_attrib['TimeStamp'] = {}
                for ch2 in ch1:
                    if 'CreationDate' in ch2.tag:
                        self.instance_attrib['TimeStamp']['CreationDate'] = ch2.text
                    if 'LastEditDate' in ch2.tag:
                        self.instance_attrib['TimeStamp']['LastEditDate'] = ch2.text                       
                    if 'LastActivityDate' in ch2.tag:
                        self.instance_attrib['TimeStamp']['LastActivityDate'] = ch2.text
                    if 'CommunityOwnedDate' in ch2.tag:
                        self.instance_attrib['TimeStamp']['CommunityOwnedDate'] = ch2.text
                    if 'ClosedDate' in ch2.tag:
                        self.instance_attrib['TimeStamp']['ClosedDate'] = ch2.text
                    
            
            if 'Contributors' in ch1.tag:
                self.instance_attrib['Contributors'] = {}
                for ch2 in ch1:
                    if 'OwnerUserId' in ch2.tag:
                        self.instance_attrib['Contributors']['OwnerUserId'] = ch2.text
                    if 'OwnerUserName' in ch2.tag:
                        self.instance_attrib['Contributors']['OwnerUserName'] = ch2.text
                    if 'LastEditorUserId' in ch2.tag:
                        self.instance_attrib['Contributors']['LastEditorUserId'] = ch2.text
            
            if 'Body' in ch1.tag:
                self.instance_attrib['Body'] = {}
                for ch2 in ch1:
                    if 'Text' in ch2.tag:
                        self.instance_attrib['Body']['Text'] = {}
                        self.instance_attrib['Body']['Text']['#Type'] = ch2.attrib['Type']
                        self.instance_attrib['Body']['Text']['#Bytes'] = ch2.attrib['Bytes']
                        self.instance_attrib['Body']['Text']['text'] = ch2.text
                    
            if 'Tags' in ch1.tag:
                self.instance_attrib['Tags'] = ch1.text
            
            if 'Credit' in ch1.tag:
                self.instance_attrib['Credit'] = {}
                for ch2 in ch1:
                    if 'Score' in ch2.tag:
                        self.instance_attrib['Credit']['Score'] = ch2.text
                    if 'CommentCount' in ch2.tag:
                        self.instance_attrib['Credit']['CommentCount'] = ch2.text
                    if 'ViewCount' in ch2.tag:
                        self.instance_attrib['Credit']['ViewCount'] = ch2.text
                    if 'AnswerCount' in ch2.tag:
                        self.instance_attrib['Credit']['AnswerCount'] = ch2.text
                    if 'FavouriteCount' in ch2.tag:
                        self.instance_attrib['Credit']['FavouriteCount'] = ch2.text
            
    
    def is_question(self):
        '''
        Retruns True if the instance is a question
        Works with QnA based knolml dataset
        '''
        if self.instanceType == 'Question':
            return True
        
    def is_answer(self):
        '''
        Retruns True if the instance is an answer
        Works with QnA based knolml dataset
        '''
        if self.instanceType == 'Answer':
            return True    
    def is_comment(self):
        '''
        Retruns True if the instance is a comment
        Works with QnA based knolml dataset
        '''
        if self.instanceType == 'Comments':
            return True
    
    def is_closed(self):
        '''
        Retruns True if the qna thread is closed
        Works with QnA based knolml dataset
        '''
        if self.instance_attrib['TimeStamp'].get('ClosedDate') == None:
            return True
        
    def just_to_check(self):
        print("just to check function")
        print(self.instanceId)
        print(self.instanceType)
        
    def get_editor(self):
        '''
        Retruns the edior details
        '''
        di = {}
        if self.instance_attrib['Contributors'].get('OwnerUserId')!=None:
            di['OwnerUserId'] = self.instance_attrib['Contributors']['OwnerUserId']
        if self.instance_attrib['Contributors'].get('OwnerUserName')!=None:
            di['OwnerUserName'] = self.instance_attrib['Contributors']['OwnerUserName']
        if self.instance_attrib['Contributors'].get('LastEditorUserId')!=None:
            di['LastEditorUserId'] = self.instance_attrib['Contributors']['LastEditorUserId']
        return di
    
    def get_title(self):
        '''
        Retruns the title
        '''
        return self.instanceTitle
    
    def get_tags(self):
        '''
        Retruns the tag details
        Works for QnA dataset
        '''
        if self.instance_attrib.get('Tags')!=None:
            return self.instance_attrib['Tags'].split('><')
        else:
            print("No tags are found")
    
    def get_timestamp(self):
        '''
        Retruns the timestamp details
        '''
        di = {}
        if self.instance_attrib['TimeStamp'].get('CreationDate')!=None:
            di['CreationDate'] = self.instance_attrib['TimeStamp']['CreationDate']
        if self.instance_attrib['TimeStamp'].get('LastEditDate')!=None:
            di['LastEditDate'] = self.instance_attrib['TimeStamp']['LastEditDate']
        if self.instance_attrib['TimeStamp'].get('LastActivityDate')!=None:
            di['LastActivityDate'] = self.instance_attrib['TimeStamp']['LastActivityDate']
        if self.instance_attrib['TimeStamp'].get('CommunityOwnedDate')!=None:
            di['CommunityOwnedDate'] = self.instance_attrib['TimeStamp']['CommunityOwnedDate']
        if self.instance_attrib['TimeStamp'].get('ClosedDate')!=None:
            di['ClosedDate'] = self.instance_attrib['TimeStamp']['ClosedDate']
        return di        
    
    def get_score(self):
        '''
        Retruns the score details
        '''
        if self.instance_attrib.get('Credit')==None:
            return 'Score value is not available'
        di = {}
        if self.instance_attrib['Credit'].get('Score')!=None:
            di['Score'] = self.instance_attrib['Credit']['Score']
        if self.instance_attrib['Credit'].get('CommentCount')!=None:
            di['CommentCount'] = self.instance_attrib['Credit']['CommentCount']
        if self.instance_attrib['Credit'].get('ViewCount')!=None:
            di['ViewCount'] = self.instance_attrib['Credit']['ViewCount']
        if self.instance_attrib['Credit'].get('AnswerCount')!=None:
            di['AnswerCount'] = self.instance_attrib['Credit']['AnswerCount']
        if self.instance_attrib['Credit'].get('FavouriteCount')!=None:
            di['FavouriteCount'] = self.instance_attrib['Credit']['FavouriteCount']
        return di  
        
    def get_text(self, *args, **kwargs):
        '''
        Retruns the text data
        '''
        di = {}
        clean = False    
        if self.instance_attrib['Body']['Text'].get('text') != None:
            di['text'] = self.instance_attrib['Body']['Text']['text']
        
        if kwargs.get('clean') != None:
            clean = kwargs['clean']
        if clean:
            di['text'] = wikiClean.getCleanText(di['text'])
            '''
            qe = QueryExecutor()
            qe.setOutputFileDirectoryName('lol')
            qe.setNumberOfProcesses(5)
            qe.setNumberOfBytes(2000000000)
            qe.setTextValue(di['text'])
            qe.runQuery()
            return qe.result()
            '''
        
        return di
    
    def get_bytes(self):
        '''
        Retruns the bytes detail
        '''
        if self.instance_attrib['Body']['Text'].get('#Bytes') != None:
               return  int(self.instance_attrib['Body']['Text']['#Bytes'])
                           

    def __count_words(self, text):
        '''
        Retruns number of words in the text
        
        **Arguments**
        text:
            Type: string
        '''
        text = text.lower()
        skips = [".", ",", ":", ";", "'", '"']
        for ch in skips:
            text = text.replace(ch, "")
        word_counts = Counter(text.split(" "))
        return word_counts                           
    
    def __get_emailid(self, text):
        '''
        Retruns the email ids in the text
        
        **Arguments**
        text:
            Type: string
        '''
        lst = re.findall('\S+@\S+',text)
        return lst
    
    def __get_url(self, text):
        '''
        Retruns all the the urls in the text
        
        **Arguments**
        text:
            Type: string
        '''
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        return url
    
    def get_text_stats(self, *args, **kwargs):
        '''
        Retruns the email ids in the text
        
        **Arguments**
        title:
            optional
            Type: bool
        
        count_words:
            optional
            type: string
        
        email_id:
            optional
            type: string
        
        url:
            optional
            type: string
                
        '''
        title = False
        if kwargs.get('title')!=None:
            if kwargs['title'] == True:
                title = True
        if title:
            if kwargs.get('count_words')!=None:
                return self.__count_words(self.title)
            if kwargs.get('email_id')!=None:
                return self.__get_emailid(self.title)
            if kwargs.get('url')!=None:
                return self.__get_url(self.title)
        else:
            if kwargs.get('count_words')!=None:
                return self.__count_words(self.get_text['text'])
            if kwargs.get('email_id')!=None:
                return self.__get_emailid(self.get_text['text'])
            if kwargs.get('url')!=None:
                return self.__get_url(self.get_text['text'])

# please have a look @aayush

        
class knowledge_data(object):
    
    def __init__(self, *args, **kwargs):
        self.file_name = ''
        self.dir_path = ''
        self.kcounter = 0
        self.knowledgeData_list = []
        self.dir = 0
        if(kwargs.get('file_name')!=None):
            self.file_name = kwargs['file_name']
        elif(kwargs.get('dir_path')!=None):
            self.dir = 1
            self.dir_path= kwargs['dir_path']
            self.number = re.compile(r'(\d+)')
            if os.path.isdir(self.dir_path+'/Posts'):
                self.file_list = sorted(glob.glob(self.dir_path+'/Posts/*.knolml'), key=self.numericalSort)
            else:
                self.file_list = sorted(glob.glob(self.dir_path+'/*.knolml'), key=self.numericalSort)
            

    def numericalSort(self, value):
        parts = self.numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts        
    
    def count_instances(self):
        if self.file_name != '':        
            tree = ET.parse(self.file_name)
            r = tree.getroot()
            di = {}
            knowledgeDataList = []
            for child in r:
                if('KnowledgeData' in child.tag):
                    #root = child
                    for ch in child:
                        if 'Title' in ch:
                            title = ch.text
                    knowledgeDataList.append([title,child])
            for kn in knowledgeDataList:
                length = len(kn[1].findall('Instance'))
                di[kn[0]] = length                

            return di  
        else:
            return 'file name not given'
        
class knol(object):
    
    def __init__(self):
        self.dir = 0
        self.kcounter = 0
        self.knowledgeData_list = []
        self.object_list = []
        self.file_name = ''
        self.dump_directory = ''

    '''
    frame method is used to store the knolml data in terms of frames
    each instances can be analyzed separately and sequencially
    '''
    def frame(self, *args, **kwargs):
        '''
        **Requires dataset to be present**
        This method takes file names as an argument and returns the list of frame objects
        
        *Arguments*
        
        file_name:
            optional
            Type: String
            The name of the article for which the frame objects have to be created.
        
        dir_path:
            optional
            Type: String
            The path of the directory containing the knolml files
            
        e.g frame = knol.frame()
        
        '''
        if(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            self.file_name = file_name
            self.get_knowledgeData(self.file_name)
        elif(kwargs.get('dir_path')!=None):
            self.dir = 1
            dir_path = kwargs['dir_path']
            self.numbers = re.compile(r'(\d+)')
            self.file_count = 0
            if os.path.isdir(dir_path+'/Posts'):
                self.file_list = sorted(glob.glob(dir_path+'/Posts/*.knolml'), key=self.numericalSort)
            else:
                self.file_list = sorted(glob.glob(dir_path+'/*.knolml'), key=self.numericalSort)
            self.get_knowledgeData(self.file_list[0])
            
        return self.object_list

    def get_knowledgeData(self,file_name):
        tree = ET.parse(file_name)
        
        root = tree.getroot()
        for elem in root:
            if 'KnowledgeData' in elem.tag:
                self.knowledgeData_list.append(elem)
        
        self.object_list = self.get_frames(self.knowledgeData_list[self.kcounter])        
    
    
    def numericalSort(self, value):
        parts = self.numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    
    def get_frames(self, elem):        
        object_list = []
        title = ''
        for ch1 in elem:
            if 'Title' in ch1.tag:
                title = ch1.text
            if 'Instance' in ch1.tag:
                instance = ch1
                object_list.append(instances(instance, title))
        
        return object_list
    
    def Next(self):
        self.kcounter+=1
        if(self.kcounter<len(self.knowledgeData_list)):
            self.get_knowledgeData(self.knowledgeData_list[self.kcounter])
        elif(self.dir==1):
            self.file_count+=1
            self.get_knowledgeData(self.file_list[self.file_count])
        
        return self.object_list
    
    #******************methods related to frames ends here*****************************
        
    '''
    Following methods are used to download the relavent dataset from archive in Knol-ML format
    '''
    def extract_from_bzip(self, *args, **kwargs):
        # file, art, index, home, key
        file = kwargs['file']
        art = kwargs['art']
        index = kwargs['index']
        home = kwargs['home']
        key = kwargs['key']
        filet = home+"/knolml_dataset/bz2t/"+file+'t'
        chunk = 1000
        try:
            f = SeekableBzip2File(self.dump_directory+'/'+file, filet)
            f.seek(int(index))
            strData = f.read(chunk).decode("utf-8")
            artName = art.replace(" ","_")
            artName = artName.replace("/","__")
            if not os.path.isdir(home+'/knolml_dataset/output/'+key):
                os.makedirs(home+'/knolml_dataset/output/'+key)
            if not os.path.exists(home+'/knolml_dataset/output/'+key+'/'+artName+".xml"):
                article = open(home+'/knolml_dataset/output/'+key+'/'+artName+".xml", 'w+')
                article.write('<mediawiki>\n')
                article.write('<page>\n')
                article.write('\t\t<title>'+art+'</title>\n')
                #article.write(strData)
                while '</page>' not in strData :
                    article.write(strData)
                    strData = f.read(chunk).decode("utf-8", errors = "ignore")
                    
            
                end = strData.find('</page>')
                article.write(strData[:end])
                article.write("\n")
                article.write('</page>\n')
                article.write('</mediawiki>')
            f.close()
        except:
            print("please provide the dump information")

    def get_article_name(self, article_list):
        '''
        article_list provides a list of articles to be searched
        this function finds the coorect name of the article which is present on wikipedia
        '''
        if type(article_list) == list:
            articles = []
            for article in article_list:
                wiki_names = wikipedia.search(article)
                if article in wiki_names:
                    articles.append(article)
                    pass
                else:
                    print("The same name article: '"+article+"' has not been found. Using the name as: "+wiki_names[0])
                    articles.append(wiki_names[0])
            return articles
        else:
            wiki_names = wikipedia.search(article_list)
            if article_list in wiki_names:
                return article_list
            else:
                print("The same name article: '"+article_list+"' has not been found. Using the name as: "+wiki_names[0])
                return wiki_names[0]            
    
    def download_from_dump(self, home, articles, key):
        if not os.path.isdir(home+'/knolml_dataset/phase_details'):
            download('knolml_dataset', verbose=True, glob_pattern='phase_details.7z', destdir=home)
            Archive('~/knolml_dataset/phase_details.7z').extractall('~/knolml_dataset')
        if not os.path.isdir(home+'/knolml_dataset/bz2t'):
            download('knolml_dataset', verbose=True, glob_pattern='bz2t.7z', destdir=home)
            Archive('~/knolml_dataset/bz2t.7z').extractall(home+'/knolml_dataset')
        fileList = glob.glob(home+'/knolml_dataset/phase_details/*.txt')
        for files in fileList:
            if('phase' in files):
                with open(files,'r') as myFile:
                    for line in myFile:
                        l = line.split('#$*$#')
                        if l[0] in articles:
                            print("Found hit for article "+l[0])
                            # file, art, index, home, key
                            self.extract_from_bzip(file=l[1],art=l[0],index=int(l[2]), home=home, key=key)
    
    def download_dataset(self, *args, **kwargs):
        # sitename = Portal name
        # article_list = [] List of article to be extracted
        # wikipedia_dump = directory of the wikipedia dump
        '''
        sitename varibale contains the portal from which user wants to download the dataset.
        Each sitename has various parameters which can be provided as optional argument
        '''
        if kwargs.get('sitename') != None:
            sitename = kwargs['sitename'].lower()
        else:
            print('add sitename')
            return
        try:
            compress_bool = kwargs['compress']
        except:
            compress_bool = False
        sitename = sitename.lower()
        home = expanduser("~")
        download_data = True
        if kwargs.get('destdir') != None:
            destdir = kwargs['destdir']
        else:
            if not os.path.isdir(home+'/knolml_dataset/wikipedia_articles'):
                os.makedirs(home+'/knolml_dataset/wikipedia_articles')
            destdir = home+'/knolml_dataset/wikipedia_articles'
            
        if kwargs.get('wikipedia_dump')!=None:
            self.dump_directory = kwargs['wikipedia_dump']
            
        if sitename == 'wikipedia':
            if kwargs.get('article_list')!=None:
                article_list = kwargs['article_list']
                key = 'article_list'
                #articles = self.get_article_name(article_list)
                self.download_from_dump(home, article_list, key)
                
                if compress_bool:
                    wikiConverter.compressAll(home+'/knolml_dataset/output/'+key,output_dir=destdir+'/'+key)
                else:
                    print("conversion started")
                    wikiConverter.convertall(home+'/knolml_dataset/output/'+key,output_dir=destdir+'/'+key)
            if kwargs.get('download')!=None:
                download_data = kwargs['download']
                
            if kwargs.get('category_list')!= None:
                category_list = kwargs['category_list']
                final_category_list = []
                final_category = {}
                sub_category = {}
                we = wikiExtract()
                for category_name in category_list:
                    category_title = we.get_articles_by_category(category_name)
                    #print(category_title)
                    for key,val in category_title.items():
                        if key != 'extra#@#category':
                            final_category[key] = val
                            if download_data:
                                download_list = []
                                for el in category_title[key]:
                                    download_list.append(el['title'])
                                articles = self.get_article_name(download_list)
                                self.download_from_dump(home, articles, key)
                                if compress_bool:
                                    wikiConverter.compressAll(home+'/knolml_dataset/output/'+key,output_dir=destdir+'/'+key)
                                else:
                                    print("conversion started")
                                    wikiConverter.convertall(home+'/knolml_dataset/output/'+key,output_dir=destdir+'/'+key)
                        else:
                            li = []
                            for el in category_title[key]:
                                category_list.append(el['title'].replace('Category:',''))
                                li.append(el['title'].replace('Category:',''))
                            
                            sub_category[category_name] = li
                final_category_list.append(final_category)
                final_category_list.append(sub_category)
                
                return final_category_list

            if kwargs.get('template_list')!= None:
                template_list = kwargs['template_list']
                final_template_list = []
                final_template = {}
                sub_template = {}
                we = wikiExtract()
                for template_name in template_list:
                    template_title = we.get_articles_by_template(template_name)
                    #print(category_title)
                    for key,val in template_title.items():
                        if key != 'extra#@#category':
                            final_template[key] = val
                            if download_data:
                                download_list = []
                                for el in template_title[key]:
                                    download_list.append(el['title'])
                                articles = self.get_article_name(download_list)
                                self.download_from_dump(home, articles, key)
                                if compress_bool:
                                    wikiConverter.compressAll(home+'/knolml_dataset/output/'+key,output_dir=destdir+'/'+key)
                                else:
                                    print("conversion started")
                                    wikiConverter.convertall(home+'/knolml_dataset/output/'+key,output_dir=destdir+'/'+key)
                        else:
                            li = []
                            for el in template_title[key]:
                                template_list.append(el['title'].replace('Category:',''))
                                li.append(el['title'].replace('Category:',''))
                            
                            sub_template[category_name] = li
                final_template_list.append(final_template)
                final_template_list.append(sub_template)
                
                return final_template_list            
        elif sitename == 'stackexchange':
            if kwargs.get('portal')!=None:
                portal = kwargs['portal']
                qaConverter.convert(name=portal, download=True, post=True)
                    
    '''
    get_article method downloads the full revision history of an article in knol-ML format
    '''
    def get_wiki_article(self, article_name, *args, **kwargs):
        #self.file_name = article_name.replace(' ','_')
        #self.file_name = self.file_name.replace('/','__')
        #self.file_name = self.file_name+'.knolml'
        compress = False
        wiki_names = wikipedia.search(article_name)
        output_dir = 'output'
        if(kwargs.get('output_dir')!=None):
            output_dir = kwargs['output_dir']
                
        if kwargs.get('compress')!=None:
            compress = kwargs['compress']
        #self.file_name = output_dir+'/'+self.file_name
            
        if article_name in wiki_names:
            if compress:
                wikiConverter.getArticle(file_name=article_name, output_dir='outputD')
                article_name = article_name.replace(' ', '_')
                article_name = article_name.replace('/', '__')
                wikiConverter.compress('outputD/'+article_name+'.knolml', output_dir)
            else:
                wikiConverter.getArticle(file_name=article_name, output_dir=output_dir)
        else:
            print("Article name is not found. Taking '"+wiki_names[0]+"' as the article name")
            article_name = wiki_names[0]
            if compress:
                wikiConverter.getArticle(file_name=article_name, output_dir='outputD')
                article_name = article_name.replace(' ', '_')
                article_name = article_name.replace('/', '__')
                wikiConverter.compress('outputD/'+article_name+'.knolml', output_dir)
            else:
                wikiConverter.getArticle(file_name=article_name, output_dir=output_dir)
        
      

    '''
    function to display the query on database
    '''
    def display_data(self, query, conn):
        cursor = conn.execute(query)
        displayList = []
        for row in cursor:
             displayList.append(row)
        
        return displayList
    
    '''
    following function queries the database to extract the articles based on category namme
    '''
    def get_wiki_article_by_class(self, *args, **kwargs):
        home = expanduser("~")
        if not os.path.exists(home+'/knolml_dataset/articleDescdb.db'):
            download('knolml_dataset', verbose=True, glob_pattern='articleDescdb.db', destdir=home)
        try:
            conn = sqlite3.connect(home+'/knolml_dataset/articleDescdb.db')		#connecting to database  
            print("Connection made")
        except:
            print("connection refused")
            
        if kwargs.get('wikiproject')!=None:
            wikiproject = kwargs['wikiproject'].lower()
            
            article_id = []
            if wikiproject.lower()!='mathematics':
                article_ids = self.display_data("select article_nm,project from wiki_project where project='"+wikiproject.lower()+"';",conn)
                for i in article_ids:
                    article_id.append(i[0])
                article_id = str(tuple(article_id))
                
                articles = self.display_data("select article_nm from article_desc where article_id in "+article_id+";", conn)
            else:
                articles = self.download_dataset('wikipedia', category_list=['WikiProject Mathematics articles'], download=False)
        
        if kwargs.get('wiki_class')!=None:
            c = kwargs['wiki_class'].lower()
            if c=='fa':
                c = 'FA'
            elif c == 'ga':
                c = 'GA'
            elif c == 'c':
                c = 'C'
            elif c == 'b':
                c = 'B'
            elif c == 'a':
                c = 'A'
            elif c == 'start':
                c = 'Start'
            elif c == 'stub':
                c = 'Stub'
            
            articles = self.display_data("select article_id, article_nm from article_desc where class ='"+c+"';", conn)
        return articles
             

    # All the analysis functions are written after this
    def __instance_date(self, *args, **kwargs):     
        if kwargs.get('file_list') != None:
            file_list = kwargs['file_list']
        for file_name in file_list:
            context_wiki = ET.iterparse(file_name, events=("start","end"))
            # Turning it into an iterator
            context_wiki = iter(context_wiki)
            
            # getting the root element
            event_wiki, root_wiki = next(context_wiki)
            date = []
            try:
                for event, elem in context_wiki:
                    if event == "end" and 'Instance' in elem.tag:
                        for ch1 in elem:
                            if 'TimeStamp' in ch1.tag:
                                for ch2 in ch1:
                                    if 'CreationDate' in ch2.tag:                                    
                                        d = ch2.text.replace('-','')
                                        date.append(d.split('T')[0])
                        elem.clear()
                        root_wiki.clear()
            except:
                print('problem with file parsing: '+file_name)
            
            if(kwargs.get('instance_date')!=None):  
                if kwargs.get('dir_path')!=None:
                    file_name = file_name.replace(kwargs['dir_path']+'/','')
                else:
                    file_name = file_name.split('/')[-1]
                file_name = file_name[:-7].replace('_', ' ')
                file_name = file_name.replace('__', '/')
                kwargs['instance_date'][file_name] = date
            
    
    def get_instance_date(self, *args, **kwargs):
        '''
        This piece of code is to ensure the multiprocessing
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 4           # Bydefault it is 4
        
        fileNum = len(file_list)
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        manager = Manager()
        instance_date = manager.dict()
        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=self.__instance_date, kwargs={'file_list':fileList[i], 'instance_date': instance_date,'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return instance_date
    
    def get_pageviews(self, site_name, *args, **kwargs):
        if site_name.lower() == 'wikipedia':
            start = ''
            end = ''
            granularity='monthly'
            if kwargs.get('article_name')!=None:
                article_name = kwargs['article_name']
            article_name = self.get_article_name(article_name)
            if kwargs.get('start')!=None:
                start = kwargs['start'].replace('-','')

            if kwargs.get('end')!=None:
                end = kwargs['end'].replace('-','')

            if kwargs.get('granularity')!=None:
                granularity = kwargs['granularity']                
                
            p = PageviewsClient(user_agent="<person@organization.org>")
            
            if start=='':
                return p.article_views('en.wikipedia', article_name, granularity=granularity)
            elif end=='':
                return p.article_views('en.wikipedia', article_name, granularity=granularity, start=start, end=start)
            else:
                return p.article_views('en.wikipedia', article_name, granularity=granularity, start=start, end=end)

    @staticmethod
    def get_diff_match(revisionsDict, length, n):
        #n = int(input(str(length)+" Revisons found, enter the revision number to be loaded: "))
        returnResult = []
        original = n
        m = int((math.log(length)) ** 2)+1
        if n%m != 0:
            interval = n - (n%m) + 1
            n = n - interval + 1
        else:
            interval = n - (m-1)
            n = n - interval + 1
        
        
        count = interval
        prev_str = revisionsDict[count]
        result = prev_str
        returnResult.append(result)
        while count < original:
            count += 1
            s = [x.replace("\n", "`").replace("-", "^") for x in prev_str.split(" ")]
            i = 0
            while(True):
                if i == len(s):
                    break;
                if s[i].isspace() or s[i] == '':
                    del s[i]
                else:	
                    i += 1	
        
            next_rev = revisionsDict[count]
            s2 = next_rev.split(" ")
            i = 0
            while(True):
                if i == len(s2):
                    break;
                if s2[i].isspace() or s2[i] == '':
                    del s2[i]
                else:	
                    i += 1	
        
            index = 0
            result = ""
            for x in s2:
                if x.isdigit():
                    for i in range(index, index+int(x)):
                        result += s[i].replace("`", "\n").replace("^", "-")
                        result += " "
                        index += 1
                elif x[0] == "'" and x[-1] == "'" and x[1:-1].isdigit():
        
                        result += x[1:-1].replace("`", "\n			").replace("^", "-")
                        result += " "
                else:
                    if x[0] == '-':
                        for i in range(index, index+int(x[1:])):
                            index += 1
                    else:
                        result += x.replace("`", "\n			").replace("^", "-")		
                        result += " "
        
            prev_str = result
            returnResult.append(result)        
        
        return returnResult


    
    @classmethod
    def wikiRetrieval(cls,file_name,n):
        tree = ET.parse(file_name)
        r = tree.getroot()
        revisionsDict = {}
        for child in r:
            if('KnowledgeData' in child.tag):
                root = child
        length = len(root.findall('Instance'))
        for each in root.iter('Instance'):
            instanceId = int(each.attrib['Id'])
            for child in each:
                if 'Body' in child.tag:
                    revisionsDict[instanceId] = child[0].text

        returnResult = knol.get_diff_match(revisionsDict, length, n)
        return returnResult
    
    
    def allRevisions(self,file_name,root,tree):
        
        
        '''
        for child in r:
            if('KnowledgeData' in child.tag):
                root = child
        '''
        
         
        for child in root:
            if('KnowledgeData' in child.tag):                
                if('Wiki' in child.attrib['Type']):
                    length = len(child.findall('Instance'))        
                    if length == 1:
                        print("No revisions found, generate revisions from xmltoknml.py first")
                        exit()
                    
                    revisionList = []
                    k = int((math.log(length)) ** 2)
                    for i in range(k+1,(math.ceil(length/(k+1))-1)*(k+1)+1,(k+1)):
                        revisionList.append(i)
                        
                    revisionList.append(length)
                #print(revisionList)

        
        
       
        return revisionList
        
   
    @classmethod     
    def getAllRevisions(cls,file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()
        

        for child in root:
            if('KnowledgeData' in child.tag):
                #print(child.attrib['Type'])
                if('Wiki' in child.attrib['Type']):
                    revisionsList = cls.allRevisions(cls,file_name,root,tree)
                elif('QA' in child.attrib['Type']):
                    revisionsList = child
                
        return revisionsList
    
    
    '''
    This is dummy function to refer how to get all the revisions of wiki    
    '''
    def getRev(self, file_name):
        cRev = 1
        #print(revisionList)
        revisionList = self.getAllRevisions(file_name)
        for rev in revisionList:
            revisions = self.wikiRetrieval(file_name,rev)
            #print(len(revisions))
            for revision in revisions:
                # write your analysis for each revision
                x = 0
                
                with open('dummy.txt','a') as myFile:
                    myFile.write(revision+'\n')
                    myFile.write(str(cRev)+'\n')
                
                cRev+=1

    
    
    '''
    This function can be used to get knol from a knolml file.
    The idea behind knol is to generalize the knowledge unit for each portal.
    Each frame will have parameters (user, time, data, etc) related to it, one can easily retrieve the parameters associated with a frame
    '''
    
    # Yet to add the function
        
    
              
    def __countRev(self, *args, **kwargs):
        if kwargs.get('file_list') != None:
            file_list = kwargs['file_list']
        if kwargs.get('l') != None:
            l = kwargs['l']
        for file_name in file_list:
            context_wiki = ET.iterparse(file_name, events=("start","end"))
            # Turning it into an iterator
            context_wiki = iter(context_wiki)
            if kwargs.get('granularity') != None:
                d_form = '%Y-%m-%d'
                start = datetime.strptime(kwargs['start'], d_form)
                if kwargs.get('end')!=None:
                    if kwargs['end'] != '':
                        end = datetime.strptime(kwargs['end'], d_form)
                m1 = start.month
                y1 = start.year
                rev_list = []
                date_format = "%Y-%m-%dT%H:%M:%S.%f"
            total_rev = 0
            total_rev_dict = {}
            # getting the root element
            event_wiki, root_wiki = next(context_wiki)
            try:
                for event, elem in context_wiki:
                    if event == "end" and 'Instance' in elem.tag:
                        if kwargs.get('instance_type') != None:
                            if kwargs['instance_type'] == 'question' and elem.attrib['InstanceType']=='Question':
                                l.acquire()
                                if(kwargs.get('revisionLength')!=None):
                                    if kwargs['revisionLength'].get('questions') == None:
                                        kwargs['revisionLength']['questions'] = 1
                                    else:
                                        kwargs['revisionLength']['questions'] += 1
                                l.release()
                            elif kwargs['instance_type'] == 'answer' and elem.attrib['InstanceType']=='Answer':
                                l.acquire()
                                if(kwargs.get('revisionLength')!=None):
                                    if kwargs['revisionLength'].get('answers') == None:
                                        kwargs['revisionLength']['answers'] = 1
                                    else:
                                        kwargs['revisionLength']['answers'] += 1
                                l.release()
                            
                        total_rev+=1
                        for ch1 in elem:
                            if 'TimeStamp' in ch1.tag:
                                for ch2 in ch1:
                                    if 'CreationDate' in ch2.tag:
                                        t = ch2.text
                                        if kwargs.get('granularity') != None:
                                            if kwargs['granularity'].lower() == 'monthly':
                                                t = datetime.strptime(t, date_format)
                                                if t>= start:
                                                    if total_rev_dict.get(t.year)==None:
                                                        total_rev_dict[t.year] = {}
                                                        total_rev_dict[t.year][t.month] = 1
                                                    elif total_rev_dict[t.year].get(t.month)==None:
                                                        total_rev_dict[t.year][t.month] = 1
                                                    else:
                                                        total_rev_dict[t.year][t.month] += 1
                                            if kwargs['granularity'].lower() == 'yearly':
                                                if t>=start:
                                                    if total_rev_dict.get(t.year)==None:
                                                        total_rev_dict[t.year] = 1
                                                    else:
                                                        total_rev_dict[t.year] += 1
                        
                        elem.clear()
                        root_wiki.clear()
            except:
                print('problem with file parsing: '+file_name)
            #print(total_rev_dict)
            #return total_rev_dict
            if(kwargs.get('revisionLength')!=None and kwargs['instance_type']==''):  
                if kwargs.get('dir_path')!=None:
                    file_name = file_name.replace(kwargs['dir_path']+'/','')
                file_name = file_name[:-7].replace('_', ' ')
                file_name = file_name.replace('__', '/')
                if kwargs.get('granularity') != None:
                    kwargs['revisionLength'][file_name] = total_rev_dict
                else:
                    kwargs['revisionLength'][file_name] = total_rev
            

    
    def get_num_instances(self, *args, **kwargs):
        '''
        This piece of code is to ensure the multiprocessing
        Enter a date in YYYY-MM-DD format for start and end dates
        '''
        if kwargs.get('instance_type')!=None:
            instance_type = kwargs['instance_type']
        else:
            instance_type = ''
            
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 4           # Bydefault it is 4
        
        fileNum = len(file_list)
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        

        manager = Manager()
        revisionLength = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            if kwargs.get('granularity') != None:
                granularity = kwargs['granularity']
                start = kwargs['start']
                if kwargs.get('end')!=None:
                    end = kwargs['end']
                else:
                    end = ''
                processDict[i+1] = Process(target=self.__countRev, kwargs={'file_list':fileList[i], 'revisionLength': revisionLength, 'dir_path': dir_path, 'granularity': granularity, 'start': start, 'end':end, 'instance_type':instance_type, 'l': l})
        
            else:
                processDict[i+1] = Process(target=self.__countRev, kwargs={'file_list':fileList[i], 'revisionLength': revisionLength, 'dir_path': dir_path, 'instance_type':instance_type,'l': l})                
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return revisionLength
    
    def __is_qa(self, file_name):
        with open(file_name, 'r') as myFile:
            for line in myFile:
                if '<KnowledgeData' in line and 'QA' in line: 
                    return True
    def get_instance_id(self, *args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            f = file_name.split('/')[-1]
            instance = {}
            
            context_wiki = ET.iterparse(file_name, events=("start","end"))
            # Turning it into an iterator
            context_wiki = iter(context_wiki)
            event_wiki, root_wiki = next(context_wiki)
            for event, elem in context_wiki:
                if event == "end" and 'Instance' in elem.tag:
                    if kwargs.get('type') == None:
                        if instance.get(f) == None:
                            instance[f] = []
                        else:
                            instance[f].append(elem['Id'])
                    elem.clear()
                    root_wiki.clear()
            return instance
        if kwargs.get('dir_path') != None:
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
            instance = {}
            if self.__is_qa(file_list[0]):
                for files in file_list:
                    f = files.split('/')[-1]
                    context_wiki = ET.iterparse(files, events=("start","end"))
                    # Turning it into an iterator
                    context_wiki = iter(context_wiki)
                    event_wiki, root_wiki = next(context_wiki)
                    for event, elem in context_wiki:
                        if event == "end" and 'Instance' in elem.tag:
                            if kwargs.get('type') == None:
                                instance[f] = []
                                instance[f].append(elem['Id'])
                            elif kwargs['type'] == 'accepted answer':
                                if elem.attrib.get('AcceptedAnswerId')!=None:
                                    instance[f] = []
                                    instance[f].append(elem.attrib['Id'])
                            elem.clear()
                            root_wiki.clear()           
                
            return instance         
                
            
    def get_wiki_talk_instance(self, *args, **kwargs):
        if kwargs.get('file_path')!=None:
            file_name = kwargs['file_path']
            rev = wikiExtract.get_wiki_revision(file_name)
            revisions = {}
            revisions[file_name.split('/')[-1]] = rev
        
        if kwargs.get('file_list')!=None:
            for file_name in kwargs['file_list']:
                rev = wikiExtract.get_wiki_revision(file_name)

                if(kwargs.get('revisions')!=None):  
                    if kwargs.get('dir_path')!=None:
                        file_name = file_name.replace(kwargs['dir_path']+'/','')
                    file_name = file_name[:-7].replace('_', ' ')
                    file_name = file_name.replace('__', '/')
                    kwargs['revisions'][file_name] = rev

    def get_wiki_talk_instances(self, *args, **kwargs):
        '''
        This piece of code is to ensure the multiprocessing
        Enter a date in YYYY-MM-DD format for start and end dates
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 4           # Bydefault it is 4
        
        fileNum = len(file_list)
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        

        manager = Manager()
        revisions = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):

            processDict[i+1] = Process(target=self.get_wiki_talk_instance, kwargs={'file_list':fileList[i], 'revisions': revisions, 'dir_path': dir_path,'l': l})                
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return revisions

    def __get_editor(self, *args, **kwargs):
        #print(file_name)
        if(kwargs.get('file_path')!=None):
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()

            uList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    for ch in child:
                        if('Instance' in ch.tag):
                            for newch in ch:
                                if('Contributors' in newch.tag):
                                    for chi in newch:
                                        if('OwnerUserId' in chi.tag):
                                            if(chi.text not in uList):
                                                uList.append(chi.text)
            return uList
            
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                context_wiki = ET.iterparse(f, events=("start","end"))
                # Turning it into an iterator
                context_wiki = iter(context_wiki)
                event_wiki, root_wiki = next(context_wiki)
                uList = []
                editor_dict = {}
                editor_bool = 0
                try:
                    for event, elem in context_wiki:
                        if event == "end" and 'Instance' in elem.tag:
                                for newch in elem:
                                    if 'TimeStamp' in newch.tag:
                                        for ch1 in newch:
                                            if 'CreationDate' in ch1.tag:
                                                date_format = "%Y-%m-%dT%H:%M:%S.%f"
                                                t = datetime.strptime(ch1.text, date_format)
                                                if kwargs.get('granularity')!=None:
                                                    if kwargs.get('start')!=None:
                                                        s = datetime.strptime(kwargs['start'], '%Y-%m-%d')
                                                        if t>s:
                                                            editor_bool = 1
                                                    if kwargs.get('end')!=None:
                                                        e = datetime.strptime(kwargs['end'], '%Y-%m-%d')
                                                        if t>e:
                                                            editor_bool = 0
                                                            continue
                                                    if kwargs['granularity'].lower() == 'monthly':
                                                        if editor_dict.get(t.year)==None:
                                                            editor_dict[t.year] = {}
                                                            editor_dict[t.year][t.month] = []
                                                        elif editor_dict[t.year].get(t.month)==None:
                                                            editor_dict[t.year][t.month] = []
                                                    elif kwargs['granularity'].lower() == 'yearly':
                                                            if editor_dict.get(t.year)==None:
                                                                editor_dict[t.year] = []
                                                    elif kwargs['granularity'].lower() == 'daily':
                                                            if editor_dict.get(t.year)==None:
                                                                editor_dict[t.year] = {}
                                                                editor_dict[t.year][t.month] = {}
                                                                editor_dict[t.year][t.month][t.day] = []
                                                            elif editor_dict[t.year].get(t.month)==None:
                                                                editor_dict[t.year][t.month] = {}
                                                                editor_dict[t.year][t.month][t.day] = []
                                                            elif editor_dict[t.year][t.month].get(t.day)==None:
                                                                editor_dict[t.year][t.month][t.day] = []
                                                            
                                    if('Contributors' in newch.tag):
                                        for chi in newch:
                                            if('OwnerUserName' in chi.tag):
                                                U = chi.text
                                                
                                            if editor_bool:
                                                
                                                if kwargs['granularity'].lower() != None:
                                                    if kwargs['granularity'].lower() == 'monthly':
                                                    
                                                        if U not in editor_dict[t.year][t.month]:
                                                            editor_dict[t.year][t.month].append(U)
                                                            
                                                    elif kwargs['granularity'].lower() == 'daily':
                                                        if U not in editor_dict[t.year][t.month][t.day]:
                                                            editor_dict[t.year][t.month][t.day].append(U)
                                                    
                                                    elif kwargs['granularity'].lower() == 'yearly':
                                                        if U not in editor_dict[t.year]:
                                                            editor_dict[t.year].append(U)
                                            else:
                                                if(U not in uList):
                                                    uList.append(U)
                                elem.clear()
                                root_wiki.clear()                                                            
                except:
                    print('problem with file parsing: '+f)
                if(kwargs.get('users')!=None):
                    if kwargs.get('dir_path')!=None:
                        f = f.replace(kwargs['dir_path']+'/','')
                    f = f[:-7].replace('_', ' ')
                    f = f.replace('__', '/')
                    if kwargs.get('granularity')==None:
                        kwargs['users'][f] = uList
                    else:
                        kwargs['users'][f] = editor_dict
                    
        else:
            print("No arguments provided")


    def get_editors(self, *args, **kwargs):

        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 24           # Bydefault it is 24
        
        fileNum = len(file_list)
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        
        manager = Manager()
        usersList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):    
            if kwargs.get('granularity') != None:
                granularity = kwargs['granularity']
                start = kwargs['start']
                end = kwargs['end']
                processDict[i+1] = Process(target=self.__get_editor, kwargs={'file_name':fileList[i],'users': usersList, 'granularity':granularity, 'start':start, 'end':end, 'dir_path': dir_path, 'l': l})
            else:
                processDict[i+1] = Process(target=self.__get_editor, kwargs={'file_name':fileList[i],'users': usersList, 'dir_path': dir_path, 'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return usersList

    def get_wiki_group_editors(self, group):
        '''
        This defination can be used to get the edits of a user in wikipedia
        '''
        if group=='bots':
            B = self.download_dataset('wikipedia',download=False, category_list=['All Wikipedia bots'])
            bot_list = []
            for i in B[0]['All Wikipedia bots']:
                bot_list.append(i['title'].replace('User:',''))
            return bot_list
    
    def get_author_similarity(self, editors, *args, **kwargs):
        if kwargs.get('similarity')!=None:
            similar = kwargs['similarity']
        
        if similar.lower()=='jaccard':
            s1 = []
            s2 = []
            similarity = {}
            for article, aval in editors.items():
                similarity[article] = {}
                try:
                    start = list(editors[article].keys())[0]
                    end = list(editors[article].keys())[-1]
                except:
                    continue
                for date in range(start, end):
                    similarity[article][date] = {}
                    for month in range(1,13):
                        similarity[article][date][month] = {}
                        for day in range(1,32):
                            try:
                                s1 = editors[article][date][month][day]
                            except:
                                s1 = []
                            stotal = []
                            sinter = []
                            for page, val in editors.items():
                                if page!=article:
                                    try:
                                        s2 = editors[page][date][month][day]
                                    except:
                                        s2 = []
                                    
                                    sinter = sinter+s2
                            
                            stotal = stotal+s1
                            try:
                                similarity[article][date][month][day] = len(set(s1) & set(sinter))/len(stotal)
                            except:
                                similarity[article][date][month][day] = 0
            return similarity
        
    def __chunks(self, l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

    def get_author_edits(self, *args, **kwargs):
        '''
        get_author_edits(site_name,[article_list, dir_path, editor_list, all_wiki=False])
        The following function is used to get the edits of each user
        all_wiki = if site_name = wikipedia then setting this varible True will get all the edits of the users of article
        article_list = list of file names (in knolml format)
        dir_path = path of the directory where all the files are present (in knolml format)
        editor_list = list of editor usernames for which edits are required
        type = type of edit to be measured e.g. bytes, edits, sentences. bytes by default
        ordered_by = means of ordering e.g. editor, questions, answers or article
        '''

        all_wiki = False
        if kwargs.get('article_list')!=None:
            article_list = kwargs['article_list']
        elif kwargs.get('dir_path')!=None:
            article_list = glob.glob(kwargs['dir_path']+'/*.knolml')
        elif kwargs.get('editor_list')!=None:
            editor_list = kwargs['editor_list']
            all_wiki = True
        author_contrib = {}
        if kwargs.get('type')!=None:
            type = kwargs['type']
        else:
            type = 'bytes'
        
        if kwargs.get('ordered_by')!=None:
            order = kwargs['ordered_by']
        else:
            order = 'editor'
        if not all_wiki:
            for article in article_list:
                context_wiki = ET.iterparse(article, events=("start","end"))
                # Turning it into an iterator
                context_wiki = iter(context_wiki)
                event_wiki, root_wiki = next(context_wiki)
                edit_bytes = 0
                editor = ''
                if kwargs.get('dir_path')!=None:
                    article_key = article.replace(kwargs['dir_path'], '')
                    article_key = article_key.replace('/', '')
                else:
                    article_key = article
                if order=='article':
                    author_contrib[article_key] = {}
                #try:
                for event, elem in context_wiki:
                    if event == "end" and 'Instance' in elem.tag:
                        editor_flag = 0
                        for ch1 in elem:
                            if 'Contributors' in ch1.tag:
                                for ch2 in ch1:
                                    if 'OwnerUserName' in ch2.tag:
                                        author = ch2.text
                                    elif 'OwnerUserId' in ch2.tag:
                                        author = ch2.text
                                        if order=='editor':
                                            editor_flag = 1
                                            if author_contrib.get(author)==None:
                                                author_contrib[author] = {}
                                                author_contrib[author][article_key] = 0
                                            elif author_contrib[author].get(article_key)==None:
                                                author_contrib[author][article_key] = 0
                                            
                                        elif order=='questions' and elem.attrib['InstanceType'] == 'Question':
                                            editor_flag = 1
                                            if author_contrib.get(author)==None:
                                                author_contrib[author] = 1

                                        elif order=='answers' and elem.attrib['InstanceType'] == 'Answer':
                                            editor_flag = 1
                                            if author_contrib.get(author)==None:
                                                author_contrib[author] = 1                                                        
                                            
                                        elif order=='article':
                                            editor_flag = 1
                                            if author_contrib[article_key].get(author)==None:
                                                author_contrib[article_key][author] = 0
                                        editor = author
                            
                            if 'Body' in ch1.tag and editor_flag==1:
                                if type=='bytes':
                                    for ch2 in ch1:
                                        if 'Text' in ch2.tag:
                                            diff = int(ch2.attrib['Bytes']) - edit_bytes
                                            if order == 'editor':
                                                author_contrib[editor][article_key] += diff
                                            elif order == 'questions':
                                                author_contrib[editor] += int(ch2.attrib['Bytes'])
                                            elif order == 'answer':
                                                author_contrib[editor] += int(ch2.attrib['Bytes'])
                                            elif order == 'article':
                                                author_contrib[article_key][editor] += diff
                                            edit_bytes = int(ch2.attrib['Bytes'])
                                elif type=='edits':
                                    if order == 'editor':
                                        author_contrib[editor][article_key] += 1
                                    elif order == 'questions':
                                        author_contrib[editor] += 1
                                    elif order == 'answer':
                                        author_contrib[editor] += 1
                                    elif order=='article':
                                        author_contrib[article_key][editor] += 1
                        
                        elem.clear()
                        root_wiki.clear()
                #except:
                    #print("error with file: "+article)
        
        else:
            we = wikiExtract()
            editor_extract = []
            for editor in editor_list:
                if len(editor.split('.')) > 3 or len(editor.split(':'))>3:
                    pass
                else:
                    editor_extract.append(editor)
            editors_name = self.__chunks(editor_extract,50)
            final_list = []
            for e in editors_name:
                final_list += we.get_author_wiki_edits(e)
            author_contrib = final_list
        
        return author_contrib
    
    def __get_reverts(self, file_name):

        context_wiki = ET.iterparse(file_name, events=("start","end"))
        # Turning it into an iterator
        context_wiki = iter(context_wiki)
        event_wiki, root_wiki = next(context_wiki)
        sha_dict = {}
        reverts_count = 0
        id = 1
        try:
            for event, elem in context_wiki:
                if event == "end" and 'Instance' in elem.tag:
                    for ch1 in elem:
                        if 'Knowl' in ch1.tag:
                            if ch1.attrib['key'] == 'sha':
                                if sha_dict.get(ch1.text)==None:
                                    sha_dict[ch1.text] = 0
                                else:
                                    reverts_count+=1
                    
                    id+=1
                    elem.clear()
                    root_wiki.clear()
        except:
            print("error in file parsing "+ file_name)        
        return reverts_count
    
    def get_wiki_revert(self, *args, **kwargs):
        if kwargs.get('file_path')!=None:
            file_name = kwargs['file_path']
            reverts_count = self.__get_reverts(file_name)

        
        if kwargs.get('file_list')!=None:
            for file_name in kwargs['file_list']:
        
                reverts_count = self.__get_reverts(file_name)

                if(kwargs.get('reverts')!=None):
                    if kwargs.get('dir_path')!=None:
                        file_name = file_name.replace(kwargs['dir_path']+'/','')
                    file_name = file_name[:-7].replace('_', ' ')
                    file_name = file_name.replace('__', '/')

                    kwargs['reverts'][file_name] = reverts_count

    def get_wiki_reverts(self, *args, **kwargs):

        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 4           # Bydefault it is 4
        
        fileNum = len(file_list)
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        manager = Manager()
        revertList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):    

            processDict[i+1] = Process(target=self.get_wiki_revert, kwargs={'file_list':fileList[i],'reverts': revertList, 'dir_path': dir_path, 'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return revertList                                    


    def getKnowledgeAge(self, *args, **kwargs):
        
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        
        if(kwargs.get('file_path')!=None):
            file_name = kwargs['file_path']
            context_wiki = ET.iterparse(file_name, events=("start","end"))
            # Turning it into an iterator
            context_wiki = iter(context_wiki)
            event_wiki, root_wiki = next(context_wiki)
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            try:
                for event, elem in context_wiki:
                    if event == "end" and 'Instance' in elem.tag:
                        for newch in elem:
                            if 'TimeStamp' in newch.tag:
                                for ch1 in newch:
                                    if 'CreationDate' in ch1.tag:
                                        firstDate = ch1.text
                                        firstDate = datetime.strptime(date_format, ch1.text)
                                        flag = 1
                        if(flag):
                            break
                currentDate = datetime.strptime(datetime.today().strftime(date_format), date_format)
                
                articleAge = currentDate - firstDate 
            except:
                print("problem with file ", file_name)
                
            return articleAge
        
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                context_wiki = ET.iterparse(f, events=("start","end"))
                # Turning it into an iterator
                context_wiki = iter(context_wiki)
                event_wiki, root_wiki = next(context_wiki)
                date_format = "%Y-%m-%dT%H:%M:%S.%f"
                firstDate = ''
                articleAge = ''
                try:
                    for event, elem in context_wiki:
                        if event == "end" and 'Instance' in elem.tag:
                            for newch in elem:
                                if 'TimeStamp' in newch.tag:
                                    for ch1 in newch:
                                        if 'CreationDate' in ch1.tag:
                                            firstDate = datetime.strptime(ch1.text, date_format)
                                            flag = 1
                            if(flag):
                                break
                    currentDate = datetime.strptime(datetime.today().strftime(date_format), date_format)
                    
                    articleAge = currentDate - firstDate
                    if kwargs.get('date')!=None:
                        currentDate = datetime.strptime(kwargs['date'], '%Y-%m-%d')
                    else:
                        currentDate = datetime.strptime(datetime.today().strftime(date_format), date_format)
                    
                    articleAge = currentDate - firstDate
                except:
                    print("problem with file ", f)
                if(kwargs.get('articleAge')!=None):
                   
                    f = f.split('/')[-1]
                    f = f[:-7].replace('_', ' ')
                    f = f.replace('__', '/')
                    kwargs['articleAge'][f] = articleAge
                
     
    
    def get_age_of_knowledge(self, *args, **kwargs):

        '''
        This piece of code is to ensure the multiprocessing
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        fileNum = len(file_list)
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24
        
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
            
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        

        
        manager = Manager()
        ageList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            if kwargs.get('date')!=None:
                processDict[i+1] = Process(target=self.getKnowledgeAge, kwargs={'file_name':fileList[i],'articleAge': ageList, 'date':kwargs['date'], 'l': l})        
            else:
                processDict[i+1] = Process(target=self.getKnowledgeAge, kwargs={'file_name':fileList[i],'articleAge': ageList, 'l': l})
                
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return ageList        

    
    def __return_edit_stats(self, revision, prevTotalLinks, prevRevision, result):
        # revision, prevTotalLinks, prevRevision
        currRevision = revision
        code = mwparserfromhell.parse(currRevision)
        externalLinks = code.filter_external_links()
        wikiLinks = code.filter_wikilinks()

        for i in range(len(externalLinks)):
            externalLinks[i] = str(externalLinks[i])
        for i in range(len(wikiLinks)):
            wikiLinks[i] = str(wikiLinks[i])

        externalLinks = list(set(externalLinks))
        wikiLinks = list(set(wikiLinks))
        totalLinks = []
        for each in externalLinks:
            totalLinks.append(each)
        for each in wikiLinks:
            totalLinks.append(each)

        if totalLinks != prevTotalLinks:
            if len(totalLinks) > len(prevTotalLinks):
                result['Hyperlink Added'] += 1
            elif len(totalLinks) < len(prevTotalLinks):
                result['Hyperlink Deleted'] += 1
            else:
                result['Hyperlink Fixed'] += 1

        if currRevision != prevRevision:
            if len(word_tokenize(currRevision)) > len(word_tokenize(prevRevision)):
                result['Content Added'] += 1
            elif len(word_tokenize(currRevision)) < len(word_tokenize(prevRevision)):
                result['Content Deleted'] += 1
            else:
                result['Content Reorganised'] += 1
        prevRevision = currRevision
        prevTotalLinks = totalLinks
        return result
    
    def revisionEdits(self, file_name, slab):
        revlength = 0
        with open(file_name, 'r') as myFile:
            for line in myFile:
                if '<KnowledgeData' in line:
                    if 'compressed' in line:
                        compressed = True
                        print('compressed true')
                    else:
                        print('compressed false')
                        compressed = False
                    if 'Wiki' in line:
                        wiki=True
                        print('wiki true')
                    else:
                        wiki=False
                if 'Instance' in line:
                    revlength += 1
                    
        result = {
            'Number of Words': 0,
            'Number of Sentences': 0,
            'Number of Wikilinks': 0,
            'Number of PNs': 0,
            'Content Added': 0,
            'Content Deleted': 0,
            'Content Reorganised': 0,
            'Hyperlink Added': 0,
            'Hyperlink Deleted': 0,
            'Hyperlink Fixed': 0
        }
        revlength = int(revlength/slab)
        prevRevision = ''
        prevTotalLinks = []
        count = 1
        slabNo = 1 
        slabs = {}

        if wiki==True and compressed==True:
            tree = ET.parse(file_name)
            root = tree.getroot()
            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child
            
            revisionList = knol.getAllRevisions(file_name)
            for rev in revisionList:
                revisions = knol.wikiRetrieval(file_name,rev)
                for revision in revisions:
                    result = self.__return_edit_stats(revision, prevTotalLinks, prevRevision, result)
                    if count%revlength == 0:
                        slabs['Slab'+str(slabNo)] = copy.deepcopy(result)
                        slabNo += 1

                    count += 1
            return slabs

        if wiki==True and compressed==False:
            print('inside this function')
            count = 1
            context_wiki = ET.iterparse(file_name, events=("start","end"))
            # Turning it into an iterator
            context_wiki = iter(context_wiki)
            event_wiki, root_wiki = next(context_wiki)
            try:
                for event, elem in context_wiki:
                    if event == "end" and 'Instance' in elem.tag:
                        for ch1 in elem:
                            if 'Body' in ch1.tag:
                                for ch2 in ch1:
                                    if 'Text' in ch2.tag:
                                        revision = ch2.text
                                        result = self.__return_edit_stats(revision, prevTotalLinks, prevRevision, result)
                                        if count%revlength == 0:
                                            slabs['Slab'+str(slabNo)] = copy.deepcopy(result)
                                            slabNo += 1
                    
                                        count += 1
                        elem.clear()
                        root_wiki.clear()
            
            except:
                print('error in file parsing')    
            return slabs                

        if wiki==False:
            length = 0
            content = {}
            hyperlink = {}
            s1 = []
            s2 = []
            totalLinks = 0
            slabs = {}
            if slab < length:
                revlength = int(length/slab)
            else:
                revlength = 1
            count = 0
            slabNo = 1
            for child in root:
                if 'Instance' in child.tag:
                    if 'RevisionId' in child.attrib:
                        revisionId = child.attrib['RevisionId']
                    else:
                        # This means its a comment
                        continue

                    for each in child:
                        if 'Body' in each.tag:
                            for i in each:
                                if 'Text' in i.tag:
                                    s = re.findall(r'(http?://\S+)', i.text)

                                    if len(s) != 0: #If Hyperlink is found
                                        if revisionId in hyperlink:
                                            if len(hyperlink[revisionId]) < len(s):
                                                result['Hyperlink Added'] += 1
                                            elif len(hyperlink[revisionId]) > len(s):
                                                result['Hyperlink Deleted'] += 1
                                            elif len(hyperlink[revisionId]) == len(s) and hyperlink[revisionId] != s:
                                                result['Hyperlink Fixed'] += 1
                                        else:
                                            result['Hyperlink Added'] += 1                                        
                                        hyperlink[revisionId] = s

                                    if revisionId in content:
                                        #check if content is added or not
                                        if len(content[revisionId]) < len(i.text):
                                            result['Content Added'] += 1
                                        elif len(content[revisionId]) > len(i.text):
                                            result['Content Deleted'] += 1
                                        elif len(content[revisionId]) == len(i.text) and content[revisionId] != i.text:
                                            result['Content Reorganised'] += 1
                                         
                                    else:
                                        #content is added
                                        result['Content Added'] += 1

                                    content[revisionId] = i.text

                    if count%revlength == 0:
                        slabs['Slab'+str(slabNo)] = copy.deepcopy(result)
                        slabNo += 1

                count += 1

            return slabs


    
    def get_revision_type(self, *args, **kwargs):
        if kwargs.get('slab')!=None:
            slab = kwargs['slab']
        else:
            slab = 1
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            return self.revisionEdits(file_name, slab)

        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            for f in file_name:
                if(kwargs.get('RevisionEdits')!=None):
                    kwargs['RevisionEdits'][f] = self.revisionEdits(f, slab)


    def get_revision_types(self, *args, **kwargs):
        all_var = knol.__get_multiprocessing(*args, **kwargs)
        # revisionId, file_list, pNum
        fileList = all_var[1]
        pNum = all_var[2]
        if kwargs.get('slab') != None:
            slab = kwargs['slab']
        else:
            slab = 1

        manager = Manager()
        RevisionEdits = manager.dict()

        l = Lock()
        processDict = {}
 
        for i in range(pNum):
            processDict[i+1] = Process(target=self.revisionTypes, kwargs={'file_name':fileList[i],'RevisionEdits': RevisionEdits, 'slab':slab, 'l': l})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()

        return RevisionEdits

    #yet to complete this method
    def __text_stats(self, *args, **kwargs):
        if kwargs.get('file_name') != None:
            for f in kwargs['file_name']:
                context_wiki = ET.iterparse(f, events=("start","end"))
                # Turning it into an iterator
                context_wiki = iter(context_wiki)
                event_wiki, root_wiki = next(context_wiki)
                try:
                    for event, elem in context_wiki:
                        if event == "end" and 'Instance' in elem.tag:
                            for ch1 in elem:
                                if 'Body' in ch1.tag:
                                    text = ch1.text
                except:
                    print('error in file parsing')
    #not yet working for Wikipedia
    #yet to complete this method
    def get_text_stats(self, *args, **kwargs):
        if kwargs.get('sitename')==None:
            print('please provide the sitename as argument')
        elif kwargs['sitename']=='stackexchange':
            if kwargs.get('dir_path')==None:
                print('provide the directory path')
            else:
                dir_path = kwargs['dir_path']
                all_var = knol.__get_multiprocessing(*args, **kwargs)
                fileList = all_var[1]
                pNum = all_var[2]
                manager = Manager()
                text_edits = manager.dict()
                l = Lock()
                processDict = {}
         
                for i in range(pNum):
                    processDict[i+1] = Process(target=self.__text_stats, kwargs={'file_name':fileList[i],'text_edits': text_edits, 'l': l})
        
                for i in range(pNum):
                    processDict[i+1].start()
        
                for i in range(pNum):
                    processDict[i+1].join()
        
                return text_edits
            
  
    def get_stack_posts(self, dir_path, post_type, *args, **kwargs):
        if kwargs.get('order_by')!=None:
            order = kwargs['order_by']
            if order.lower() == 'recent':
                if os.path.isdir(dir_path+'/Posts'):
                    file_list = sorted(glob.glob(dir_path+'/Posts/*.knolml'), key=self.numericalSort)
                else:
                    print("provide the path for stack exchange knolml dataset")
                
    
    @staticmethod
    def knowledgeByDate(file_name, first_date, *args, **kwargs):
        
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        
        fe = 0
        d_f = "%Y-%m-%d"
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        first_date = datetime.strptime(first_date, d_f)
        if(kwargs.get('end_date')!=None):
            end_date = kwargs['end_date']
            end_date = datetime.strptime(end_date, d_f)
            fe=1
                        
        tree = ET.parse(file_name)            
        root = tree.getroot()
        length = 0
        revList = []
        dummyList = []
        flag = 0
        wikiFlag = 0
        for child in root:
            if('KnowledgeData' in child.tag):
                length = len(child.findall('Instance'))
                if('Wiki' in child.attrib['Type']):
                    wikiFlag = 1
                for ch1 in child:
                    if('Instance' in ch1.tag):
                        instanceId = ch1.attrib['Id']
                        for ch2 in ch1:
                            if('TimeStamp' in ch2.tag):
                                for ch3 in ch2:
                                    if('CreationDate' in ch3.tag):
                                        firstDate = datetime.strptime(ch3.text, date_format)
                                        if(firstDate >= first_date):
                                            flag=1
                                            
                                        
                                        if(fe==1 and firstDate>end_date):
                                            flag=0
                            
                            if('Body' in ch2.tag):
                                for ch4 in ch2:
                                    if('Text' in ch4.tag and flag==1):
                                        if(wikiFlag==1):
                                            dummyList.append(int(instanceId))
                                        else:
                                            revList.append(ch4.text)
        
        if(wikiFlag==1):
            k = int((math.log(length)) ** 2)
            for i in range(k+1,(math.ceil(length/(k+1))-1)*(k+1)+1,(k+1)):
                if(i in dummyList):
                    revList.append(i)
            if(length in dummyList):
                revList.append(length)
        return revList

    @staticmethod
    def getUrl(*args, **kwargs):
        
        href_regex = r'href=[\'"]?([^\'" >]+)'
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        
        if(kwargs.get('file_path')!=None):
            
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()    
            
            urlList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    if('Wiki' in child.attrib['Type'] and 'revision' in child.attrib['Type']):
                        length = len(child.findall('Instance'))
                        revision = knol.getRevision(file_name,length)
                        urls = re.findall(href_regex, revision)
                        for ur in urls:
                            urlList.append(ur)
                        
                        return urlList
                        
                    for ch1 in child:
                        if('Instance' in ch1.tag):
                            for ch2 in ch1:
                                if('Body' in ch2.tag):
                                    for ch3 in ch2:
                                        if('Text' in ch3.tag):
                                            urls = re.findall(href_regex, ch3.text)
                                            
                                            for ur in urls:
                                                urlList.append(ur)                                            
            
            return urlList
        
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()    
                urlList = []
                for child in root:
                    if('KnowledgeData' in child.tag):
                        for ch1 in child:
                            if('Instance' in ch1.tag):
                                for ch2 in ch1:
                                    if('Body' in ch2.tag):
                                        for ch3 in ch2:
                                            if('Text' in ch3.tag):
                                                urls = re.findall(href_regex, ch3.text)
                                                
                                                for ur in urls:
                                                    urlList.append(ur)                                            
                if(kwargs.get('url_list')!=None):
                    kwargs['url_list'][f] = urlList


    @staticmethod
    def countWords(*args, **kwargs):
        #t1 = time.time()
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        if(kwargs.get('lastRev')!=None):
            lastRev = kwargs['lastRev']
        dummyDict = {}
        if(kwargs.get('file_path')!=None):
            
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()    
            wordCount = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    if('Wiki' in child.attrib['Type']):
                        if('compressed' in child.attrib['Type']):
                            if(lastRev):
                                length = len(child.findall('Instance'))
                                revision = knol.getRevision(file_name,length)
                                Text = knol.getCleanText(revision)
                                wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                wordCount.append(wordNum)                        
                            else:
                                revisionList = knol.getAllRevisions(file_name)
                                for rev in revisionList:
                                    revisions = knol.wikiRetrieval(file_name,rev)
                                    for revision in revisions:
                                        Text = knol.getCleanText(revision)
                                        wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                        wordCount.append(wordNum)

                        else:
                            context_wiki = ET.iterparse(file_name, events=("start","end"))
                            # Turning it into an iterator
                            context_wiki = iter(context_wiki)
                            
                            # getting the root element
                            event_wiki, root_wiki = next(context_wiki)
                            
                            for event, elem in context_wiki:
                                if event == "end" and 'Instance' in elem.tag:
                                    for body in elem:
                                        if('Body' in body.tag):
                                            for textt in body:
                                                if('Text' in textt.tag):
                                                    wordNum = len(re.sub('['+string.punctuation+']', '', textt.text).split())
                                                    wordCount.append(wordNum)
                                    elem.clear()
                                    root_wiki.clear() 


                    elif('QA' in child.attrib['Type']):
                        print('yes')
                        if(lastRev):
                            for ch1 in child:
                                if('Instance' in ch1.tag):
                                    for ch2 in ch1:
                                        if('Body' in ch2.tag):
                                            for ch3 in ch2:
                                                if('Text' in ch3.tag):
                                                    Text = ch3.text
                        
                        
                        Text = knol.getCleanText(Text)
                        wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                        
                            
            
            if(kwargs.get('wordCount')!=None):
                kwargs['wordCount'][file_name] = wordCount
            

                                    
                        
            
        
        elif(kwargs.get('file_name')!=None):
            #print('yes')
            file_name = kwargs['file_name']
            #print('file name is: ',file_name)
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()                                                    
                wordCount = []
                for child in root:
                    if('KnowledgeData' in child.tag):
                        if('Wiki' in child.attrib['Type']):
                            if('compressed' in child.attrib['Type']):
                                if(lastRev):
                                    length = len(child.findall('Instance'))
                                    revision = knol.getRevision(f,length)
                                    Text = knol.getCleanText(revision)
                                    wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                    wordCount.append(wordNum)                        
                                else:
                                    revisionList = knol.getAllRevisions(f)
                                    for rev in revisionList:
                                        revisions = knol.wikiRetrieval(f,rev)
                                        for revision in revisions:
                                            Text = knol.getCleanText(revision)
                                            wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                            wordCount.append(wordNum)
    
                            else:
                                context_wiki = ET.iterparse(f, events=("start","end"))
                                # Turning it into an iterator
                                context_wiki = iter(context_wiki)
                                
                                # getting the root element
                                event_wiki, root_wiki = next(context_wiki)
                                
                                for event, elem in context_wiki:
                                    if event == "end" and 'Instance' in elem.tag:
                                        for body in elem:
                                            if('Body' in body.tag):
                                                for textt in body:
                                                    if('Text' in textt.tag):
                                                        wordNum = len(re.sub('['+string.punctuation+']', '', textt.text).split())
                                                        wordCount.append(wordNum)
                                        elem.clear()
                                        root_wiki.clear()
                                        
                                        
                        elif('QA' in child.attrib['Type']):
                            if(lastRev):
                                for ch1 in child:
                                    if('Instance' in ch1.tag):
                                        for ch2 in ch1:
                                            if('Body' in ch2.tag):
                                                for ch3 in ch2:
                                                    if('Text' in ch3.tag):
                                                        Text = ch3.text
                            
                            
                            Text = knol.getCleanText(Text)
                            wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                            
                                  
                
                if(kwargs.get('wordCount')!=None):
                    kwargs['wordCount'][f] = wordCount
                else:
                    #x = 0
                    dummyDict[f] = wordCount
                
            
            #t2 = time.time()
            #print(t2-t1)

    @staticmethod
    def countAllWords(*args, **kwargs):
        #t1 = time.time()
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
            
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        if(kwargs.get('last_rev')!=None):
            if(kwargs['last_rev']==True):
                lastRev = True
        else:
            lastRev = False
            
        fileNum = len(file_list)
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24
        
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
            
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        

        
        manager = Manager()
        countList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knol.countWords, kwargs={'file_name':fileList[i],'wordCount': countList, 'lastRev':lastRev,'l': l})
            #processDict[i+1] = Process(target=self.countWords, kwargs={'file_name':fileList[i], 'lastRev':lastRev,'l': l})
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
        
        '''
        t2 = time.time()
        print(t2-t1)
        '''
        return countList 
        

    @staticmethod
    def Infobox(*args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            tree = ET.parse(file_name)
            root = tree.getroot()

            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child

            try:
                revisionId = kwargs['revision_id']
            except:
                revisionId = len(root.findall('Instance'))

            wikiText = knol.getRevision(file_name, revisionId)

            if wikiText.find('{{Infobox') != -1:
                return 1
            else:
                return 0


        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)
                root = tree.getroot()

                for child in root:
                    if('KnowledgeData' in child.tag):
                        root = child

                try:
                    revisionId = kwargs['revision_id'][f]
                except:
                    revisionId = len(root.findall('Instance'))

                wikiText = knol.getRevision(f, revisionId)

                if wikiText.find('{{Infobox') != -1:
                    check = 1
                else:
                    check = 0

                if(kwargs.get('Infobox')!=None):
                    kwargs['Infobox'][f] = check

    @staticmethod
    def __get_multiprocessing(*args, **kwargs):
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        if kwargs.get('revision_id') != None:
            revisionId = kwargs['revision_id']
        else:
            revisionId = None

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24

        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])

        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        

        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        all_var = []
        all_var.append(revisionId)
        all_var.append(fileList)
        all_var.append(pNum)
        
    @staticmethod
    def checkInfobox(*args, **kwargs):

        '''
        This piece of code is to ensure the multiprocessing
        '''
        all_var = knol.__get_multiprocessing(*args, **kwargs)
        # revisionId, file_list, pNum
        revisionId = all_var[0]
        fileList = all_var[1]
        pNum = all_var[2]
        l = Lock()
        processDict = {}            
        manager = Manager()
        Infobox = manager.dict()
        for i in range(pNum):
            processDict[i+1] = Process(target=knol.Infobox, kwargs={'file_name':fileList[i],'Infobox': Infobox,'l': l, 'revision_id': revisionId})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()  
   
        return Infobox


    @staticmethod
    def countImages(*args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            tree = ET.parse(file_name)
            root = tree.getroot()

            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child

            try:
                revisionId = kwargs['revision_id']
            except:
                revisionId = len(root.findall('Instance'))

            wikiText = knol.getRevision(file_name, revisionId)

            countImages = 0
            imageFormates = ['.jpg','.jpeg','.svg','.gif','.png','.bmp','.tiff']
            for image in imageFormates:
                countImages += wikiText.count(image)

            return countImages  


        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            count = 0
            imageFormates = ['.jpg','.jpeg','.svg','.gif','.png','.bmp','.tiff']
            for f in file_name:
                tree = ET.parse(f)
                root = tree.getroot()

                for child in root:
                    if('KnowledgeData' in child.tag):
                        root = child

                try:
                    revisionId = kwargs['revision_id'][f]
                except:
                    revisionId = len(root.findall('Instance'))

                wikiText = knol.getRevision(f, revisionId)
                count += 1

                countImages = 0
                for image in imageFormates:
                    countImages += wikiText.count(image)

                if(kwargs.get('images')!=None):
                    kwargs['images'][f] = countImages


    @staticmethod
    def getNumberOfImages(*args, **kwargs):

        '''
        This piece of code is to ensure the multiprocessing
        '''
        all_var = knol.__get_multiprocessing(*args, **kwargs)
        # revisionId, file_list, pNum
        revisionId = all_var[0]
        fileList = all_var[1]
        pNum = all_var[2]


        manager = Manager()
        Images = manager.dict()

        l = Lock()
        processDict = {}
        for i in range(pNum):
            processDict[i+1] = Process(target=knol.countImages, kwargs={'file_name':fileList[i],'images': Images,'l': l, 'revision_id': revisionId})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()

        return Images


    @staticmethod
    def gini(array):
        array = array.flatten()
        if np.amin(array) < 0:
            array -= np.amin(array)
        for i in array:
            i += 0.0000001
        array = np.sort(array)
        index = np.arange(1,array.shape[0]+1)
        n = array.shape[0]
        return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))


    @staticmethod
    def getContributions(file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()

        for child in root:
            if('KnowledgeData' in child.tag):
                root = child

        contributors = {}
        #editor=''
        for child in root:
            if('Instance' in child.tag):
                for newch in child:
                    if('Contributors' in newch.tag):
                        for chi in newch:
                            if('OwnerUserId' in chi.tag):
                                editor = chi.text

                    if('Body' in newch.tag):
                        for chi in newch:
                            if('Text' in chi.tag):
                                editLength = int(chi.attrib['Bytes'])

                try:
                    if editor not in contributors:
                        contributors[editor] = editLength
                    else:
                        contributors[editor] += editLength
                except:
                    #print(file_name)
                    continue

        s = []
        for each in contributors:
            s.append(float(contributors[each]))

        return s


    @staticmethod
    def localGiniCoefficient(*args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            p = np.array(knol.getContributions(file_name))
            giniValue = knol.gini(p)
            return giniValue

        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            for f in file_name:
                p = np.array(knol.getContributions(f))
                if(len(p)==0):
                    giniValue = -1
                else:
                    giniValue = knol.gini(p)

                if(kwargs.get('GiniValues')!=None):
                    kwargs['GiniValues'][f] = giniValue


    @staticmethod
    def getLocalGiniCoefficient(*args, **kwargs):

        all_var = knol.__get_multiprocessing(*args, **kwargs)
        # revisionId, file_list, pNum
        revisionId = all_var[0]
        fileList = all_var[1]
        pNum = all_var[2]


        manager = Manager()
        GiniValues = manager.dict()

        l = Lock()
        processDict = {}
        for i in range(pNum):
            processDict[i+1] = Process(target=knol.localGiniCoefficient, kwargs={'file_name':fileList[i],'GiniValues': GiniValues,'l': l})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()
        
        return GiniValues
    

    def globalGini(self, *args, **kwargs):
        if kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            
        if(kwargs.get('l')!=None):
            l = kwargs['l']

        if(kwargs.get('contributors')==None):
            contributors = {}

        for f in file_name:
            tree = ET.parse(f)
            root = tree.getroot()

            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child
            editor=''
            for child in root:
                if('Instance' in child.tag):
                    for newch in child:
                        if('Contributors' in newch.tag):
                            for chi in newch:
                                if('OwnerUserId' in chi.tag):
                                    editor = chi.text
                                elif('LastEditorUserId' in chi.tag):
                                    editor = chi.text

                        if('Body' in newch.tag):
                            for chi in newch:
                                if('Text' in chi.tag):
                                    editLength = int(chi.attrib['Bytes'])
                                    
                    if(kwargs.get('contributors')!=None):
                        if kwargs['contributors'].get(editor)==None:
                            l.acquire()
                            kwargs['contributors'][editor] = editLength
                            l.release()
                            #x = 0
                        else:
                            l.acquire()
                            kwargs['contributors'][editor] += editLength
                            l.release()
                            #x=1
                    
                    else:
                        if contributors.get(editor)==None:
                            l.acquire()
                            contributors[editor] = editLength
                            l.release()
                        else:
                            l.acquire()
                            contributors[editor] += editLength
                            l.release()
                            
        
        
        
     
        #print(t2-t1)
        
        if(kwargs.get('contributors')==None):
            s = []
            for each in contributors:
                s.append(float(contributors[each]))
    
            p = np.array(s)
            giniValue = knol.gini(p)
            return giniValue            
            
    def get_global_gini_coefficient(self, *args, **kwargs):
    
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<4):
            cnum = fileNum+1           # Bydefault it is 4
        else:
            cnum = 4


        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])

        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())


        manager = Manager()
        contributors = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=self.globalGini, kwargs={'file_name':fileList[i],'contributors': contributors,'l': l})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()



        s = []
        for key,items in contributors.items():
            s.append(float(contributors[key]))

        p = np.array(s)
        giniValue = knol.gini(p)
        

        return giniValue
    
    
    @staticmethod
    def findTags(*args, **kwargs):
        #print(list_tags)
        if(kwargs.get('list_tags')!=None):
            list_tags = kwargs['list_tags']

        if(kwargs.get('l')!=None):
            lock = kwargs['l']            

            
        #print(list_tags)        
        if(kwargs.get('file_path')!=None):
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()
    
           
    
            uList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    for ch in child:
                        if('Instance' in ch.tag):
                            for newch in ch:
                                if('Contributors' in newch.tag):
                                    for chi in newch:
                                        if('OwnerUserId' in chi.tag):
                                            if(chi.text not in uList):
                                                uList.append(chi.text)
            return uList
            
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()
                postList = []
                for child in root:
                    if('KnowledgeData' in child.tag):
                        for ch in child:
                            if('Instance' in ch.tag):
                                for newch in ch:
                                    if('Body' in newch.tag):
                                        for txt in newch:
                                            if('Text' in txt.tag):                                            
                                                postList.append(txt.text)                            
                                    
                                    if('Tags' in newch.tag):
                                        
                                        if(list_tags in newch.text):
                                            print(f +': '+ list_tags)
                                            if(kwargs.get('tagPosts')!=None):
                                                kwargs['tagPosts'][f] = []
                                            continue
                                        else:
                                            postList = []
                                            
                                            
                                            
    
    
                if(kwargs.get('tagPosts')!=None):
                    '''
                    if(kwargs['tagPosts'].get(f)!=None):
                        kwargs['tagPosts'][f] = postList
                    '''
                    if(kwargs['tagPosts'].get(f)!=None):
                        lock.acquire()
                        with open(list_tags+'.txt', 'a') as newFile:
                            newFile.write(f +': ')
                            newFile.write(str(postList))
                            newFile.write('\n')
                            postList = []
                        lock.release()                    


        else:
            print("No arguments provided")    
    
    @staticmethod
    def findAllTags(list_tags,*args, **kwargs):
        #t1 = time.time()
        
        
        all_var = knol.__get_multiprocessing(*args, **kwargs)
        # revisionId, file_list, pNum
        revisionId = all_var[0]
        fileList = all_var[1]
        pNum = all_var[2]
        
        
    
        
        manager = Manager()
        tagPosts = manager.dict()
    
        l = Lock()
        processDict = {}
        for i in range(pNum):
            processDict[i+1] = Process(target=knol.findTags, kwargs={'list_tags':list_tags,'file_name':fileList[i],'tagPosts':tagPosts,'l': l})
            
            #processDict[i+1] = Process(target=self.countWords, kwargs={'file_name':fileList[i], 'lastRev':lastRev,'l': l})
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
        
        '''
        t2 = time.time()
        print(t2-t1)
        '''
        return tagPosts 


    # Graph methods starts here. Please check the graph_creater function for more information
    def get_graph_by_wikiarticle(self, article_name):
        '''
        **Does not require dataset download**
        
        This method takes an article name as an argument and creates the induced subgraph
        among the articles present in there.
        
        *Arguments*
        article_name:
            Type: String
            The name of the article for which the interwiki graph has to be created.
        
        e.g knol.get_graph_by_name('India')
        '''
        gc.get_graph_by_name(article_name)
        
        
    def get_graph_by_wikiarticle_list(self, article_list, *args, **kwargs):
        '''
        **Does not require dataset download**
        
        This method takes a list of articles name as an argument and creates the induced subgraph
        among the articles using the wikilinks.
        
        *Arguments*
        article_list:
            Type: List of strings
            The list of articles name for which the interwiki graph has to be created.
        file_name:
            optional
            file name by which you want to create the graph
        eg. knol.get_graph_by_wikiarticle_list(['India', 'Pakistan'], file_name='relation')
        '''
        if kwargs.get('file_name')!=None:
            file_name = kwargs['file_name']+'.graphml'
            gc.get_inter_graph(article_list, file_name=file_name)
        else:
            gc.get_inter_graph(article_list)


    def get_graph_by_wikiarticle_countries(self, *args, **kwargs):
        '''
        **Does not require dataset download**
        
        This method creates the induced subgraph among the articles of all the 
        wikipedia pages of all the countries using the wikilinks.
        
        *Arguments*
        country_list:
            optional
            Type: List of strings
            The list of countries name for which the interwiki graph has to be created.
            When not set, the graph is created for all the countries
        
        e.g knol.get_graph_by_wikiarticle_countries()

        '''
        if kwargs.get('country_list')!=None:
            country_list = kwargs['country_list']
            gc.all_countries_graph(country_list=country_list)
        else:
            gc.all_countries_graph()
            

    def get_graph_by_wikiarticle_cities(self, country_name):
        '''
        **Does not require dataset download**
        
        This method creates the induced subgraph among the articles of all the 
        wikipedia pages of all the cities of a given country using the wikilinks.
        
        *Arguments*
        country_name:
            Type: string
            The country name for which the city graph has to be created.
            
        
        e.g knol.get_graph_by_wikiarticle_cities('United States')

        '''
        gc.get_cities_by_country(country_name)
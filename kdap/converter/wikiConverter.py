#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:56:24 2019

@author: descentis
"""

import os
from multiprocessing import Process, Lock
import time
import numpy as np
import glob
import difflib
import xml.etree.ElementTree as ET
import math
import textwrap
import html
import requests
import io

class wikiConverter(object):


    instance_id = 1
    
    
    def indent(self,elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    @staticmethod
    def wiki_file_writer(elem,myFile,prefix):
        global instance_id
        t = '\t'
    
        Instance = t+t+"<Instance "
        
      
        for ch_elem in elem:        
                        
            if(('id' in ch_elem.tag) and ('parentid' not in ch_elem.tag)):             
                Instance = Instance+ "Id="+'"'+str(wikiConverter.instance_id)+'"'+" InstanceType="+'"'+"Revision/Wiki"+'"'+" RevisionId="+ '"'+str(ch_elem.text)+'"'+">\n"
                myFile.write(Instance)
                
                '''
                RevisionId = t+t+t+"<RevisionId>"+ch_elem.text+"</RevisionId>\n"
                myFile.write(RevisionId)
                '''
            
            '''
            if(ch_elem.tag==prefix+'parentid'):
                ParentId = t+t+t+"<ParentId>"+ch_elem.text+"</ParentId>\n" 
                myFile.write(ParentId)
            '''
                
    
                
            
                      
            
            '''
            Timestamp Information
            '''
            if('timestamp' in ch_elem.tag):
                '''
                if(f_p!=1):
                    Instance = Instance+" InstanceType= "+'"'+"wiki/text"+'"'+">\n"
                    myFile.write(Instance)
                '''
                Timestamp = t+t+t+"<TimeStamp>\n"
                myFile.write(Timestamp)
                CreationDate = t+t+t+t+"<CreationDate>"+ch_elem.text[:-1]+'.0'+"</CreationDate>\n"
                myFile.write(CreationDate)
                Timestamp = t+t+t+"</TimeStamp>\n"
                myFile.write(Timestamp)            
                
                
            '''
            Contributors information
            '''
            if('contributor' in ch_elem.tag):            
                Contributors = t+t+t+"<Contributors>\n"
                myFile.write(Contributors)
                for contrib in ch_elem:
                    if('ip' in contrib.tag):
                        LastEditorUserName = t+t+t+t+"<OwnerUserName>"+html.escape(contrib.text)+"</OwnerUserName>\n"
                        myFile.write(LastEditorUserName)                        
                    else:
                        if('username' in contrib.tag):
                            try:
                                LastEditorUserName = t+t+t+t+"<OwnerUserName>"+html.escape(contrib.text)+"</OwnerUserName>\n"
                            except:
                                LastEditorUserName = t+t+t+t+"<OwnerUserName>None</OwnerUserName>\n"
                            myFile.write(LastEditorUserName)                        
                        if(('id' in contrib.tag) and ('parentid' not in contrib.tag)):
                            LastEditorUserId = t+t+t+t+"<OwnerUserId>"+contrib.text+"</OwnerUserId>\n"
                            myFile.write(LastEditorUserId)
                    
                        
                Contributors = t+t+t+"</Contributors>\n"
                myFile.write(Contributors)
            
            
            '''
            Body/Text Information
            '''
            if('text' in ch_elem.tag):
                Body = t+t+t+"<Body>\n"
                myFile.write(Body)
                if(ch_elem.attrib.get('bytes')!=None):
                    text_field = t+t+t+t+"<Text Type="+'"'+"wiki/text"+'"'+" Bytes="+'"'+ch_elem.attrib['bytes']+'">\n'
                elif(ch_elem.text != None):
                    text_field = t+t+t+t+"<Text Type="+'"'+"wiki/text"+'"'+" Bytes="+'"'+str(len(ch_elem.text))+'">\n'
                else:
                    text_field = t+t+t+t+"<Text Type="+'"'+"wiki/text"+'"'+" Bytes="+'"'+str(0)+'">\n'
                myFile.write(text_field)
                if(ch_elem.text == None):                
                    text_body = "";
                else:
                   
                    text_body = textwrap.indent(text=ch_elem.text, prefix=t+t+t+t+t)
                    text_body = html.escape(text_body)
                Body_text = text_body+"\n"
                myFile.write(Body_text)
                text_field = t+t+t+t+"</Text>\n"
                myFile.write(text_field)        
                Body = t+t+t+"</Body>\n"
                myFile.write(Body)            
            
    
            
            if('comment' in ch_elem.tag):
                Edit = t+t+t+"<EditDetails>\n"
                myFile.write(Edit)
                if(ch_elem.text == None):                
                    text_body = "";
                else:
                    text_body = textwrap.indent(text=ch_elem.text, prefix=t+t+t+t+t)
                    text_body = html.escape(text_body)
                
                EditType = t+t+t+t+"<EditType>\n"+text_body+"\n"+t+t+t+t+"</EditType>\n"
                #Body_text = text_body+"\n"
                myFile.write(EditType)
                
                Edit = t+t+t+"</EditDetails>\n"
                myFile.write(Edit)    
    
            if('sha1' in ch_elem.tag):
                sha = ch_elem.text
                if(type(sha)!=type(None)):
                    shaText = t+t+t+'<Knowl key="sha">'+sha+'</Knowl>\n'
                    myFile.write(shaText)
                else:
                    shaText = ''
                
        Instance = t+t+"</Instance>\n"
        myFile.write(Instance)  
        wikiConverter.instance_id+=1             
 
    @staticmethod
    def wiki_knolml_converter(name, *args, **kwargs):
        #global instance_id
        #Creating a meta file for the wiki article
        
        
        
        # To get an iterable for wiki file

        file_name = name
        context_wiki = ET.iterparse(file_name, events=("start","end"))
        # Turning it into an iterator
        context_wiki = iter(context_wiki)
        
        # getting the root element
        event_wiki, root_wiki = next(context_wiki)
        file_name = name[:-4]+'.knolml'
        file_path = file_name
        if kwargs.get('output_dir')!=None:
            file_path = file_path.replace('output','wikipedia_articles')
        
        if not os.path.exists(file_path):
            with open(file_path,"w",encoding='utf-8') as myFile:
                myFile.write("<?xml version='1.0' encoding='utf-8'?>\n")
                myFile.write("<KnolML>\n")
                myFile.write('<Def attr.name="sha" attrib.type="string" for="Instance" id="sha"/>\n')
               
            prefix = '{http://www.mediawiki.org/xml/export-0.10/}'    #In case of Wikipedia, prefic is required
            f = 0
            title_text = ''
            try:
                for event, elem in context_wiki:
                    
                    if event == "end" and 'id' in elem.tag:
                        if(f==0):
                            with open(file_path,"a",encoding='utf-8') as myFile:
                                 myFile.write("\t<KnowledgeData "+"Type="+'"'+"Wiki/text/revision"+'"'+" Id="+'"'+elem.text+'"'+">\n")
                                 
                            f=1
                                
                    if event == "end" and 'title' in elem.tag:
                        title_text = elem.text
            
                    if(f==1 and title_text!=None):            
                        Title = "\t\t<Title>"+title_text+"</Title>\n"
                        with open(file_path,"a",encoding='utf-8') as myFile:
                            myFile.write(Title)
                        title_text = None
                    if event == "end" and 'revision' in elem.tag:
                 
                        with open(file_path,"a",encoding='utf-8') as myFile:
                            wikiConverter.wiki_file_writer(elem,myFile,prefix)
                            
                            
                        elem.clear()
                        root_wiki.clear() 
            except:
                print("found problem with the data: "+ file_name)
        
            with open(file_path,"a",encoding='utf-8') as myFile:
                myFile.write("\t</KnowledgeData>\n")
                myFile.write("</KnolML>\n") 
        
            wikiConverter.instance_id = 1


    @staticmethod
    def is_number(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def encode(str1, str2):
    	output = ""
    	s = [x.replace("\n", "`").replace("-", "^") for x in str1.split(" ")]
    
    	s2 = [x.replace("\n", "`").replace("-", "^") for x in str2.split(" ")]
    
    	i = 0
    	while(True):
    		if i == len(s):
    			break;
    		if s[i].isspace() or s[i] == '':
    			del s[i]
    		else:	
    			i += 1	
    	i = 0
    	while(True):
    		if i == len(s2):
    			break;
    		if s2[i].isspace() or s2[i] == '':
    			del s2[i]
    		else:	
    			i += 1	
    			
    	d = difflib.Differ()
    
    	result = list(d.compare(s, s2))
    
    	pos = 0
    	neg = 0
    
    	for x in result:
    		if x[0] == " ":
    			pos += 1
    			if neg != 0:
    				output += "-"+str(neg)+" "
    				neg = 0
    		elif x[0] == "-":
    			neg += 1
    			if pos != 0:
    				output += str(pos)+" "
    				pos = 0	
    		elif x[0] != "?":
    			if pos != 0:
    				output += str(pos)+" "
    				pos = 0	
    			if neg != 0:
    				output += "-"+str(neg)+" "
    				neg = 0
    			if wikiConverter.is_number(x[2:]):
    				output += "'"+x[2:]+"' "
    			else:			
    				output += x[2:]+" "
    	if pos != 0:
    		output += str(pos)+" "
    	if neg != 0:
    		output += "-"+str(neg)+" "
    	return output.replace("\t\t\t", "")
    
    #Main function
    
    @staticmethod
    def compress(file_name, directory):
    	# file_name = input("Enter path of KML file:")
    
        tree = ET.parse(file_name)
        r = tree.getroot()
        for child in r:
            if('KnowledgeData' in child.tag):
                child.attrib['Type'] = 'Wiki/text/revision/compressed'
                root = child
                
        last_rev = ""
        length = len(root.findall('Instance'))
    
        print(length, "revisions found")
    
        count = 0
        intervalLength =  int((math.log(length)) ** 2);  
    
        # Keep the Orginal text after every 'm' revisions
        m = intervalLength+1
        for each in root.iter('Text'):
            count += 1
            if m != intervalLength+1:
                current_str = each.text
                each.text = wikiConverter.encode(prev_str, current_str)
                prev_str = current_str
                # print("Revision ", count, " written")
    			
                m = m - 1
                if m == 0:
                    m = intervalLength+1
            else:
                prev_str = each.text
                # print("Revision ", count, " written")
                m = m - 1
                continue
    
        print("KnolML file created")
    	
        # Creating directory 
        if not os.path.exists(directory):
            os.mkdir(directory)
    
        # Changing file path to include directory
        file_name = file_name.split('/')
        file_name = directory+'/'+file_name[-1]
        '''
        file_name.insert(-1, directory)
        separator = '/'
        file_name = separator.join(file_name)
        '''
    
        tree.write(file_name[:-7]+'.knolml')
        f = open(file_name[:-7]+'.knolml')
        f_str = f.read()
        f.close()
    
        f2 = open(file_name[:-7]+'.knolml', "w")
        f2.write("<?xml version='1.0' encoding='utf-8'?>\n"+f_str)
        f2.close()
    
    
    @staticmethod
    def wikiConvert(*args, **kwargs):

        if(kwargs.get('output_dir')!=None):
            output_dir = kwargs['output_dir']        
        if(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            wikiConverter.wiki_knolml_converter(file_name)
            file_name = file_name[:-4] + '.knolml'
            wikiConverter.compress(file_name,output_dir)
            os.remove(file_name)            
       
        if(kwargs.get('file_list')!=None):
            path_list = kwargs['file_list']
            for file_name in path_list:            
                wikiConverter.wiki_knolml_converter(file_name)
                file_name = file_name[:-4] + '.knolml'
                wikiConverter.compress(file_name,output_dir)
                os.remove(file_name)
        
        if((kwargs.get('file_name')==None) and (kwargs.get('file_list')==None)):
            print("No arguments provided")
    
    def returnList(self, l, n):
        for i in range(0,len(l),n):
            yield l[i:i+n]

    @staticmethod
    def __file_lists(fileNum,c_num,fileNames):
        fileList = []
        if(fileNum<c_num):
            for f in fileNames:
                fileList.append([f])
        
        else:           

            f = np.array_split(fileNames,c_num)
            for i in f:
                fileList.append(i.tolist())
        
        return fileList
     
    @staticmethod
    def compressAll(dir_path, *args, **kwargs):
        t1 = time.time()
        if(kwargs.get('c_num')!=None):
            c_num = kwargs['c_num']
        else:
            c_num = 4              # By default it is 4
        fileNames = glob.glob(dir_path+'/*.xml')
        if(kwargs.get('output_dir')!=None):
            output_dir=kwargs['output_dir']
        else:
            output_dir = os.getcwd()
        fileNum = len(fileNames)   
        fileList = wikiConverter.__file_lists(fileNum, c_num, fileNames)
        l = Lock()
        processDict = {}
        if(fileNum<c_num):
            pNum = fileNum
        else:
            pNum = c_num
        for i in range(pNum):
            processDict[i+1] = Process(target=wikiConverter.wikiConvert,kwargs={'output_dir':output_dir,'file_list': fileList[i],'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()
        
        
        t2 = time.time()
        
        print("All process done with time: ",str(t2-t1))

    @staticmethod
    def convertwiki(*args, **kwargs):

        if(kwargs.get('output_dir')!=None):
            output_dir = kwargs['output_dir']        
        if(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            wikiConverter.wiki_knolml_converter(file_name,output_dir=output_dir)
            file_name = file_name[:-4] + '.knolml'
            #wikiConverter.compress(file_name,output_dir)
            #os.remove(file_name)            
       
        if(kwargs.get('file_list')!=None):
            path_list = kwargs['file_list']
            for file_name in path_list:            
                wikiConverter.wiki_knolml_converter(file_name, output_dir=output_dir)
                file_name = file_name[:-4] + '.knolml'
                #wikiConverter.compress(file_name,output_dir)
                #os.remove(file_name)
        
        if((kwargs.get('file_name')==None) and (kwargs.get('file_list')==None)):
            print("No arguments provided")
            

    @staticmethod
    def convertall(dir_path, *args, **kwargs):
        t1 = time.time()
        if(kwargs.get('c_num')!=None):
            c_num = kwargs['c_num']
        else:
            c_num = 4              # By default it is 4
        fileNames = glob.glob(dir_path+'/*.xml')
        if(kwargs.get('output_dir')!=None):
            output_dir=kwargs['output_dir']
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = os.getcwd()
        fileNum = len(fileNames)
        fileList = wikiConverter.__file_lists(fileNum, c_num, fileNames)
        l = Lock()
        processDict = {}
        if(fileNum<c_num):
            pNum = fileNum
        else:
            pNum = c_num
        for i in range(pNum):
            processDict[i+1] = Process(target=wikiConverter.convertwiki,kwargs={'output_dir':output_dir,'file_list': fileList[i],'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()
        
        
        t2 = time.time()
        
        print("All process done with time: ",str(t2-t1))        
        
        
    @staticmethod    
    def getArticle(*args, **kwargs):
    	# articleName = raw_input()
    	# articleName = articleName.replace(' ', '_')
        featuredArticleList = []
        if(kwargs.get('file_name')!=None):
            featuredArticleList.append(kwargs['file_name'])            
       
        if(kwargs.get('file_list')!=None):
            featuredArticleList = kwargs['file_list']
            
        if(kwargs.get('output_dir')!=None):
            output_dir = kwargs['output_dir']+'/'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = ''
    
        for each in featuredArticleList:
            articleName = each
            articleName = articleName.replace(' ','_')
            articleName = articleName.replace('/','__')
            file_handler = io.open(output_dir+articleName+'.xml', mode='w+', encoding='utf-8')
            url = 'https://en.m.wikipedia.org/w/index.php?title=Special:Export&pages=' + articleName + '&history=1&action=submit'
            headers = {
			'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
            }
            print('Downloading ' + articleName + '...') 
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                xml = r.text
                file_handler.write(xml)
                print(articleName,'Completed!')
            else:
                print('Something went wrong! ' + articleName + '\n' + '\n')
            
            file_handler.close()
            wikiConverter.wiki_knolml_converter(output_dir+articleName+'.xml')    
    
    @staticmethod    
    def serialCompress(self,dir_path, *args, **kwargs):
        t1 = time.time()
        file_list = os.listdir(dir_path)
        path_list = []
        
        if(kwargs.get('output_dir')!=None):
            output_dir=kwargs['output_dir']
        else:
            output_dir = os.getcwd()
        for f in file_list:
            path_list.append(dir_path+'/'+f)
        
        self.convert(path_list,output_dir=output_dir)
        t2 = time.time()
        
        print("all process done: ",str(t2-t1))
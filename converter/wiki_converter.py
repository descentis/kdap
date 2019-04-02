#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 21:48:53 2018

@author: descentis
"""

import xml.etree.cElementTree as ET
import textwrap
import html

'''
This function is used to indent the xml; document is pretty style
'''

instance_id = 1

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def wiki_file_writer(elem,myFile,prefix):
    global instance_id
    t = '\t'

    Instance = t+t+"<Instance "
    
  
    for ch_elem in elem:        
                    
        if(('id' in ch_elem.tag) and ('parentid' not in ch_elem.tag)):             
            Instance = Instance+ "Id="+'"'+str(instance_id)+'"'+" InstanceType="+'"'+"Revision/Wiki"+'"'+" RevisionId="+ '"'+str(ch_elem.text)+'"'+">\n"
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
                        LastEditorUserName = t+t+t+t+"<OwnerUserName>"+html.escape(contrib.text)+"</OwnerUserName>\n"
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
                shaText = t+t+t+'<data key="sha">'+sha+'</data>\n'
                myFile.write(shaText)
            else:
                shaText = ''
            
    Instance = t+t+"</Instance>\n"
    myFile.write(Instance)  
    instance_id+=1             

def wiki_knml_converter(name):
    global instance_id
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
    with open(file_path,"w",encoding='utf-8') as myFile:
        myFile.write("<?xml version='1.0' encoding='utf-8'?>\n")
        myFile.write("<KnolML>\n")
        myFile.write('<key attr.name="sha" attrib.type="string" for="Instance" id="sha"/>\n')
       
    prefix = '{http://www.mediawiki.org/xml/export-0.10/}'    #In case of Wikipedia, prefic is required
    f = 0
    title_text = ''
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
                wiki_file_writer(elem,myFile,prefix)
                
                
            elem.clear()
            root_wiki.clear() 

    with open(file_path,"a",encoding='utf-8') as myFile:
        myFile.write("\t</KnowledgeData>\n")
        myFile.write("</KnolML>\n") 

    instance_id = 1
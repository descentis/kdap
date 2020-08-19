#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:29:07 2018

@author: descentis
"""

import xml.etree.cElementTree as ET
import textwrap
import html
import os.path
from datetime import datetime
import glob
from subprocess import call
import errno
import os
from internetarchive import download

class qaConverter(object):
    
    def __init__(self):
        self.random = 'just to check'
        print(self.random)
    
    @staticmethod
    def getPostType(name):
        # To get an iterable
        n1 = name.split('/')
        postFile = n1[0]+'/Posts.xml'
        context_post = ET.iterparse(postFile, events=("start", "end"))
        # turning it into an iterator
        context_post = iter(context_post)
        
        # get the root element
        event_posts, root_posts = next(context_post)
        
        postType = {}
        for event, elem in context_post:
            if event == "end" and elem.tag == "row":
                li = []
                if(elem.attrib.get('ParentId')!=None):
                    
                    li.append(elem.attrib['PostTypeId'])
                    li.append(elem.attrib['ParentId'])
                    postType[elem.attrib['Id']] = li
                else:
                    li.append(elem.attrib['PostTypeId'])
                    postType[elem.attrib['Id']] = li
           
                elem.clear()     
                root_posts.clear()
        
        return postType    
    
    @staticmethod
    def make_path(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise    

    @staticmethod
    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                qaConverter.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    @staticmethod
    def tag_remover(body):
        for i in body:
            if(i=='<'):
                body = body.replace(i,"")
            if(i=='>'):
                body = body.replace(i,", ")
        return body
    
    
    @staticmethod
    def writeHistoryData(*args, **kwargs):
        elem = kwargs['elem']
        post_id = kwargs['post_id']
        instanceId = kwargs['instanceId']
        HistoryType = kwargs['HistoryType']
        postType = kwargs['postType']
        val = kwargs['val']
        name = kwargs['name']
        filePath = name+'/'
        if(val==1 and postType[0]!='2'):
            filePath = filePath+"Post"+str(post_id)+".knolml"
            
            with open(filePath,"w",encoding='utf-8') as myFile:
                myFile.write("<?xml version='1.0' encoding='utf-8'?>\n")
                myFile.write("<KnolML>\n") 
                myFile.write("\t<KnowledgeData "+"Type="+'"'+"QA/text"+'"'+" Id= "+'"'+str(post_id)+'"'+">\n")
                t = '\t'
                f2 = 0
                if(postType[0]!='2'):
                    Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"InstanceType= "+'"Revision/Question" '+"RevisionId= "+ '"'+str(elem.attrib['RevisionGUID'])+'"'+">\n"
                    myFile.write(Instance)
                    f2 = 1
                elif(postType[0]=='2'):
                    Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"OriginalId= "+'"'+str(post_id)+'"'+" "+"InstanceType= "+'"Revision/Answer" '+"RevisionId= "+ '"'+str(elem.attrib['RevisionGUID'])+'"'+">\n"                
                    myFile.write(Instance)
                    f2=1
    
                
                
                if(f2==1):
        
                    '''
                    Timestamp information
                    '''
                
                    qaConverter.__write_timestamp(myFile, elem)
        
        
                    '''
                    Contributors information
                    '''
                    
                    
                    Contributors = t+t+t+"<Contributors>\n"
                    myFile.write(Contributors)
                    if(elem.attrib.get("UserId") != None):
                        Contributors =t+t+t+t+"<OwnerUserId>"+elem.attrib['UserId']+"</OwnerUserId>\n"
                        myFile.write(Contributors)
                    Contributors = t+t+t+"</Contributors>\n"
                    myFile.write(Contributors)


                    '''
                    PostHistory might have a comment associated with each entry.
                    I have added that section as editDetails
                    '''
        
                    Edit = t+t+t+"<EditDetails>\n"
                    myFile.write(Edit)
                    
                    if(HistoryType.get(int(elem.attrib['PostHistoryTypeId']))!=None):
                        EditType = t+t+t+t+"<EditType>"+HistoryType[int(elem.attrib['PostHistoryTypeId'])]+"</EditType>\n"
                    else:
                        EditType = t+t+t+t+"<EditType>Unknown</EditType>\n"
                    myFile.write(EditType)
        
                    if(elem.attrib.get('Comment')!=None):
                        text_body = textwrap.indent(text=elem.attrib['Comment'], prefix=t+t+t+t)
                        text_body = html.escape(text_body)
                        Body_text = text_body+"\n"
                        EditType = t+t+t+t+"<EditComment>"+Body_text+"</EditComment>\n"
                        myFile.write(EditType)
                    Edit = t+t+t+"</EditDetails>\n"
                    myFile.write(Edit)
                    
        
                    '''
                    Writing the body/text part
                    '''
                    if(elem.attrib.get('Text')!=None):        
                        Body = t+t+t+"<Body>\n"
                        myFile.write(Body)
                        text_field = t+t+t+t+"<Text Type= "+'"'+"text"+'"'+" Bytes="+'"'+str(len(elem.attrib['Text']))+'">\n'
                        myFile.write(text_field)
                        if(elem.attrib['PostHistoryTypeId']=="3" or elem.attrib['PostHistoryTypeId']=="6"):            
                            body_text = elem.attrib['Text']
                            body_text = qaConverter.tag_remover(body_text)
                            text_body = textwrap.indent(text=body_text, prefix=t+t+t+t+t)
                            text_body = html.escape(text_body)
                        else:
                            text_body = textwrap.indent(text=elem.attrib['Text'], prefix=t+t+t+t+t)
                            text_body = html.escape(text_body)
                        Body_text = text_body+"\n"
                        myFile.write(Body_text)
                        text_field = t+t+t+t+"</Text>\n"
                        myFile.write(text_field)        
                        Body = t+t+t+"</Body>\n"
                        myFile.write(Body)
        

                    
                    Instance = t+t+"</Instance>\n"
                    myFile.write(Instance)
                     
                    
        
        else:
            f = 0
            if(postType[0]!='2'):
                filePath = filePath+"Post"+str(post_id)+".knolml"
                f = 1
            elif(postType[0]=='2'):
                
                filePath = filePath+"Post"+str(postType[1])+".knolml"
                f = 1
    
            
            if(f==1):
                with open(filePath,"a",encoding='utf-8') as myFile:
                    t = '\t'
                    if(postType[0]=='1'):
                        Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"InstanceType= "+'"Revision/Question" '+"RevisionId= "+ '"'+str(elem.attrib['RevisionGUID'])+'"'+">\n"
                    else:
                        Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"OriginalId= "+'"'+str(post_id)+'"'+" "+"InstanceType= "+'"Revision/Answer" '+"RevisionId= "+ '"'+str(elem.attrib['RevisionGUID'])+'"'+">\n"
                    myFile.write(Instance)
                    
        
        
                    '''
                    Timestamp information
                    '''
                
                    qaConverter.__write_timestamp(myFile, elem)
        
        
                    '''
                    Contributors information
                    '''
                    
                    
    
                    if(elem.attrib.get("UserId") != None):
                        Contributors = t+t+t+"<Contributors>\n"
                        myFile.write(Contributors)
                        Contributors =t+t+t+t+"<OwnerUserId>"+elem.attrib['UserId']+"</OwnerUserId>\n"
                        myFile.write(Contributors)
                        Contributors = t+t+t+"</Contributors>\n"
                        myFile.write(Contributors)
                    
        
                    '''
                    Writing the body/text part
                    '''
                    if(elem.attrib.get('Text')!=None):        
                        Body = t+t+t+"<Body>\n"
                        myFile.write(Body)
                        text_field = t+t+t+t+"<Text Type= "+'"'+"text"+'"'+" Bytes="+'"'+str(len(elem.attrib['Text']))+'">\n'
                        myFile.write(text_field)
                        if(elem.attrib['PostHistoryTypeId']=="3" or elem.attrib['PostHistoryTypeId']=="6"):            
                            body_text = elem.attrib['Text']
                            body_text = qaConverter.tag_remover(body_text)
                            text_body = textwrap.indent(text=body_text, prefix=t+t+t+t+t)
                            text_body = html.escape(text_body)
                        else:
                            text_body = textwrap.indent(text=elem.attrib['Text'], prefix=t+t+t+t+t)
                            text_body = html.escape(text_body)
                        Body_text = text_body+"\n"
                        myFile.write(Body_text)
                        text_field = t+t+t+t+"</Text>\n"
                        myFile.write(text_field)        
                        Body = t+t+t+"</Body>\n"
                        myFile.write(Body)
        
                    '''
                    PostHistory might have a comment associated with each entry.
                    I have added that section as editDetails
                    '''
        
                    Edit = t+t+t+"<EditDetails>\n"
                    myFile.write(Edit)
                    
                    if(HistoryType.get(int(elem.attrib['PostHistoryTypeId']))!=None):
                        EditType = t+t+t+t+"<EditType>"+HistoryType[int(elem.attrib['PostHistoryTypeId'])]+"</EditType>\n"
                    else:
                        EditType = t+t+t+t+"<EditType>Unknown</EditType>\n"
                    myFile.write(EditType)
        
                    if(elem.attrib.get('Comment')!=None):
                        text_body = textwrap.indent(text=elem.attrib['Comment'], prefix=t+t+t+t+t)
                        text_body = html.escape(text_body)
                        Body_text = text_body+"\n"
                        EditType = t+t+t+t+"<EditComment>\n"
                        myFile.write(EditType)
                        myFile.write(Body_text)
                        EditType = t+t+t+t+"</EditComment>\n"
                        myFile.write(EditType)
                    Edit = t+t+t+"</EditDetails>\n"
                    myFile.write(Edit)        
    
                    Instance = t+t+"</Instance>\n"
                    myFile.write(Instance)
    
    
    @staticmethod
    def postHistoryConversion(name):
    
        # To get an iterable
        n1 = name.split('/')
        postHistoryFile = n1[0]+'/PostHistory.xml'
        context_postHistory = ET.iterparse(postHistoryFile, events=("start", "end"))
        # turning it into an iterator
        context_postHistory = iter(context_postHistory)
        
        # get the root element
        event_posts, root_posts = next(context_postHistory)
    
        # Dictionary of postHistoryType
        HistoryType = {1:'Initial Title',2:'Initial Body',3:'Initial Tags',4:'Edit Title',5:'Edit Body',6:'Edit Tags',7:'Rollback Title',8:'Rollback Body',
                       9:'Rollback Tags',10:'Post Closed',11:'Post Reopened',12:'Post Deleted',13:'Post Undeleted',14:'Post Locked',15:'Post Unlocked',
                       16:'Community Owned',17:'Post Migrated',18:'Question Merged',19:'Question Protected',20:'Question Unprotected',21:'Post Disassociated',
                       22:'Question Unmerged'}
        
        postIdBuffer = {}
        postType = qaConverter.getPostType(name)
        
        instanceId = 1
        for event, elem in context_postHistory:
            if event == "end" and elem.tag == "row":
                post_id = elem.attrib['PostId']
    
                if(postType[post_id][0]=='1'):
                    if(postIdBuffer.get(post_id)==None):
                        postIdBuffer[post_id] = 1
                        # elem,post_id,instanceId,HistoryType,postType,val,name
                        qaConverter.writeHistoryData(elem=elem, post_id=post_id, instanceId=postIdBuffer[post_id], HistoryType=HistoryType, postType=postType[post_id], val=1, name=name)
                    else:
                        postIdBuffer[post_id]+=1
                        qaConverter.writeHistoryData(elem=elem, post_id=post_id, instanceId=postIdBuffer[post_id], HistoryType=HistoryType, postType=postType[post_id], val=2, name=name)
                    
                    instanceId+=1
                elif(postType[post_id][0]=='2'):
                    if(postIdBuffer.get(post_id)==None):
                        if(postIdBuffer.get(postType[post_id][1])!=None):
                            postIdBuffer[postType[post_id][1]] += 1
                            qaConverter.writeHistoryData(elem=elem,post_id=post_id,instanceId=postIdBuffer[postType[post_id][1]],HistoryType=HistoryType,postType=postType[post_id],val=1,name=name)
                        
                    else:
                        if(postIdBuffer.get(postType[post_id][1])!=None):
                            postIdBuffer[postType[post_id][1]]+=1
                            qaConverter.writeHistoryData(elem=elem,post_id=post_id,instanceId=postIdBuffer[postType[post_id][1]],HistoryType=HistoryType,postType=postType[post_id],val=2,name=name)
                    instanceId+=1
                    
                else:
                    if(postIdBuffer.get(post_id)==None):
                        postIdBuffer[post_id] = 1
                        qaConverter.writeHistoryData(elem=elem,post_id=post_id,instanceId=postIdBuffer[post_id],HistoryType=HistoryType,postType=postType[post_id],val=1,name=name)
                    else:
                        postIdBuffer[post_id]+=1
                        qaConverter.writeHistoryData(elem=elem,post_id=post_id,instanceId=postIdBuffer[post_id],HistoryType=HistoryType,postType=postType[post_id],val=2,name=name)
                    
                    instanceId+=1                    

                elem.clear()
                root_posts.clear()
        

        '''
        file_list = glob.glob(name+"/*.knolml")
        for file_path in file_list:
            if(os.path.isfile(file_path)):
                with open(file_path,"a",encoding='utf-8') as myFile:
                    myFile.write("\t</KnowledgeData>\n")
                    myFile.write("</KnolML>\n")           
        
        '''
        return postType
        
    @staticmethod
    def write_body_rep(elem, myFile):
        '''
        Contributors information
        '''
        
        t = '\t'
        Contributors = t+t+t+"<Contributors>\n"
        myFile.write(Contributors)
        if(elem.attrib.get("OwnerUserId") != None):
            Contributors =t+t+t+t+"<OwnerUserId>"+elem.attrib['OwnerUserId']+"</OwnerUserId>\n"
            myFile.write(Contributors)

        if(elem.attrib.get("LastEditorUserId") != None):
            Contributors =t+t+t+t+"<LastEditorUserId>"+elem.attrib['LastEditorUserId']+"</LastEditorUserId>\n"
            myFile.write(Contributors)
        Contributors = t+t+t+"</Contributors>\n"
        myFile.write(Contributors)


        '''
        PostHistory might have a comment associated with each entry.
        I have added that section as editDetails
        

        Edit = t+t+t+"<EditDetails>\n"
        myFile.write(Edit)
        
        if(HistoryType.get(int(elem.attrib['PostHistoryTypeId']))!=None):
            EditType = t+t+t+t+"<EditType>"+HistoryType[int(elem.attrib['PostHistoryTypeId'])]+"</EditType>\n"
        else:
            EditType = t+t+t+t+"<EditType>Unknown</EditType>\n"
        myFile.write(EditType)

        if(elem.attrib.get('Comment')!=None):
            text_body = textwrap.indent(text=elem.attrib['Comment'], prefix=t+t+t+t)
            text_body = html.escape(text_body)
            Body_text = text_body+"\n"
            EditType = t+t+t+t+"<EditComment>"+Body_text+"</EditComment>\n"
            myFile.write(EditType)
        Edit = t+t+t+"</EditDetails>\n"
        myFile.write(Edit)
        '''
        

        '''
        Writing the body/text part
        '''
        if(elem.attrib.get('Body')!=None):        
            Body = t+t+t+"<Body>\n"
            myFile.write(Body)
            text_field = t+t+t+t+"<Text Type= "+'"'+"text"+'"'+" Bytes="+'"'+str(len(elem.attrib['Body']))+'">\n'
            myFile.write(text_field)

            body_text = elem.attrib['Body']
            #body_text = self.tag_remover(body_text)
            text_body = html.escape(body_text)
            text_body = textwrap.indent(text=text_body, prefix=t+t+t+t+t)
            

            Body_text = text_body+"\n"
            myFile.write(Body_text)
            text_field = t+t+t+t+"</Text>\n"
            myFile.write(text_field)        
            Body = t+t+t+"</Body>\n"
            myFile.write(Body)

        
        if(elem.attrib.get('Tags')!=None):
            Tags_element = t+t+t+"<Tags>"+html.escape(elem.attrib['Tags'])+"</Tags>\n"
            
            myFile.write(Tags_element)
        
        Reputation_tag = t+t+t+"<Credit> \n"
        myFile.write(Reputation_tag)
        if(elem.attrib.get("Score") != None):
            score = t+t+t+t+"<Score>"+elem.attrib['Score']+"</Score>\n"
            myFile.write(score)
        if(elem.attrib.get("ViewCount") != None):
            ViewCount = t+t+t+t+"<ViewCount>"+elem.attrib['ViewCount']+"</ViewCount>\n"
            myFile.write(ViewCount)
        if(elem.attrib.get("AnswerCount") != None):        
            AnswerCount = t+t+t+t+"<AnswerCount>"+elem.attrib['AnswerCount']+"</AnswerCount>\n"
            myFile.write(AnswerCount)
        if(elem.attrib.get("CommentCount") != None):
            CommentCount = t+t+t+t+"<CommentCount>"+elem.attrib['CommentCount']+"</CommentCount>\n"
            myFile.write(CommentCount)
    
        if(elem.attrib.get("FavouriteCount") != None):
            FavouriteCount = t+t+t+t+"<FavouriteCount>"+elem.attrib['FavouriteCount']+"</FavouriteCount>\n"
            myFile.write(FavouriteCount)
    
        Reputation_tag = t+t+t+"</Credit> \n"
        myFile.write(Reputation_tag)        

        
        Instance = t+t+"</Instance>\n"
        myFile.write(Instance)


    '''
    Writing the data for posts
    '''
    @staticmethod
    def __write_timestamp(myFile, elem):
        t = '\t'
        '''
        Timestamp information
        '''
    
        TimeStamp = t+t+t+"<TimeStamp>\n "
        myFile.write(TimeStamp)
        if(elem.attrib.get("CreationDate") != None):
            CreationDate = t+t+t+t+"<CreationDate>"+elem.attrib['CreationDate']+"</CreationDate> \n"
            myFile.write(CreationDate)
        if(elem.attrib.get("LastEditDate") != None):
            LastEditDate = t+t+t+t+"<LastEditDate>"+elem.attrib['LastEditDate']+"</LastEditDate> \n"
            myFile.write(LastEditDate)
        if(elem.attrib.get("LastActivityDate") != None):
            LastActivityDate = t+t+t+t+"<LastActivityDate>"+elem.attrib['LastActivityDate']+"</LastActivityDate> \n"
            myFile.write(LastActivityDate)
        if(elem.attrib.get("CommunityOwnedDate") != None):
            CommunityOwnedDate = t+t+t+t+"<CommunityOwnedDate>"+elem.attrib['CommunityOwnedDate']+"</CommunityOwnedDate> \n"
            myFile.write(CommunityOwnedDate)
        if(elem.attrib.get("ClosedDate") != None):
            ClosedDate = t+t+t+t+"<ClosedDate>"+elem.attrib['ClosedDate']+"</ClosedDate> \n"
            myFile.write(ClosedDate)
        TimeStamp = t+t+t+"</TimeStamp>\n "
        myFile.write(TimeStamp)
        
    @staticmethod
    def writePostData(*args, **kwargs):
        # elem,post_id,instanceId,postType,val,name
        elem = kwargs['elem']
        post_id = kwargs['post_id']
        instanceId = kwargs['instanceId']
        postType = kwargs['postType']
        val = kwargs['val']
        name = kwargs['name']
        filePath = name+'/'
        if(val==1 and postType[0]!='2'):
            filePath = filePath+"Post"+str(post_id)+".knolml"
            
            with open(filePath,"w",encoding='utf-8') as myFile:
                t = '\t'
                myFile.write("<?xml version='1.0' encoding='utf-8'?>\n")
                myFile.write("<KnolML>\n") 
                myFile.write("\t<KnowledgeData "+"Type="+'"'+"QA/text"+'"'+" Id= "+'"'+str(post_id)+'"'+">\n")
                if(elem.attrib.get('Title')!=None):
                    myFile.write(t+t+"<Title>"+html.escape(elem.attrib['Title'])+"</Title>\n")
                
                f2 = 0
                if(postType[0]!='2'):
                    Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"InstanceType= "+'"Question"'+">\n"
                    myFile.write(Instance)
                    f2 = 1
                elif(postType[0]=='2'):
                    Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"OriginalId= "+'"'+str(post_id)+'"'+" "+"InstanceType= "+'"Answer"'+">\n"                
                    myFile.write(Instance)
                    f2=1
    
                
                
                if(f2==1):
        
                    qaConverter.__write_timestamp(myFile, elem)
        
                    
                    qaConverter.write_body_rep(elem,myFile)
                    
        
        else:
            f = 0
            if(postType[0]!='2'):
                filePath = filePath+"Post"+str(post_id)+".knolml"
                f = 1
            elif(postType[0]=='2'):
                
                filePath = filePath+"Post"+str(postType[1])+".knolml"
                f = 1
    
            
            if(f==1):
                with open(filePath,"a",encoding='utf-8') as myFile:
                    t = '\t'
                    if(postType[0]=='1'):
                        Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"InstanceType= "+'"Question"'+">\n"
                    else:
                        Instance = t+t+"<Instance Id= "+'"'+str(instanceId)+'"'+" "+"OriginalId= "+'"'+str(post_id)+'"'+" "+"InstanceType= "+'"Answer"'+">\n"
                    myFile.write(Instance)
                    
        
        
                    '''
                    Timestamp information
                    '''
                
                    qaConverter.__write_timestamp(myFile, elem)
        
                    qaConverter.write_body_rep(elem,myFile)




    '''
    This function converts the Post.xml file into KML
    '''
    
    @staticmethod
    def postConversion(name):
        
        # To get an iterable
        n1 = name.split('/')
        postFile = n1[0]+'/Posts.xml'
        context_post = ET.iterparse(postFile, events=("start", "end"))
        # turning it into an iterator
        context_post = iter(context_post)
        
        # get the root element
        event_posts, root_posts = next(context_post)
        
        postIdBuffer = {}
        #postType = getPostType()
        
        instanceId = 1
        for event, elem in context_post:
            if event == "end" and elem.tag == "row":
                post_id = elem.attrib['Id']
                
                if(elem.attrib['PostTypeId']=='1'):
                    postType = [elem.attrib['PostTypeId']]
                    if(postIdBuffer.get(post_id)==None):
                        postIdBuffer[post_id] = 1
                        #elem,post_id,instanceId,postType,val,name
                        qaConverter.writePostData(elem=elem,post_id=post_id,instanceId=postIdBuffer[post_id],postType=postType,val=1,name=name)
                    else:
                        
                        postIdBuffer[post_id]+=1
                        qaConverter.writePostData(elem=elem,post_id=post_id,instanceId=postIdBuffer[post_id],postType=postType,val=2,name=name)
                    
                    instanceId+=1
                elif(elem.attrib['PostTypeId']=='2'):
                    postType = [elem.attrib['PostTypeId'],elem.attrib['ParentId']]
                    if(postIdBuffer.get(post_id)==None):
                        if(postIdBuffer.get(postType[1])!=None):
                            postIdBuffer[postType[1]] += 1
                            qaConverter.writePostData(elem=elem,post_id=post_id,instanceId=postIdBuffer[postType[1]],postType=postType,val=1,name=name)
                        
                    else:
                        if(postIdBuffer.get(postType[1])!=None):
                            postIdBuffer[postType[1]] += 1
                            qaConverter.writePostData(elem=elem,post_id=post_id,instanceId=postIdBuffer[postType[1]],postType=postType,val=2,name=name)
                    instanceId+=1
                    
                else:
                    postType = [elem.attrib['PostTypeId']]
                    if(postIdBuffer.get(post_id)==None):
                        postIdBuffer[post_id] = 1
                        qaConverter.writePostData(elem=elem,post_id=post_id,instanceId=postIdBuffer[post_id],postType=postType,val=1,name=name)
                    else:
                        
                        postIdBuffer[post_id]+=1
                        qaConverter.writePostData(elem=elem,post_id=post_id,instanceId=postIdBuffer[post_id],postType=postType,val=2,name=name)
                    
                    instanceId+=1
                    
                    
                elem.clear()
                root_posts.clear()
        
        '''
        file_list = glob.glob(name+"/*.knolml")
        for file_path in file_list:
            if(os.path.isfile(file_path)):
                with open(file_path,"a",encoding='utf-8') as myFile:
                    myFile.write("</KnolML>\n") 
        '''
        return postType        

    @staticmethod
    def commentsConversion(name,p):
        if(p==0):
            postType = qaConverter.postHistoryConversion(name)
            #self.postConversion(name)
        else:
            postType = qaConverter.getPostType(name)
            qaConverter.postConversion(name)
            

        # To get an iterable
        n1 = name.split('/')
        commentFile = n1[0]+'/Comments.xml'
        context_comments = ET.iterparse(commentFile, events=("start", "end"))
        # turning it into an iterator
        context_comments = iter(context_comments)
        
        # get the root element
        event_posts, root_posts = next(context_comments)
        
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        for event,elem in context_comments:
            if event == "end" and elem.tag == "row":
                post_id = elem.attrib['PostId']
                post_id_list = postType[post_id]
                if(len(post_id_list)==2):   #checking whether it is a question or answer. If it is an answer, we need to get the parent ID.
                    post_id = post_id_list[1]
                El_id = '"'+elem.attrib['PostId']+'"' #This is to mark the answers
                
                file_path = name+"/Post"+str(post_id)+".knolml" #creating the path for KMNL file
                
                #if(post_id=='3'):
                #print(El_id)
                '''
                if(count==1):
                    break
                count+=1
                '''
                commentDate = elem.attrib['CreationDate']
                
                instance_list = []
                parentId = ''
                if(os.path.exists(file_path)):  #If KMNL file has already been created then read that file
                    
                    dict_answers = {}
                    with open(file_path) as file:
                        for sent in file:
                            if('<Instance' in sent):
                                if('OriginalId' in sent):
                                    sent = sent.split(' ')
                                    #print(sent[4],post_id)
                                    dict_answers[sent[4]] = sent[4]
    
                                    if(dict_answers.get(El_id)!=None):
                                        
                                        parentId = dict_answers[El_id]
                                        '''
                                        if(post_id=='22'):
                                            print(parentId)
                                        '''
                                    sent = " ".join(sent)
                                else:
                                    if(dict_answers.get(El_id)==None):
                                        parentId = '"1"'
                                    
    
                                    
                                #print(parentId)
                            instance_list.append(sent)
    
                    '''
                    if(post_id=='22'):
                        print(dict_answers)
                        print(El_id,parentId)
                    '''
                    
                                    
                    
                    
                    open(file_path, "w").close()
        
    
                comment_index = 0
                index_append_list = 0
                flag = 0
                
                for sent in instance_list:
                    if(flag==1): #This returns that a hit has been found where the comment should be appended 
                        break
                    if("<CreationDate>" in sent):                    
                        post_date = sent.replace('<CreationDate>','')
                        post_date = post_date.replace('</CreationDate>','')
                        post_date = post_date.replace('\t','')
                        post_date = post_date.replace('\n','')
                        post_date = post_date.replace(' ','')
                        post_date = datetime.strptime(post_date, date_format)
                        comDate = datetime.strptime(commentDate, date_format)
                        
                        '''
                        This part finds the index where this comment should be put
                        '''
                        if(comDate<post_date):                        
                            for new_sent in range(comment_index,0,-1):
                                if('<Instance' in instance_list[new_sent]):
                                    index_append_list = new_sent
                                    
                                    flag = 1
                                    break
    
                        
                    comment_index+=1
                
                if(index_append_list==0):
                    index_append_list = len(instance_list)+1
                
                
                '''
                This part adds the comment to its respective place in the list
                '''
                t = '\t'
                Instance = t+t+"<Instance Id= "+"zzz"+" "+"ParentId= "+parentId+" InstanceType="+'"'+"Comments"+'" >\n'
                instance_list.insert(index_append_list,Instance)
                index_append_list+=1
                TimeStamp = t+t+t+"<TimeStamp>\n "
                instance_list.insert(index_append_list,TimeStamp)
                index_append_list+=1
                if(elem.attrib.get("CreationDate") != None):
                    CreationDate = t+t+t+t+"<CreationDate>"+elem.attrib['CreationDate']+"</CreationDate> \n"
                    #myFile.write(CreationDate)
                    instance_list.insert(index_append_list,CreationDate)
                    index_append_list+=1
                TimeStamp = t+t+t+"</TimeStamp>\n "
                #myFile.write(TimeStamp)
                instance_list.insert(index_append_list,TimeStamp)
                index_append_list+=1
                
                contributors = t+t+t+"<Contributors>\n "
                instance_list.insert(index_append_list,contributors)
                index_append_list+=1
                
                if(elem.attrib.get('UserId')!=None):
                    ownerUserId = t+t+t+t+"<OwnerUserId>"+elem.attrib['UserId']+"</OwnerUserId> \n"
                    instance_list.insert(index_append_list,ownerUserId)
                    index_append_list+=1
                else:
                    ownerUserId = t+t+t+t+"<OwnerUserId>"+str(0)+"</OwnerUserId> \n"
                    instance_list.insert(index_append_list,ownerUserId)
                    index_append_list+=1
                    
                contributors = t+t+t+"</Contributors>\n "
                instance_list.insert(index_append_list,contributors)
                index_append_list+=1
                    
                if(elem.attrib.get('Text')!=None):        
                    Body = t+t+t+"<Body>\n"
                    instance_list.insert(index_append_list,Body)
                    index_append_list+=1
                    text_field = t+t+t+t+"<Text Type= "+'"'+"text"+'"'+" Bytes="+'"'+str(len(elem.attrib['Text']))+'">\n'
                    instance_list.insert(index_append_list,text_field)
                    index_append_list+=1
        
                    text_body = textwrap.indent(text=elem.attrib['Text'], prefix=t+t+t+t+t)
                    text_body = html.escape(text_body)
                    Body_text = text_body+"\n"
                    instance_list.insert(index_append_list,Body_text)
                    index_append_list+=1
                    text_field = t+t+t+t+"</Text>\n"
                    instance_list.insert(index_append_list,text_field)
                    index_append_list+=1
                    Body = t+t+t+"</Body>\n"
                    instance_list.insert(index_append_list,Body)
                    index_append_list+=1

                Reputation_tag = t+t+t+"<Credit> \n"
                instance_list.insert(index_append_list,Reputation_tag)
                index_append_list+=1
                if(elem.attrib.get("Score") != None):
                    score = t+t+t+t+"<Score>"+elem.attrib['Score']+"</Score>\n"
                    instance_list.insert(index_append_list,score)
                    index_append_list+=1
                    
            
                Reputation_tag = t+t+t+"</Credit> \n"
                instance_list.insert(index_append_list,Reputation_tag)
                index_append_list+=1                       

                
                Instance = t+t+"</Instance>\n"
                instance_list.insert(index_append_list,Instance)
                
                '''
                Writing everything to the file
                '''
                open(file_path, "w").close()
                
                '''
                instanceId = 1
                dict_answers = {'1':'1'}
                
                for myLine in instance_list:
                    if('<Instance Id' in myLine):
                        myLine = myLine.split(' ')
                        myLine[2] = '"'+str(instanceId)+'"'
                        myLine = " ".join(myLine)
                        
                        if(myLine[3] == 'OriginalId='):   
                            if(dict_answers.get(myLine[4])==None):
                                dict_answers[myLine[4]] = str(instanceId)
                        
                        instanceId+=1
                '''
                
                
                instanceId = 1
                '''            
                if(post_id == '22'):
                    print(dict_answers)            
                '''
                
                dict_answers = {'"1"':'"1"'}
                #print(dict_answers)
                with open(file_path,'a') as myFile:
                    
                    for myLine in instance_list:
                        '''
                        if(post_id=='22'):
                            if('<Instance Id' in myLine):
                                print(myLine)
                        '''
                        if('<Instance Id' in myLine):
    
                            myLine = myLine.split(' ')
                            myLine[2] = '"'+str(instanceId)+'"'
                            #myLine[2] = '"'+str(instanceId)+'"'
                            
                            
                            if(myLine[3] == 'OriginalId='):   
                                if(dict_answers.get(myLine[4])==None):
                                    dict_answers[myLine[4]] = '"'+str(instanceId)+'"'
    
                            
                            
                            if(myLine[3]=='ParentId='):
                                
                                #print(file_path)
                                #print(myLine[0],myLine[1],myLine[2],myLine[3],myLine[4],myLine[5],myLine[6])
                                
                                '''
                                if(post_id == '22'):
                                    print(myLine[5])
                                '''
                                #print(file_path)
                                #print(myLine)
                                
                                if((dict_answers.get(myLine[4])!=None)):
                                    '''
                                    if(post_id == '21'):
                                        print(myLine[4])
                                    '''
                                    myLine[4] = dict_answers[myLine[4]]
                                    
                            
                            
                            myLine = " ".join(myLine)
                            instanceId+=1
                            
                            '''
                            if(post_id == '22'):
                                print(dict_answers)
                            '''
                        myFile.write(myLine)    
    
                elem.clear()
                root_posts.clear()

        file_list = glob.glob(name+"/*.knolml")
        for file_path in file_list:
            if(os.path.isfile(file_path)):
                with open(file_path,"a",encoding='utf-8') as myFile:
                    myFile.write("\t</KnowledgeData>\n")
                    myFile.write("</KnolML>\n")                 
                
    
    @staticmethod            
    def convert(*args, **kwargs):
        name = kwargs['name']
        name = name.lower()
        if(kwargs.get('download')!=None):             
            down = kwargs['download']
            if(down):

                
                with open('stackExchangeList.txt','r') as myFile:
                    for line in myFile:
                        if(name in line):
                            siteName = line[:-1]
                print("Downloading the "+name+" Stack Exchange data dump")
                download('stackexchange', verbose=True, glob_pattern=siteName)
                qaConverter.make_path(name)
                call(["7z","x",'stackexchange/'+siteName,'-o'+name])
                
                '''
                calling the KML converter for Stack_exchange
                '''
                
                if(kwargs.get('posthistory')!=None):
                    ph = kwargs['posthistory']
                    if(ph):
                        print("Converting PostHistory of "+name+" Stack Exchange into knolml")
                        qaConverter.make_path(name+"/PostHistory")
                        namePh = name+"/PostHistory"
                        qaConverter.commentsConversion(namePh,0)
                        print("PostHistory conversion completed for "+name+" Stack Exchange")
                if(kwargs.get('post')!=None):
                    p = kwargs['post']
                    if(p):
                        print("Converting Posts of "+name+" Stack Exchange into knolml")
                        qaConverter.make_path(name+"/Posts")
                        nameP = name+"/Posts"
                        qaConverter.commentsConversion(nameP,1)
                        print("Posts conversion completed for "+name+" Stack Exchange")
                
            else:
                '''
                calling the KML converter for Stack_exchange
                '''
                with open('stackExchangeList.txt','r') as myFile:
                    for line in myFile:
                        if(name in line):
                            siteName = line[:-1]

                call(["7z","x",'stackexchange/'+siteName,'-o'+name])
                
                if(kwargs.get('posthistory')!=None):
                    ph = kwargs['posthistory']
                    if(ph):
                        print("Converting PostHistory of "+name+" Stack Exchange into knolml")
                        qaConverter.make_path(name+"/PostHistory")
                        namePh = name+"/PostHistory"
                        qaConverter.commentsConversion(namePh,0)
                        print("PostHistory conversion completed for "+name+" Stack Exchange")

                if(kwargs.get('post')!=None):
                    p = kwargs['post']
                    if(p):
                        print("Converting Posts of "+name+" Stack Exchange into knolml")
                        qaConverter.make_path(name+"/Posts")
                        nameP = name+"/Posts"
                        qaConverter.commentsConversion(nameP,1)
                        print("Posts conversion completed for "+name+" Stack Exchange")
                
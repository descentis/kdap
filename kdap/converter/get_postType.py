#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 11:18:54 2018

@author: descentis
"""

import xml.etree.cElementTree as ET

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
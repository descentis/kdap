#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 20:50:31 2020

@author: descentis
"""

import xml.etree.cElementTree as ET
import time

t1 = time.time()
context_post = ET.iterparse('stack_post.xml', events=("start", "end"))

context_post = iter(context_post)

event_posts, root_posts = next(context_post)
classA = 0
classB = 0
classC = 0
classD = 0
#developers = {}
for event, elem in context_post:
    if event == "end" and elem.tag == "row":
        if elem.attrib['PostTypeId'] == '1':
            if elem.attrib.get('AcceptedAnswerId') != None and elem.attrib.get('ClosedDate') == None and int(elem.attrib['Score'])>7:
                classA += 1
            elif elem.attrib.get('AcceptedAnswerId') != None and elem.attrib.get('ClosedDate') == None and int(elem.attrib['Score'])<7 and int(elem.attrib['Score'])>1:
                classB += 1
            elif elem.attrib.get('ClosedDate') == None and int(elem.attrib['Score'])<0:
                classC += 1
            else:
                classD += 1
        elem.clear()
        root_posts.clear()
t2 = time.time()
print(t2-t1)
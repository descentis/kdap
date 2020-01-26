#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 22:52:01 2019

@author: descentis
"""
from random import sample
import xml.etree.cElementTree as ET
import time

t1 = time.time()
context_post = ET.iterparse('stack_post.xml', events=("start", "end"))

context_post = iter(context_post)

event_posts, root_posts = next(context_post)
question_id = []
#developers = {}
for event, elem in context_post:
    if event == "end" and elem.tag == "row":
        if elem.attrib['PostTypeId'] == "1":
            question_id.append(elem.attrib['Id'])
        
        elem.clear()
        root_posts.clear()

print('first part done')            
sampled_question = sample(question_id, 100000)
sampled_dict = {}

for i in sampled_question:
    sampled_dict[i] = 1
number_of_questions = len(question_id)
'''
RQ1: histogram of questioners
RQ2: histogram of answerers
'''
editor_question = {}
editor_answer = {}
editor_graph = {}
context_post = ET.iterparse('stack_post.xml', events=("start", "end"))

context_post = iter(context_post)

event_posts, root_posts = next(context_post)
for event, elem in context_post:
    if event == "end" and elem.tag == "row":
        if elem.attrib['PostTypeId'] == "1" and sampled_dict.get(elem.attrib['Id'])!=None:
            if elem.attrib.get('OwnerUserId')!=None:
                if editor_question.get(elem.attrib['OwnerUserId']) == None:
                    editor_question[elem.attrib['OwnerUserId']] = 1
                    
                else:
                    editor_question[elem.attrib['OwnerUserId']] += 1
                    
        elif elem.attrib['PostTypeId'] == "2" and sampled_dict.get(elem.attrib['ParentId']):
            if elem.attrib.get('OwnerUserId')!=None:
                if editor_answer.get(elem.attrib['OwnerUserId']) == None:
                    editor_answer[elem.attrib['OwnerUserId']] = 1
                else:
                    editor_answer[elem.attrib['OwnerUserId']] += 1           
        
        elem.clear()
        root_posts.clear()
total_posts = 0        
q_hist = {}
for key,val in editor_question.items():
    total_posts += editor_question[key]
    if q_hist.get(val)==None:
        q_hist[val] = 1
    else:
        q_hist[val] += 1        

a_hist = {}
for key,val in editor_answer.items():
    total_posts += editor_answer[key]
    if a_hist.get(val)==None:
        a_hist[val] = 1
    else:
        a_hist[val] += 1     

editor_list = list(editor_question.keys())

editor_list += list(editor_answer.keys())

editor_list = list(set(editor_list))
comm_hist = {}
for k in range(0, 110, 10):
    comm_hist[k] = 0

for e in editor_list:
    if editor_answer.get(e) == None:
        comm_hist[0] += 1
    elif editor_question.get(e) == None:
        value = (editor_answer[e]/editor_answer[e])*100
    else:
        value = (editor_answer[e]/(editor_answer[e]+editor_question[e]))*100
        if value <= 10:
            comm_hist[10] += 1
        if value > 100:
            comm_hist[100] += 1
        else:
            r = int(value/10)*10
            comm_hist[r] += 1
        
t2 = time.time()
print(t2-t1)
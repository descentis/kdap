#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:08:48 2019

@author: descentis
"""
import kdap

knol = kdap.knol()
questioners = knol.get_author_edits(dir_path='beer/Posts', type='edits', ordered_by='questions')
q_hist = {}
total_posts = 0
for key,val in questioners.items():
    total_posts += questioners[key]
    if q_hist.get(val)==None:
        q_hist[val] = 1
    else:
        q_hist[val] += 1
answerers = knol.get_author_edits(dir_path='beer/Posts', type='edits', ordered_by='answers')

a_hist = {}
for key,val in answerers.items():
    total_posts += answerers[key]
    if a_hist.get(val)==None:
        a_hist[val] = 1
    else:
        a_hist[val] += 1
        
editor_list = list(questioners.keys())
editor_list += list(answerers.keys())

comm_hist = {}
for k in range(0, 110, 10):
    comm_hist[k] = 0

for e in editor_list:
    if answerers.get(e) == None:
        comm_hist[0] += 1
    else:
        value = (answerers[e]/total_posts)*100
        if value<=10:
           comm_hist[10] += 1 
        else:
            r = int(value/10)*10
            comm_hist[r] += 1                
        

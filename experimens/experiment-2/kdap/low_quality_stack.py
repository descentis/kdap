#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:00:01 2020

@author: descentis
"""
import kdap
import glob
knol = kdap.knol()

def find_lower(text, title):
    lower = 0
    upper = 0
    space = 0
    total = 0
    for i in text:
        if i.islower():
            lower += 1
        else:
            upper += 1
        if i == ' ':
            space += 1
        total += 1
    result = {}
    result['lower'] = lower/total
    result['upper'] = upper/total
    result['space'] = space/total
    if text[0].islower():
        result['capital'] = 0
    else:
        result['capital'] = 1
    return result
file_list = glob.glob('anime/Posts/*.knolml')
countA = 0
countB = 0
countC = 0
countD = 0
for f in file_list:
    fr = knol.frame(file_name=f)
    for frm in fr:
        if frm.is_question():
            if not frm.is_closed() and frm.get_score['Score']>7:
                countA += 1
                words = frm.get_text_stats(count_words=True)
                email = frm.get_text_stats(email_id=True)
                url = frm.get_text_stats(url=True)
                question_length = frm.get_bytes()
                tags = frm.get_tags()
                title_length = frm.title
                result = find_lower(frm.get_text()['text'], frm.title)
            if not frm.is_closed() and frm.get_score['Score']<7 and frm.get_score['Score']>1:
                countB += 1
                words = frm.get_text_stats(count_words=True)
                email = frm.get_text_stats(email_id=True)
                url = frm.get_text_stats(url=True)
                question_length = frm.get_bytes()
                tags = frm.get_tags()
                title_length = frm.title
                result = find_lower(frm.get_text()['text'], frm.title)
            if not frm.is_closed() and frm.get_score['Score']<0:
                countC += 1
                words = frm.get_text_stats(count_words=True)
                email = frm.get_text_stats(email_id=True)
                url = frm.get_text_stats(url=True)
                question_length = frm.get_bytes()
                tags = frm.get_tags()
                title_length = frm.title
                result = find_lower(frm.get_text()['text'], frm.title)
            else:
                countD += 1
                words = frm.get_text_stats(count_words=True)
                email = frm.get_text_stats(email_id=True)
                url = frm.get_text_stats(url=True)
                question_length = frm.get_bytes()
                tags = frm.get_tags()
                title_length = frm.title
                result = find_lower(frm.get_text()['text'], frm.title)
                
            
            
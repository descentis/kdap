#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 21:16:26 2019

@author: descentis
"""

import kdap
import glob
from random import sample
from scipy.stats import pearsonr
import time
import psutil
import os

def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss
knol = kdap.knol()

#task-1
category_list = ['FA', 'GA', 'B', 'C', 'Start', 'Stub']
articles = {}
for category in category_list:
    articles[category] = sample(knol.get_wiki_article_by_class(wiki_class=category), 5)


#task-2
file_list = glob.glob('anime/Posts/*.knolml')

final_list = sample(file_list, 10000)
sampled_questions = []
sampled_answers = []
sampled_comments = []
for f in final_list:
    fr = knol.frame(file_name=f)
    for frm in fr:
        if frm.is_question():
            sampled_questions.append(frm.get_text())
        if frm.is_answer():
            sampled_answers.append(frm.get_text())
        if frm.is_comment():
            sampled_comments.append(frm.get_text())

#task-3
p1 = get_process_memory()
t1 = time.time()
revision = knol.get_revision_type(file_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list/United_States.knolml')
t2 = time.time()
p2 = get_process_memory()
print(t2-t1)
print("memory taken = ",p2-p1)


# task - 4
p1 = get_process_memory()
t1 = time.time()
instanceId = knol.get_instance_id(dir_path='anime/Posts', type='accepted answer')
accepted_questions = []
for f in list(instanceId.keys()):
    fr = knol.frame(file_name='anime/Posts/'+f)
    accepted_questions.append(fr[0].get_text())
t2 = time.time()
p2 = get_process_memory()
print(t2-t1)
print("memory taken = ",p2-p1)

# task - 5
p1 = get_process_memory()
t1 = time.time()
stack_list = ['3dprinting', 'ai', 'arduino', 'boardgames', 'chemistry', 'chess']
gini_list = []
atoq_ratio = []
for portal in stack_list:
    #knol.download_dataset(sitename='stackexchange', portal=portal)
    gini_list.append(knol.get_global_gini_coefficient(dir_path=portal+'/Posts'))
    questions = knol.get_num_instances(dir_path=portal+'/Posts', instance_type='question')
    answers = knol.get_num_instances(dir_path=portal+'/Posts', instance_type='answer')   
    atoq_ratio.append(questions['questions']/answers['answers'])

print(pearsonr(gini_list, atoq_ratio))
t2 = time.time()
p2 = get_process_memory()
print(t2-t1)
print("memory taken = ",p2-p1)

# task - 6
p1 = get_process_memory()
t1 = time.time()
revisions = knol.get_num_instances(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list', granularity='monthly', start='2015-07-01')
views = knol.get_pageviews(site_name='Wikipedia', article_name='United States', granularity='monthly', start='2015-07-01', end='2019-07-01')
t2 = time.time()
p2 = get_process_memory()
print(t2-t1)
print("memory taken = ",p2-p1)


# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 19:38:33 2019

@author: descentis
"""
import time
import kdap
from random import sample
from scipy.stats import variation 

'''
code to get the articles related to a WikiProject

******stratified sampling*******
(sample size of the strata = size of the entire sample / population size*layer size)
'''
knol = kdap.knol()

wikiproject_list = ['History', 'Scociology', 'Geography', 'Culture', 'Technology', 'Science', 'Mathematics', 'Philosophy', 'Religion']

article_dict = {}
population_size = 0
project_size = []
-
    population_size += len(article_dict[project])
    project_size.append(len(article_dict[project]))
    
sample_size = 6000

sample_project_list = []

for i in project_size:
    sample_project_list.append((sample_size/population_size)*i)

article_list = []

j=0
for key,val in article_dict.items():
    article_list += sample(article_dict[key], sample_project_list[j])
    j+=1
    
knol.download_dataset('wikipedia', article_list=article_list, wikipedia_dump='/media/descentis/0FC10BE60FC10BE6/WikipediaData/dumps.wikimedia.org/enwiki/latest')

wiki_bots = knol.get_wiki_group_editors('bots')

editor_edits = knol.get_author_edits('wikipedia', dir_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list')

editor_edits_list = []
for key,val in editor_edits.items():
    if key not in wiki_bots:
        li = []
        for art, edit in val.items():
            li.append(edit)
        editor_edits_list.append(variation(li, axis = 1))

editor_list = []

for key,val in editor_edits.items():
    if key not in wiki_bots:
        editor_list.append(key)

edits_on_wikipedia = knol.get_author_edits('wikipedia', editor_list=editor_list, type='edits', all_wiki=True)

reverts = knol.get_wiki_reverts(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list')

talk_edits = knol.get_wiki_talk_instances(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list')

editors = knol.get_editors(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list')

article_age = knol.get_age_of_knowledge(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/article_list', date='2016-04-01')


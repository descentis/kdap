#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:51:54 2019

@author: descentis
"""

import kdap

def blm():
    knol = kdap.knol()
    B = knol.download_dataset('wikipedia',wikipedia_dump='/media/descentis/0FC10BE60FC10BE6/WikipediaData/dumps.wikimedia.org/enwiki/latest', category_list=['Black Lives Matter'])
    C = knol.download_dataset('wikipedia',wikipedia_dump='/media/descentis/0FC10BE60FC10BE6/WikipediaData/dumps.wikimedia.org/enwiki/latest', template_list=['Black Lives Matter'])
    
    date = knol.get_instance_date(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/Black Lives Matter')
    article_list = []
    for key,val in date.items():
        article_list.append(key)
    revisions = knol.get_num_instances(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/Black Lives Matter', granularity='monthly', start='2009-01-01')
    
    editors = knol.get_editors(dir_path='/home/descentis/knolml_dataset/wikipedia_articles/Black Lives Matter', granularity='daily', start='2014-01-01', end='2016-01-01')
    
    similarity = knol.get_author_similarity(editors, similarity='jaccard')
    
    page_views = {}
    
    for article in article_list:
        views = knol.get_pageviews(site_name='Wikipedia', article_name=article, granularity='monthly', start='2015-02-01', end='2015-10-01')
        page_views[article] = views
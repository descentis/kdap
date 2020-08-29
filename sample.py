#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 21:00:11 2019

@author: descentis
"""

import kdap 

article_list = ['Derivative', 'Vector']
knol = kdap.knol()

knol.download_dataset(sitename='wikipedia',article_list=article_list, wikipedia_dump='/media/descentis/0FC10BE60FC10BE6/WikipediaData/dumps.wikimedia.org/enwiki/latest', destdir='dataset')
#wikiConverter.compressAll('wiki',output_dir='output')
#wikiConverter.getArticle(file_name='Indian Institute of Technology Ropar', output_dir='wiki')
#p = knolAnalysis.getLocalGiniCoefficient(dir_path='/home/descentis/research/KML/output/')
#qaConverter.convert('beer', download=True, posthistory=True, post=True)
#p = knolAnalysis.revisionTypes(file_path='/home/descentis/research/KML/output/Indian Institute of Technology RoparCompressed.knolml')

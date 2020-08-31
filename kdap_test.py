#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:28:34 2020

@author: Main
"""

import kdap

knol = kdap.knol()

#knol.get_wiki_article('Indian Institute of Technology Ropar')
fr = knol.frame(file_name='output/Indian_Institute_of_Technology_Ropar.knolml', get_bulk=False)
#revisions = knol.get_num_instances(dir_path='/Users/Main/Documents/research/kdap/output', granularity='monthly', start='2015-07-01')

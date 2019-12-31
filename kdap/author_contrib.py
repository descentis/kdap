#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 12:55:50 2019

@author: descentis
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import difflib
import collections
from datetime import datetime

author_contribution = collections.defaultdict(lambda: [])

#Main Function
#file_name = input("Enter compressed KNML file path: ")
file_name = "2006_Westchester_County_torna.knolml"
d1 = datetime.strptime(input("Enter start date as YYYY-MM-DD format: "), '%Y-%m-%d')
d2 = datetime.strptime(input("Enter start date as YYYY-MM-DD format: "), '%Y-%m-%d')


tree = ET.parse(file_name)
root = tree.getroot()
last_rev = ""
count = 0
length = len(root[0].findall('Instance'))

revisionsList = []

last_contribution = 0

for each in root.iter('Instance'):
	instanceId = int(each.attrib['Id'])
	dict_key = 0
	dict_val = 0
	for child in each:
		if 'TimeStamp' in child.tag:
			contr_date = datetime.strptime(child[0].text.split("T")[0], '%Y-%m-%d')
			if d1 > contr_date or d2 < contr_date:
				break 
		if 'Contributors' in child.tag:
			dict_key = revision = child[0].text
		if 'Body' in child.tag:
			dict_val = len(child[0].text.split())
			#print(dict_key)
			#print(dict_val)	
			author_contribution[dict_key].append(dict_val-last_contribution)
			last_contribution = dict_val
#List of all revisions			
#print(revisionsList)

#Sentence Number, modified sentence
for i in range(1, len(revisionsList)):
	analyze(revisionsList[i-1].split(), revisionsList[i].split(), i+1)


print("\n\n======Authors' Contribution==========\n\n")
'''
for x in sorted(author_contribution.items() ,  key=lambda x: x[1]):
	print(x[0], "\n--->", x[1])
'''
for x in author_contribution.items():
	print(x[0], "\n--->", x[1])
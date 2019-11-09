#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:57:27 2019

@author: descentis

"""

from kdap.analysis import instances
from kdap.converter.qaConverter import qaConverter
from kdap.analysis import knol
#from kdap.converter.wikiConverter import wikiConverter
import xml.etree.ElementTree as ET

def frames(file_name):
    tree = ET.parse(file_name)
    
    root = tree.getroot()
    
    object_list = []
    title = ''
    for elem in root:
        if 'KnowledgeData' in elem.tag:
            for ch1 in elem:
                if 'Title' in ch1.tag:
                    title = ch1.text
                if 'Instance' in ch1.tag:
                    instance = ch1
                    object_list.append(instances(instance, title))
    
    return object_list
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 12:15:28 2020

@author: Main
"""
list1 = []
with open('stackExchangeList.txt', 'r') as myfile:
    for line in myfile:
        list1.append(line[:-1])
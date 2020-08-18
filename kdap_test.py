#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:28:34 2020

@author: Main
"""

import kdap

knol = kdap.knol()

revisions = knol.get_num_instances(dir_path='/Users/Main/Documents/research/kdap/output', granularity='monthly', start='2015-07-01')

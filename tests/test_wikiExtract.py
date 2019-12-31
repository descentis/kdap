#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 14:38:53 2019

@author: descentis
"""

import unittest
from kdap.wikiextract.wikiExtract import wikiExtract
class TestWikiExtract(unittest.TestCase):
    
    def setUp(self): 
        pass
    
    def test_category(self):
        '''
        testing the category method
        '''
        d = {'Left-wing advocacy groups in France': [{'pageid': 7932537,
   'ns': 0,
   'title': 'Comité de vigilance des intellectuels antifascistes'},
  {'pageid': 8417221, 'ns': 0, 'title': 'ADFE-Français du Monde'},
  {'pageid': 33092539,
   'ns': 0,
   'title': 'Section des sourds et malentendants socialistes'},
  {'pageid': 2799424, 'ns': 0, 'title': 'SOS Racisme'}],
 'extra#@#category': []}
        we = wikiExtract()
        C = we.get_articles_by_category('Left-wing advocacy groups in France')
        self.assertEqual(C, d)
    
if __name__ == '__main__': 
    unittest.main() 
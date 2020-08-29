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
    
    
    def test_template(self):
        # testing the template method
        t = {'python': [{'pageid': 45459, 'ns': 0, 'title': 'Control flow'},
  {'pageid': 59231, 'ns': 0, 'title': 'Exception handling'},
  {'pageid': 1010628, 'ns': 0, 'title': 'Method overriding'},
  {'pageid': 23655350,
   'ns': 4,
   'title': 'Wikipedia:Bots/Requests for approval/jverlindaBot'},
  {'pageid': 58886025, 'ns': 2, 'title': 'User:Lpwarner/be bold'}]}
        we = wikiExtract()
        C = we.get_articles_by_template('python')
        self.assertEqual(C,t)
        
    def test_author_wiki_edits(self):
        # testing the wiki author edits
        e = [{'name': 'Ak47', 'missing': ''}]
        we = wikiExtract()
        C = we.get_author_wiki_edits(['ak47'])
        self.assertEqual(C, e)
        
if __name__ == '__main__': 
    unittest.main() 
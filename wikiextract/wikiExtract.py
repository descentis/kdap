#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:07:50 2019

@author: descentis
"""
import pycountry
from sampleExtractdb import display_data

class wikiExtract(object):
    
    def getCountryList(self):
        list_countries = []
        for c in pycountry.countries:
            list_countries.append(str(c.name))
        
        wiki_countries = []
        '''
        countries_id = display_data("select article_nm,project from wiki_project where project='countries';")
        for i in countries_id:
            wikiC = display_data("select article_nm from article_desc where article_id ="+ "'"+i[0]+"';")
            wiki_countries.append(wikiC[0][0])
            print(wikiC[0][0])
        '''
        for l in list_countries:
            print(l)
            try:
                wikiC = display_data("select article_id from article_desc where article_nm ="+ "'"+l+"';")
            except:
                pass
            if(len(wikiC)>0):
                wiki_countries.append(wikiC[0][0])
                print(wikiC[0][0])
        
        '''
        country_wiki_name = []
        for i in wiki_countries:
            if i.lower() in list_countries:
                country_wiki_name.append(i)
        '''
        return wiki_countries
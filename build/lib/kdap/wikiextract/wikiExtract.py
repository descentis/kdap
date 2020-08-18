#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:07:50 2019

@author: descentis
"""

#from sampleExtractdb import display_data
import requests

class wikiExtract(object):
    
    def get_articles_by_category(self, category_name):
        '''
        this definition can be used to get the names of article
        related to a category
        '''
        url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&format=json&cmlimit=500&cmtitle=Category:'
        category_dict = {}
        url = url1+category_name
        article_list = []
        extra_category = []
        while(True):
            r = requests.get(url)
            try:
                data = r.json()
            except:
                break
            pages = data['query']['categorymembers']
            for i in pages:
                
                if 'Category:' in i['title']:
                    extra_category.append(i)
                elif 'Template:' not in i['title']:
                    article_list.append(i)
            
            if data.get('continue')!=None:
                url = url+'&cmcontinue='+data['continue']['cmcontinue']
            else:
                break
        category_dict[category_name] = article_list
        category_dict['extra#@#category'] = extra_category
        
        return category_dict
    
    def get_articles_by_template(self, template_name):
        '''
        this definition can be used to get the names of article
        based on category
        '''
        url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eilimit=5&format=json&eititle=Template:'
        template_dict = {}
        url = url1+template_name
        article_list = []
        while(True):
            r = requests.get(url)
            data = r.json()
            pages = data['query']['embeddedin']
            for i in pages:
                article_list.append(i)
            
            if data.get('continue')!=None:
                url = url+'&eicontinue='+data['continue']['eicontinue']
            else:
                break
        template_dict[template_name] = article_list
        
        return template_dict

    def get_author_wiki_edits(self, editor):
        '''
        This defination can be used to get the edits of a user in wikipedia
        '''
        url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=users&usprop=editcount&format=json&ususers='
        author_list = []
        editor_list = '|'.join(editor)
        url = url1+editor_list
        while(True):
            r = requests.get(url)
            try:
                data = r.json()
            except:
                break
            pages = data['query']['users']
            for i in pages:
                author_list.append(i)
            
            if data.get('continue')!=None:
                url = url+'&uccontinue='+data['continue']['uccontinue']
            else:
                break
        
        return author_list
    
    def get_wiki_revision(self, file_name):
        '''
        This defination can be used to get the number of edits in an article of wikipedia
        '''
        url1 = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvdir=newer&format=json&titles=Talk:'
        revisions = 0
        url = url1+file_name
        while(True):
            r = requests.get(url)
            try:
                data = r.json()
            except:
                break
            key = list(data['query']['pages'].keys())
            #print(key)
            pages = data['query']['pages'][key[0]]['revisions']
            for i in pages:
                revisions+=1
            
            if data.get('continue')!=None:
                url = url+'&rvcontinue='+data['continue']['rvcontinue']
            else:
                break
        
        return revisions

'''
w = wikiExtract()
B = w.get_articles_by_template(['Black Lives Matter'])
for key,val in B.items():
    print(key, val)
'''

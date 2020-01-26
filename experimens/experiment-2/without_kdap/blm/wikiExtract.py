#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:07:50 2019

@author: descentis
"""

# from sampleExtractdb import display_data
import requests


class wikiExtract(object):

    def get_articles_by_category(self, category_name):
        '''
        this definition can be used to get the names of article
        related to a category
        '''
        url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmlimit=500&format=json&cmtitle=Category:'
        category_dict = {}
        url = url1 + category_name
        article_list = []
        extra_category = []
        while (True):
            r = requests.get(url)
            data = r.json()
            pages = data['query']['categorymembers']
            for i in pages:

                if 'Category:' in i['title']:
                    extra_category.append(i)
                elif 'Template:' not in i['title']:
                    article_list.append(i)

            if data.get('continue') != None:
                url = url + '&cmcontinue=' + data['continue']['cmcontinue']
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
        url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eilimit=500&format=json&eititle=Template:'
        template_dict = {}
        url = url1 + template_name
        article_list = []
        while (True):
            r = requests.get(url)
            data = r.json()
            pages = data['query']['embeddedin']
            for i in pages:
                article_list.append(i)

            if data.get('continue') != None:
                url = url + '&eicontinue=' + data['continue']['eicontinue']
            else:
                break
        template_dict[template_name] = article_list

        return template_dict


'''
w = wikiExtract()
B = w.get_articles_by_category('All Wikipedia bots')
print(B)
'''

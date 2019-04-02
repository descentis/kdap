#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 06:54:41 2018

@author: descentis
"""

import requests
import io



def get_wiki_byname(featuredArticleList):
	# articleName = raw_input()
	# articleName = articleName.replace(' ', '_')

	for each in featuredArticleList:
		articleName = each

		file_handler = io.open(articleName+'.xml', mode='w+', encoding='utf-8')

		url = 'https://en.m.wikipedia.org/w/index.php?title=Special:Export&pages=' + articleName + '&history=1&action=submit'
		headers = {
			'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
		}
		print('Downloading ' + articleName + '...') 
		r = requests.get(url, headers=headers)
		if r.status_code == 200:
			xml = r.text
			file_handler.write(xml)
			print(articleName,'Completed!')
		else:
			print('Something went wrong! ' + articleName + '\n' + '\n')

		file_handler.close()

from blm.wikiExtract import wikiExtract
import random
import json


def get_articles():
    grades = ['FA', 'GA', 'B', 'C', 'Start', 'Stub']
    w = wikiExtract()
    articles = {}
    for grade in grades:
        class_results = w.get_articles_by_category(grade + '-Class articles')
        extras = random.choices(class_results['extra#@#category'], k=5)
        for extra in extras:
            extra_articles = w.get_articles_by_category(extra['title'][9:])[extra['title'][9:]]
            if len(extra_articles) >= 5:
                articles[grade] = [data['title'] for data in random.choices(extra_articles, k=5)]
                for i in range(len(articles[grade])):
                    if articles[grade][i][:5].lower() == 'talk:':
                        articles[grade][i] = articles[grade][i][5:]
                if len(set(articles[grade])) == len(articles[grade]):
                    break

    with open("wiki_articles.json", "w") as fh:
        json.dump(articles, fh)


'''
import time
s = time.time()
get_articles()
e = time.time()
print(e-s)
'''

from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from blm.wikiExtract import wikiExtract
# import time


def get_monthwise_articles_edited(template_name):
    w = wikiExtract()
    template_articles = w.get_articles_by_template(template_name)
    articles_list = template_articles[template_name]
    monthwise_articles = {template_name: {}}
    for article in articles_list:
        revisions = get_revisions_of_article(article['title'])[article['title']]
        for revision in revisions:
            timestamp = revision['timestamp'][:7]
            year = int(timestamp[:4])
            if 2009 <= year < 2019:
                if timestamp not in monthwise_articles[template_name]:
                    monthwise_articles[template_name][timestamp] = []
                if article not in monthwise_articles[template_name][timestamp]:
                    monthwise_articles[template_name][timestamp].append(article)
    return monthwise_articles


'''
s = time.time()
d = get_monthwise_articles_edited('Black Lives Matter')
e = time.time()
print(e-s, d, sep='\n')
'''

from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from blm.wikiExtract import wikiExtract
# import time


def get_monthly_authors_by_category(template_name):
    w = wikiExtract()
    category_dict = w.get_articles_by_template(template_name)
    article_list = category_dict[template_name]
    monthly_revisions_dict = {template_name: {}}
    for article in article_list:
        revisions = get_revisions_of_article(article['title'])[article['title']]
        for revision in revisions:
            timestamp = revision['timestamp'][:7]
            if timestamp not in monthly_revisions_dict[template_name]:
                monthly_revisions_dict[template_name][timestamp] = []
            if 'user' in revision:
                author = revision['user']
                if author not in monthly_revisions_dict[template_name][timestamp]:
                    monthly_revisions_dict[template_name][timestamp].append(author)

    return monthly_revisions_dict

'''
s = time.time()
d = get_monthly_revision_count_by_category('Black Lives Matter')
e = time.time()
print(e-s, d, sep='\n')
'''
from blm.kdap_wikiArticlesEditedMonthwise import get_monthwise_articles_edited
# import time


def get_monthwise_articles_edited_count(template_name):
    monthwise_articles = get_monthwise_articles_edited(template_name)
    monthwise_articles_count = {template_name: {}}
    for timestamp in monthwise_articles[template_name]:
        monthwise_articles_count[template_name][timestamp] = len(monthwise_articles[template_name][timestamp])
    return monthwise_articles_count


'''
s = time.time()
d = get_monthwise_articles_edited('Black Lives Matter')
e = time.time()
print(e-s, d, sep='\n')
'''

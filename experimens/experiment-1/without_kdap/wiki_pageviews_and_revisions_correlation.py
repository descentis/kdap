from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from blm.wiki_pageViews import get_pageviews
import scipy.stats as ss
import datetime


def find_correlation(article_name):
    revisions = get_revisions_of_article(article_name, rvprop='ids|timestamp')[article_name]
    revisions.reverse()

    end_timestamp = revisions[-1]['timestamp'][:10]
    end_date = (datetime.datetime(int(end_timestamp[:4]), int(end_timestamp[5:7]), int(end_timestamp[8:10]))
                + datetime.timedelta(31)).strftime('%Y-%m-%d')

    start_timestamp = revisions[0]['timestamp'][:10]
    start_date = max(datetime.datetime(int(start_timestamp[:4]), int(start_timestamp[5:7]), int(start_timestamp[8:10])),
                     datetime.datetime(2015, 7, 1)).strftime('%Y-%m-%d')

    pageviews_raw = get_pageviews('wikipedia', article_name=article_name, start=start_date, end=end_date,
                                  granularity='monthly')

    sorted_keys = sorted(pageviews_raw.keys())[:-1]
    pageviews = {k.strftime('%d-%m-%Y'): pageviews_raw[k][article_name.replace(' ', '_')] for k in sorted_keys
                 if pageviews_raw[k][article_name.replace(' ', '_')] is not None}
    # print(pageviews)

    rev_count = {k.strftime('%d-%m-%Y'): 0 for k in sorted_keys}
    for revision in revisions:
        rev_timestamp = revision['timestamp'][:10]
        rev_date = datetime.datetime(int(rev_timestamp[:4]), int(rev_timestamp[5:7]), int(rev_timestamp[8:10]))
        if rev_date >= datetime.datetime(2015, 7, 1):
            rev_count['01-' + rev_timestamp[5:7] + '-' + rev_timestamp[:4]] += 1

    # print(rev_count)

    return ss.pearsonr(list(pageviews.values()), list(rev_count.values()))


def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    import os
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

print(memory_usage_psutil())
find_correlation('United States')
print(memory_usage_psutil())

'''
import time
s = time.time()
find_correlation('United States')
e = time.time()
print(e-s)
'''

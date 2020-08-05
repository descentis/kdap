from crowd_diversity.utility_functions import get_editors_of_article, get_revisions_of_article, get_editor_contributions
import datetime
import math


def article_size(article):
    editors = set(get_editors_of_article(article))
    return math.log10(len(editors))


def article_age(article):
    revisions = get_revisions_of_article(article)
    timestamp = revisions[len(revisions) - 1]['timestamp']
    creation_date = datetime.datetime(int(timestamp[:4]), int(timestamp[5:7]), int(timestamp[8:10]))
    now_date = datetime.datetime.now()
    return math.log10((now_date - creation_date).total_seconds())


def average_experience(article):
    editors = list(set(get_editors_of_article(article)))
    contributions = get_editor_contributions()
    average = 0
    for editor in editors:
        average += contributions[editor]

    average /= len(editors)
    return math.log10(average)

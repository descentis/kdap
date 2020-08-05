import math
import statistics
from crowd_diversity.utility_functions import get_editors_of_article, get_all_bots, get_editor_contributions


def contribution_diversity(article):
    editors = get_editors_of_article(article)
    bots = get_all_bots()
    for editor in editors:
        if editor in bots:
            editors.remove(editor)

    distinct_editors = list(set(editors))

    freq = []
    for editor in distinct_editors:
        freq.append(editors.count(editor))

    diversity = math.log10((statistics.pvariance(freq)) ** 0.5 / statistics.mean(freq) * 100)
    return diversity


def experience_diversity(article):
    editors = list(set(get_editors_of_article(article)))
    contributions = get_editor_contributions()
    bots = get_all_bots()
    for editor in editors:
        if editor in bots:
            editors.remove(editor)

    freq = []
    for editor in editors:
        freq.append(contributions[editor])

    diversity = math.log10((statistics.pvariance(freq)) ** 0.5 / statistics.mean(freq) * 100)
    return diversity


'''
s = time.time()
print(experience_diversity('Conical surface'))
e = time.time()
print(e-s)
with open("articles_data.json", "r") as fh:
    all_data = json.load(fh)

all_articles = all_data['all_articles']
s = time.time()
avg = 0
for article in all_articles:
    ss = time.time()
    print(article)
    print(experience_diversity(article))
    ee = time.time()
    avg += ee - ss
e = time.time()
print(e-s, avg/len(all_articles))
'''

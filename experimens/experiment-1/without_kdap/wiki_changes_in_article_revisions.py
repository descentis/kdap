from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from bs4 import BeautifulSoup as bsoup
import mwparserfromhell as mwph
import nltk
import requests


def diff_rev(rv1, rv2):
    url = 'https://en.wikipedia.org/w/api.php?action=compare&format=json&fromrev=' + rv1 + '&torev=' + rv2
    r = requests.get(url)
    data = r.json()
    soup = bsoup('<table>' + data['compare']['*'] + '</table>', 'lxml')
    additions = [bsoup(str(tag), 'lxml').text for tag in soup.find_all('ins', {'class': 'diffchange diffchange-inline'})]
    deletions = [bsoup(str(tag), 'lxml').text for tag in soup.find_all('del', {'class': 'diffchange diffchange-inline'})]
    return additions, deletions


def clean_text(text):
    chars = ['`', '"', "'", ';', ':', '<', '>', '/', '\\', '|', '[', ']', '{', '}', '=', '+', '-', '_', '@', '(', ')']
    for char in chars:
        text = text.replace(char, '')
    return text


def get_delta_data(changes):
    delta_data = {'words': 0, 'sentences': 0, 'wikilinks': 0}
    for change in changes:
        wikitext = mwph.parse(change)
        delta_data['wikilinks'] += len(wikitext.filter_wikilinks())
        cleaned_addition = clean_text(change)
        sentences = remove_punctuation(nltk.sent_tokenize(cleaned_addition))
        print(sentences)
        delta_data['sentences'] += len(sentences)
        words = remove_punctuation(nltk.word_tokenize(cleaned_addition))
        print(words)
        delta_data['words'] += len(words)

    return delta_data


def revision_changes(article_name):
    revisions = get_revisions_of_article(article_name, rvprop='ids')[article_name]
    print(len(revisions))
    revisions.reverse()
    revisions_delta = {}
    for i in range(len(revisions) - 1):
        additions, deletions = diff_rev(str(revisions[i]['revid']), str(revisions[i+1]['revid']))
        add_data = get_delta_data(additions)
        del_data = get_delta_data(deletions)
        revisions_delta[revisions[i+1]['revid']] = {'additions': {}, 'deletions': {}}
        revisions_delta[revisions[i+1]['revid']]['additions'] = add_data
        revisions_delta[revisions[i+1]['revid']]['deletions'] = del_data

    return revisions_delta


def remove_punctuation(words):
    return [word for word in words if word not in ['.', '!', ',', ';', ':', '(', ')', '"', "'", '/', '-', '_', '=', '+',
                                                   "''", "'''", 'http', 'https', ',', '[', ']', '{', '}', '|', '\\',
                                                   '"', '``', '`', '<', '>', '--', '%', '#']]


def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    import os
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem


import time

st = time.time()
sm = memory_usage_psutil()
revision_changes("Indian Institute of Technology Ropar")
et = time.time()
em = memory_usage_psutil()
print(et - st)
print(em - sm)
'''
def filter_elements(text, start_chars, end_chars):
    s = 0
    while text.find(start_chars, s) != -1:
        s = text.find(start_chars, s)
        e = text.find(end_chars, s)
        text = text[:s] + text[e + (len(end_chars) if e + len(end_chars) < len(text) else 0):]

    return text

def count_in_article(article_name):
    soup = bsoup(requests.get('https://en.wikipedia.org/wiki/Special:Export/' + article_name).text, 'lxml')
    pagetext = soup.find('text').text

    wikilinks = mwph.parse(pagetext).filter_wikilinks()
    for wl in wikilinks:
        if wl[:7].lower() == '[[file:' or wl[:11].lower() == '[[category:':
            pagetext = pagetext.replace(str(wl), '')

    for wl in wikilinks:
        if wl[:7].lower() != '[[file:' and wl[:11].lower() != '[[category:':
            pagetext = pagetext.replace(str(wl), str(wl)[2:-2])

    wikitemplates = mwph.parse(pagetext).filter_templates()
    for wt in wikitemplates:
        pagetext = pagetext.replace(str(wt), '')

    comments = mwph.parse(pagetext).filter_comments()
    for comment in comments:
        pagetext = pagetext.replace(str(comment), '')

    external_links = mwph.parse(pagetext).filter_external_links()
    for ex_l in external_links:
        pagetext = pagetext.replace(str(ex_l), '')

    headings = mwph.parse(pagetext).filter_headings()
    for heading in headings:
        pagetext = pagetext.replace(str(heading), str(heading).strip('='))

    html_entities = mwph.parse(pagetext).filter_html_entities()
    for h_ent in html_entities:
        pagetext = pagetext.replace(str(h_ent), '')

    pagetext = filter_elements(pagetext, '{| class="wikitable', '|}')
    pagetext = filter_elements(pagetext, '{| class="infobox', '|}')
    pagetext = filter_elements(pagetext, '{| class="floatright', '|}')
    pagetext = filter_elements(pagetext, '{{cite', '}}')
    pagetext = filter_elements(pagetext, '<', '>')

    count_dict = {'wikilinks': len(wikilinks),
                  'words': len(remove_punctuation(nltk.word_tokenize(pagetext))),
                  'sentences': len(nltk.sent_tokenize(pagetext))}

    return count_dict
'''

'''
print(revision_changes('Talk:Evan Amos'))
[[File:U.S. Territorial Acquisitions.png|thumb|left|upright=1.4|United States territorial acquisitions|U.S. territorial acquisitionsportions of each territory were granted statehood since the 18th century.]]
'''

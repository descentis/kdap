import json


def get_all_bots():
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    bots = all_data['all_bots']
    return bots


def get_editors_of_article(article):
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    editors = all_data['article_editors'][article]
    return editors


def get_revisions_of_article(article):
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    revisions = all_data['article_revisions'][article]
    return revisions


def get_article_talk_page_revisions(article):
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    talk_page_revisions = all_data['article_talk_page_edits'][article]
    return talk_page_revisions


def get_editor_contributions():
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    contributions = all_data['editor_contribution']
    return contributions


with open("articles_data.json", "r") as fh:
    all_data = json.load(fh)

"""
# with open("articles_data.json", "r") as fh:
#    all_data = json.load(fh)

article_editors = all_data['article_editors']
mn = list(article_editors.keys())[0]
for article in article_editors:
    if len(set(article_editors[article])) < len(set(article_editors[mn])):
        mn = article
print(article)
"""
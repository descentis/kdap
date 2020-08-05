from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from crowd_diversity.wiki_get_article_quality import get_articles_quality
from crowd_diversity.wiki_get_editor_contribution import get_editor_contribution_to_wikipedia
import json
from blm.wikiExtract import wikiExtract
import time

def get_all_articles_data(categories):
    # getting all the articles and quality data
    with open("sample_articles.txt", "r", encoding='utf8') as fh:
        all_articles = [article.strip() for article in fh.readlines()][:100]

    articles_quality = {}
    category_articles = {}
    for article in all_articles:
        if article[:14].lower() == 'category talk:':
            all_articles.remove(article)
        if article[:11].lower() == 'draft talk:':
            all_articles.remove(article)

    for article in all_articles:
        quality = get_articles_quality(article)
        if article in quality.keys():
            for category in quality:
                if category in categories:
                    if category in category_articles.keys():
                        category_articles[category].append(article)
                    else:
                        category_articles[category] = [article]
                    quality = {category: quality[category]['class']}
                    break
            if len(quality.keys()) != 1:
                print("Quality error (either multiple or no category assessments matching article):", article, quality)
                all_articles.remove(article)
            else:
                articles_quality[article] = quality
        else:
            all_articles.remove(article)
            print('Removed ', article, 'Since it has no quality data', quality)

    print("Fetched articles and quality", time.time())

    # getting all bots
    w = wikiExtract()
    all_bots_raw = w.get_articles_by_category('All Wikipedia bots')['All Wikipedia bots']
    all_bots = []
    for raw in all_bots_raw:
        all_bots.append(raw['title'][5:])

    print("Fetched all bots", time.time())

    # getting all revisions and editors of articles, removing articles with only one editor
    editors = {}
    all_editors = []
    revisions = {}
    for article in all_articles:
        revisions[article] = get_revisions_of_article(article, rvprop='ids|timestamp|flags|comment|user|sha1')[article]
        article_editors = []
        for revision in revisions[article]:
            if revision.get('user') is not None and revision['user'] not in all_bots:
                article_editors.append(revision['user'])

        if len(set(article_editors)) < 2:
            all_articles.remove(article)
            del revisions[article]
            for category in categories:
                if article in category_articles[category]:
                    category_articles[category].remove(article)
                    break
        else:
            editors[article] = article_editors
            all_editors.extend(article_editors)

    all_editors = list(set(all_editors))

    print("Fetched all editors", time.time())
    print(len(all_editors))
    # getting editor contributions
    editor_contributions = {}
    for editor in all_editors:
        print(editor, len(list(editor_contributions.keys())), 'of', len(all_editors))
        editor_contributions[editor] = get_editor_contribution_to_wikipedia(editor)

    print("Fetched all editor contributions", time.time())

    # getting article talk page edit history
    talk_page_edits = {}
    for article in all_articles:
        talk_page_edits[article] = get_revisions_of_article('Talk:' + article,
                                                            rvprop='ids|timestamp|flags|comment|user|sha1')['Talk:' +
                                                                                                            article]

    print("Fetched talk page edits", time.time())
    # storing data as json
    with open("articles_data.json", "w") as fh:
        json.dump({"categories": categories,
                   "category_articles": category_articles,
                   "all_articles": all_articles,
                   "article_editors": editors,
                   "all_editors": all_editors,
                   "all_bots": all_bots,
                   "editor_contribution": editor_contributions,
                   "article_revisions": revisions,
                   "article_quality": articles_quality,
                   "article_talk_page_edits": talk_page_edits}, fh)


'''
get_all_articles_data(['Geography', 'History', 'Philosophy', 'Religion', 'Mathematics', 'Sociology', 'Technology',
                       'Science', 'Culture'])
'''

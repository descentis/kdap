import requests


def get_articles_quality(articles, category=''):
    url1 = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageassessments&titles="
    quality_dict = {}
    if type(articles) != list:
        articles = [articles]

    for article in articles:
        url = url1 + article
        while True:
            r = requests.get(url)
            data = r.json()
            pages = data['query']['pages']
            for page in pages:
                if pages[page].get('pageassessments') is not None:
                    assessments = pages[page]['pageassessments']
                    if category != '':
                        if category in assessments:
                            quality_dict[article] = {category: assessments[category]}
                    else:
                        if article in quality_dict.keys():
                            quality_dict[article].update(assessments)
                        else:
                            quality_dict[article] = assessments
                else:
                    print('wiki_get_article_quality.py: NO pageassessments for ', article)
            if data.get('continue') is not None:
                url = url + '&pacontinue=' + data['continue']['pacontinue']
            else:
                break

        if article not in quality_dict.keys():
            print("wiki_get_article_quality.py ERROR: No matching quality category", article)
    return quality_dict


'''
print(get_articles_quality('Cleopatra'))
'''

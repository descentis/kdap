import requests
# import time


def get_revisions_of_article(article_name, rvprop=''):
    url1 = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles="
    revisions_dict = {}
    url = url1 + article_name
    if rvprop != '':
        url = url + '&rvprop=' + rvprop
    revisions_list = []

    while True:
        r = requests.get(url)
        data = r.json()
        pages = data['query']['pages']
        if data.get('warnings'):
            print(data['warnings'])
        for page in pages:
            if 'revisions' in pages[page]:
                for i in pages[page]['revisions']:
                        revisions_list.append(i)

        if data.get('continue') is not None:
            url = url + '&rvcontinue=' + data['continue']['rvcontinue']
        else:
            break

    revisions_dict[article_name] = revisions_list
    return revisions_dict



# d=get_revisions_of_article('Indian_Institute_of_Technology_Ropar', rvprop='user|timestamp|comment|sha1|content')

# print(d['Indian_Institute_of_Technology_Ropar'])

import requests
# import time


def get_editors_of_article(article_name):
    url1 = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles="
    editors_dict = {}
    url = url1 + article_name
    editors_list = []

    while True:
        r = requests.get(url)
        data = r.json()
        pages = data['query']['pages']

        for page in pages:
            for i in pages[page]['revisions']:
                t = i.get("user")
                if t is not None:
                    editors_list.append(i["user"])

        if data.get('continue') is not None:
            url = url + '&rvcontinue=' + data['continue']['rvcontinue']
        else:
            break
    editors_list = list(set(editors_list))
    editors_dict[article_name] = editors_list
    return editors_dict


'''
start = time.time()
d=get_editors_of_article('Coffee')
end=time.time()
print(end-start, len(d['Coffee']), d['Coffee'])
'''

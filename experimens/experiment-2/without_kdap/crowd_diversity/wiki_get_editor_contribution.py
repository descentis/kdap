import requests


def get_editor_contribution_to_wikipedia(editor):
    url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=users&usprop=editcount&ususers=' + editor
    r = requests.get(url)
    data = r.json()
    if data['query']['users'][0].get('editcount') is not None:
        contribution = data['query']['users'][0]['editcount']
    else:
        contrib_list = []
        url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&uclimit=500&ucuser=' + \
              editor
        while True:
            r = requests.get(url)
            data = r.json()
            contrib_list.extend(data['query']['usercontribs'])
            if data.get('continue') is not None:
                url = url + '&uccontinue=' + data['continue']['uccontinue']
            else:
                break
        contribution = len(contrib_list)

    return contribution


'''
print(get_editor_contribution_to_wikipedia('Charles Matthews'))
'''

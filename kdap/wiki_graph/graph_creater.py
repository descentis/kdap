
'''
Given a set of wikipedia articles, this program creates the Wikipedia induced
subgraph.
'''
import wikipedia
import pycountry
import requests
import mwparserfromhell as mw


def get_graphi_by_list(article_names): # to create the induced subgraph using article names as list
    """Create induced subgraph based on list of articles provided

    Parameters
    ----------
    article_names : list[str]
        List of articles to use for subgraph

    """
    adj_list = {}

    for article_name in article_names:
        adj_list[article_name] = []

    for article in article_names:
        wiki_names = wikipedia.search(article)

        if article in wiki_names:
            page = wikipedia.page(article)
            page_links = page.links
            for new_page in page_links:
                if new_page in article_names:
                    adj_list[article].append(new_page)

        else:
            page = wikipedia.page(wiki_names[0])
            page_links = page.links
            for new_page in page_links:
                if new_page in article_names:
                    adj_list[article].append(new_page)

    return adj_list


def get_graph_by_name(article_name):
    wiki_names = wikipedia.search(article_name)

    if article_name in wiki_names:
        article = article_name
    else:
        print("The same name article has not been found. Using the name as: "+wiki_names[0])
        article = wiki_names[0]

    page = wikipedia.page(article)
    page_links = page.links

    adj_list = {}
    for page_link in page_links:
        adj_list[page_link] = []

    for articles in page_links:
        try:
            new_page = wikipedia.page(articles)
        except:
            print(articles+" page not found. Skipping to next article")
        new_links = new_page.links
        for link in new_links:
            if link in page_links:
                adj_list[articles].append(link)

    return adj_list


def get_inter_graph(article_list, *args, **kwargs):
    """
    Returns the induced subgraph of wikiarticles provided in the 'article_list'

    Parameters
    ----------
    article_list: list[str]
        list of Wikipedia article names e.g ['India', 'United States']
    file_name: str, optional
        name of the file by which you want to save the graph e.g file_name='sample'
    """
    adj_list = {}
    article_name = []
    for article in article_list:
        article = str(article)
        wiki_names = wikipedia.search(article)
        #print(wiki_names)
        if article in wiki_names:
            pass
        else:
            print("The same name article: "+str(article)+" has not been found. Using the name as: "+wiki_names[0])
            article = wiki_names[0]

        adj_list[article] = []
        article_name.append(article)
    
    for article in article_name:
        try:
            page = wikipedia.page(article)
        except:
            print('page may not be found')

        page_links = page.links
        for link in page_links:
            if link in article_name:
                adj_list[article].append(link)
    
    if kwargs.get('file_name')!=None:
        file_name = kwargs['file_name']+'.graphml'
    else:
        file_name = 'sample.graphml'

    return adj_list


def all_countries_graph(*args, **kwargs):
    if kwargs.get('country_list') != None:
        list_countries = kwargs['country_list']
    else:
        list_countries = []
        for c in pycountry.countries:
            list_countries.append(str(c.name))
    
    return get_inter_graph(list_countries, file_name='countries_graph')
    

def cities_by_country_graph():
    
    list_cities = []
    with open('../cities_india.txt','r') as myFile:
        for line in myFile:
            line = line.split('$@$')
            list_cities.append(line[1])
    
    get_inter_graph(list_cities)


def get_cities_by_country(country_name):
    """
    Creates a graph of city wikiarticles in the provided country name

    Parameters
    ----------
    country_name: str
        Name of the country for which you want to create the graph e.g "India"
    """
    article_name = 'List_of_cities_in_'+country_name+'_by_population'
    wiki_names = wikipedia.search(article_name)
    #print(wiki_names)
    if article_name in wiki_names:
        pass
    else:
        print("The same name article: "+str(article_name)+" has not been found. Using the name as: "+wiki_names[0])
        article = wiki_names[0]
    url = 'https://en.wikipedia.org/w/api.php?action=parse&prop=wikitext&format=json&page='+article 
    r = requests.get(url)
    data = r.json()
    wikiText = data['parse']['wikitext']['*']
    iterate = False
    cities_list = []
    for line in wikiText.splitlines():
        #with open('united.txt','a') as myFile:
        #    myFile.write(line+'\n')
        
        if 'wikitable sortable' in line:
            #print('Yes')
            iterate=True
        if iterate:
            #print(line)
            p = mw.parse(line)
            try:
                cities_list.append(p.filter_wikilinks()[0].title)
            except:
                pass
        if iterate and '|}' in line:
            break
        
    
    #print(cities_list)
    return get_inter_graph(cities_list, file_name=country_name)


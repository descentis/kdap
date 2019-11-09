
'''
Given a set of wikipedia articles, this program creates the Wikipedia induced
subgraph.
'''
import wikipedia
import networkx as nx 
import pycountry
'''
Following method is used to create the induced subgraph based
on the list of articles provided.
'''
def get_graphi_by_list(article_names): # to create the induced subgraph using article names as list

    G = nx.DiGraph()
    G.add_nodes_from(article_names)

    for article in article_names:
        wiki_names = wikipedia.search(article)
        if article in wiki_names:
            page = wikipedia.page(article)
            page_links = page.links
            for new_page in page_links:
                if new_page in article_names:
                    G.add_edge(article, new_page)

        else:
            page = wikipedia.page(wiki_names[0])
            page_links = page.links
            for new_page in page_links:
                if new_page in article_names:
                    G.add_edge(article, new_page)

    nx.write_graphml(G, 'test.graphml')

def get_graph_by_name(article_name):

    G = nx.DiGraph()
    wiki_names = wikipedia.search(article_name)
    if article_name in wiki_names:
        article = article_name
    else:
        print("The same name article has not been found. Using the name as: "+wiki_names[0])
        article = wiki_names[0]
    page = wikipedia.page(article)
    page_links = page.links
    G.add_nodes_from(page_links)

    for articles in page_links:
        try:
            new_page = wikipedia.page(articles)
        except:
            print(articles+" page not found. Skipping to next article")
        new_links = new_page.links
        for link in new_links:
            if link in page_links:
                G.add_edge(articles, link)
        
    nx.write_graphml(G, article_name+'.graphml')

def get_inter_graph(article_list):
    G = nx.DiGraph()
    article_name = []
    for article in article_list:
        wiki_names = wikipedia.search(article)
        if article in wiki_names:
            pass
        else:
            print("The same name article: "+article+" has not been found. Using the name as: "+wiki_names[0])
            article = wiki_names[0]
        G.add_node(article)
        article_name.append(article)
    
    for article in article_name:
        try:
            page = wikipedia.page(article)
        except:
            print('page may not be found')
        page_links = page.links
        for link in page_links:
            if link in article_name:
                G.add_edge(article,link)
                
    nx.write_graphml(G, 'cities_graph.graphml')

def all_countries_graph():
    
    list_countries = []
    for c in pycountry.countries:
        list_countries.append(str(c.name))
    
    get_inter_graph(list_countries)
    

def cities_by_country_graph():
    
    list_cities = []
    with open('../cities_india.txt','r') as myFile:
        for line in myFile:
            line = line.split('$@$')
            list_cities.append(line[1])
    
    get_inter_graph(list_cities)




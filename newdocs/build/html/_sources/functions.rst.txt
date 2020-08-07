.. _functions_toplevel:
.. currentmodule:: kdap.analysis.knol

==================
Functions Overview
==================

This page contains the list of functions and their implementation details

Extraction Methods
==================
The following functions download/crawl/extract the data from collaborative knowledge building portals.
Currently we support only the mining of Wikipedia and Stack Exchange network. the future release will support
the extraction and analysis of portals such as GitHub, Reddit, and Quora.

.. autofunction:: download_dataset
.. autofunction:: get_wiki_article

Frame Methods
=============
The following methods are used to extract the knolml articles in frames and use them to analyze each instance/revision/thread separately

.. autofunction:: frame

Graph Methods
=============
The following methods are used to create the wiki graph using the wikilinks of the articles.
Users can use one of these methods to create the wiki graph according to the requirement.

.. code:: python

    def get_graph_by_wikiarticle(self, article_name):
        '''
        **Does not require dataset download*

        This method takes an article name as an argument and creates the induced subgraph
        among the articles present in there.

        *Arguments*

        article_name:
            Type: String
            The name of the article for which the interwiki graph has to be created.

        e.g knol.get_graph_by_wikiarticle('India')
        '''

    def get_graph_by_wikiarticle_list(self, article_list, *args, **kwargs):
        '''
        **Does not require dataset download**

        This method takes a list of articles name as an argument and creates the induced subgraph
        among the articles using the wikilinks.

        *Arguments*

        article_list:
            Type: List of strings
            The list of articles name for which the interwiki graph has to be created.
        file_name:
            optional
            file name by which you want to create the graph

        eg. knol.get_graph_by_wikiarticle_list(['India', 'Pakistan'], file_name='relation')
        '''

    def get_graph_by_wikiarticle_countries(self, *args, **kwargs):
        '''
        **Does not require dataset download**

        This method creates the induced subgraph among the articles of all the
        wikipedia pages of all the countries using the wikilinks.

        *Arguments*

        country_list:
            optional
            Type: List of strings
            The list of countries name for which the interwiki graph has to be created.
            When not set, the graph is created for all the countries

        e.g knol.get_graph_by_wikiarticle_countries()
        '''

    def get_graph_by_wikiarticle_cities(self, country_name):

        '''
        **Does not require dataset download**

        This method creates the induced subgraph among the articles of all the
        wikipedia pages of all the cities of a given country using the wikilinks.

        *Arguments*

        country_name:
            Type: string
            The country name for which the city graph has to be created.


        e.g knol.get_graph_by_wikiarticle_cities('United States')
        '''

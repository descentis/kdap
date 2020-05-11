.. _functions_toplevel:

.. highlight:: python

==================
Functions Overview
==================

This page contains the list of fucntions and their implementation details

Frame Methods
=============
The following methods are used to extract the knolml articles in frames and use them to analyze each instance/revision/thread saperately

.. code:: python

    def frame(self, *args, **kwargs):
        '''
        **Requires dataset to be present**
        This method takes file names as an argument and returns the list of frame objects
        
        *Arguments*
        
        file_name:
            optional
            Type: String
            The name of the article for which the frame objects have to be created.
        
        dir_path:
            optional
            Type: String
            The path of the directory containing the knolml files
            
        e.g frame = knol.frame()
        
        '''

Graph Methods
=============
The following methods are used to create the wiki graph using the wikilinks of the articles. 
Users can use one of these methods to create the wiki graph according to the requirement.

.. code:: python

    def get_graph_by_wikiarticle(self, article_name):
        
        **Does not require dataset download**
        
        This method takes an article name as an argument and creates the induced subgraph
        among the articles present in there.
        
        *Arguments*
        
        article_name:
            Type: String
            The name of the article for which the interwiki graph has to be created.
        
        e.g knol.get_graph_by_wikiarticle('India')
        

    def get_graph_by_wikiarticle_list(self, article_list, *args, **kwargs):
        
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
        

    def get_graph_by_wikiarticle_countries(self, *args, **kwargs):
        
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


    def get_graph_by_wikiarticle_cities(self, country_name):
        
        **Does not require dataset download**
        
        This method creates the induced subgraph among the articles of all the 
        wikipedia pages of all the cities of a given country using the wikilinks.
        
        *Arguments*
        
        country_name:
            Type: string
            The country name for which the city graph has to be created.
            
        
        e.g knol.get_graph_by_wikiarticle_cities('United States')

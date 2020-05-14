.. _functions_toplevel:

.. highlight:: python

==================
Functions Overview
==================

This page contains the list of fucntions and their implementation details

Extraction Methods
==================
The following functions download/crawl/extract the data from collaborative knowledge building portals.
Currently we support only the mining of Wikipedia and Stack Exchange network. the future release will support
the extraction and analysis of portals such as GitHub, Reddit, and Quora.

.. code:: python

	def download_dataset(sitename, *args, **kwargs):
		'''
		Downloads the dataset of portal and stores it in KnolML format

		**Arguments**
		site_name:
			Type: String
			sitename for which you want to download the dataset e.g wikipedia
		destdir:
			optional
			default: None
			Type: String
			full path of the directory where you want to store the dataset
			e.g destdir='home/download'
		download:
			optional
			default: True
			Type: Bool
			if set true, will download the dataset, e.g download=True
		compress:
			optional
			default: False
			Type: Bool
			if set true, will compress the revision based data like Wikipedia
			e.g compress=True
		article_list:
			optional
			default: None
			Type: List
			list of articles for which full revision history needs to be extracted
			works only when sitename='wikipedia'
			e.g article_list=['India', 'Australia']
		category_list:
			optional
			default: None
			Type: List
			List of categories for which wiki articles need to be downloaded
			Works only if sitename='wikipedia' e.g. category_list=['Black Lives Matter']
		template_list:
			optional
			default: None
			Type: List
			List of template for which wiki articles need to be downloaded
			Works only if sitename='wikipedia' e.g. template_list=['Black Lives Matter']
		wikipedia_dump:
			optional
			default: None
			Type: String
			full path of the directory containing the full Wikipedia bzip2 dump
			Works only when sitename='wikipedia'
		portal:
			optional
			default: None
			Type String
			portal name of the Stack Exchange site which needs to be downloaded
			woeks only when sitename='stackexchange'
			e.g. portal='anime'
		'''

    def get_wiki_article(self, article_name, *args, **kwargs):
        '''
        This method downloads the wikiarticle provided in the arguments
        
        *Arguments*
        
        article_name:
            default: None
            Type: String
            name of the wiki article which needs to be downloaded in knolml format
            e.g. 'Indian Institute of Technology Ropar'
        
        output_dir:
            optional
            default: None
            Type: String
            full path of the directory where the file needs to be stored
            e.g. output_dir='/home/documents'
        compress:
            optional:
            default: False
            Type: Bool
            If true the file will be stored in compressed form
            e.g. compress=True            
        '''

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
            
        e.g frame = knol.frame('sample.knolml')
        
        '''

    def is_question(self):
        '''
        Retruns True if the instance is a question
        Works with QnA based knolml dataset
        '''
        
    def is_answer(self):
        '''
        Retruns True if the instance is an answer
        Works with QnA based knolml dataset
        '''
        
    def is_comment(self):
        '''
        Retruns True if the instance is a comment
        Works with QnA based knolml dataset
        '''
    
    def is_closed(self):
        '''
        Retruns True if the qna thread is closed
        Works with QnA based knolml dataset
        '''
        
    def get_editor(self):
        '''
        Retruns the edior details
        '''
    
    def get_title(self):
        '''
        Retruns the title
        '''
        return self.instanceTitle
    
    def get_tags(self):
        '''
        Retruns the tag details
        Works for QnA dataset
        '''
    
    def get_timestamp(self):
        '''
        Retruns the timestamp details
        '''  
    
    def get_score(self):
        '''
        Retruns the score details
        '''
        
    def get_text(self, *args, **kwargs):
        '''
        Retruns the text data
        '''

    
    def get_bytes(self):
        '''
        Retruns the bytes detail
        '''
                           

    def __count_words(self, text):
        '''
        Retruns number of words in the text
        
        **Arguments**
        text:
            Type: string
        '''
                      
    
    def __get_emailid(self, text):
        '''
        Retruns the email ids in the text
        
        **Arguments**
        text:
            Type: string
        '''
    
    def __get_url(self, text):
        '''
        Retruns all the the urls in the text
        
        **Arguments**
        text:
            Type: string
        '''
    
    def get_text_stats(self, *args, **kwargs):
        '''
        Retruns the email ids in the text
        
        **Arguments**
        title:
            optional
            Type: bool
        
        count_words:
            optional
            type: string
        
        email_id:
            optional
            type: string
        
        url:
            optional
            type: string
                
        '''


Graph Methods
=============
The following methods are used to create the wiki graph using the wikilinks of the articles. 
Users can use one of these methods to create the wiki graph according to the requirement.

.. code:: python

    def get_graph_by_wikiarticle(self, article_name):
        '''
        **Does not require dataset download**
        
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

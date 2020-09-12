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
.. autofunction:: get_wiki_article_by_class
.. autofunction:: get_instance_date
.. autofunction:: get_pageviews
.. autofunction:: get_num_instances
.. autofunction:: get_editors
.. autofunction:: get_author_edits

Frame Methods
=============
The following methods are used to extract the knolml articles in frames and use them to analyze each instance/revision/thread separately

.. autofunction:: frame

``frame`` returns a generator function that sequentially yields ``instances`` class objects to analyse each revision/thread separately

.. autoclass:: kdap.analysis.instances
   :members:

Graph Methods
=============
The following methods are used to create the wiki graph using the wikilinks of the articles.
Users can use one of these methods to create the wiki graph according to the requirement.

.. autofunction:: kdap.wiki_graph.graph_creater.get_graphi_by_list
.. autofunction:: kdap.wiki_graph.graph_creater.get_graph_by_name
.. autofunction:: kdap.wiki_graph.graph_creater.get_inter_graph
.. autofunction:: kdap.wiki_graph.graph_creater.all_countries_graph
.. autofunction:: kdap.wiki_graph.graph_creater.cities_by_country_graph
.. autofunction:: kdap.wiki_graph.graph_creater.get_cities_by_country
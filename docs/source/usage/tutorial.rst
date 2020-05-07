.. _tutorial_toplevel:

.. highlight:: python

==================
Getting Started
==================

Using kdap is very simple. You only need to create `knol`: this class will create the knol object which can be further used to call the kdap methods. For example::

    import kdap
    knol = kdap.knol()
    knol.get_wiki_article('India',[output_dir])

will download the full revision history of India article in KnolMl format, where output_dir is an optional argument to be provided without the brackets as a string. kdap makes the data extraction process super simple.
Sampeling dataset from Wikipedia or Stack Exchage requires only a few lines of code. For example, suppose you want random five articles
from each category of Wikipedia classes::
    
    from random import sample
    category_list = ['FA', 'GA', 'B', 'C', 'Start', 'Stub']
    articles = {}
    for category in category_list:
        articles[category] = sample(knol.get_wiki_article_by_class(wiki_class=category), 5)

The above code will return the names of the Wikipedia articles randomly sampled from each category.
With KnolMl dataset present in local system, you can perform various analysis on it. For example::

    revisions = knol.get_num_instances(dir_path='', granularity='monthly', start='2015-07-01')

Will return a dictionary of month wise number of revisions for all the articles in the provided directory.

Similarly stack exchange data can be analysed using the same methods. For example, finding question of answer ratio requires only few lines of code::

    stack_list = ['3dprinting', 'ai', 'arduino', 'boardgames', 'chemistry', 'chess']
    atoq_ratio = []
    for portal in stack_list:
        knol.download_dataset(sitename='stackexchange', portal=portal)
        gini_list.append(knol.get_global_gini_coefficient(dir_path=portal+'/Posts'))
        questions = knol.get_num_instances(dir_path=portal+'/Posts', instance_type='question')
        answers = knol.get_num_instances(dir_path=portal+'/Posts', instance_type='answer')   
        atoq_ratio.append(questions['questions']/answers['answers'])
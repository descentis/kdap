.. _tutorial_toplevel:

.. highlight:: python

==================
Getting Started
==================

Using kdap is very simple. You only need to create `knol`: this class will create the knol object which can be further used to call the kdap methods. For example,
let's get the revision history for the Wikipedia article on India ::

    import kdap
    knol = kdap.knol()
    knol.get_wiki_article('India',[output_dir])

This will download the full revision history of India article in KnolMl format, where output_dir is an optional argument to be provided without the brackets as a string. kdap makes the data extraction process super simple.

Sampling dataset from Wikipedia or Stack Exchage requires only a few lines of code. For example, suppose we require random five articles
from each category of Wikipedia classes. The following code will suffice::

    from random import sample
    category_list = ['FA', 'GA', 'B', 'C', 'Start', 'Stub']
    articles = {}
    for category in category_list:
        articles[category] = sample(knol.get_wiki_article_by_class(wiki_class=category), 5)

With the KnolMl dataset present in local system, we can perform various analyses on it. For example, suppose we need the
monthly revisions for the India article we downloaded earlier::

    revisions = knol.get_num_instances(file_list=['India'], granularity='monthly', start='2015-07-01')


StackExchange data can be analysed using similar methods. For example, let's find the question to answer ratio for several
StackExchange portals, specified in the list ``stack_list``::

    stack_list = ['3dprinting', 'ai', 'arduino', 'boardgames', 'chemistry', 'chess']
    atoq_ratio = []
    for portal in stack_list:
        knol.download_dataset(sitename='stackexchange', portal=portal)
        questions = knol.get_num_instances(dir_path=portal+'/Posts', instance_type='question')
        answers = knol.get_num_instances(dir_path=portal+'/Posts', instance_type='answer')
        atoq_ratio.append(questions['questions']/answers['answers'])


.. TODO insert code output
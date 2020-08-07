#Knowledge Data Analysis and Processing Platform

This library contains a collection of utilities for efficiently processing and 
analyzing the data of Wiki-based and QnA-based portals (eg., Wikipedia, Wikia, 
Stack Exchange, etc.). The function takes Knol-ML files as input. Most of the 
functions of this library are implemented in such a way that parallel processing
can be achieved.

Documentation is available via [Read The Docs](https://kdap.readthedocs.io/en/latest/usage/installation.html)

##Installing

KDAP requires Python 3.x or later. The full list of package requirements can
 be found in the requirements.txt file.
 
 ###Install Options
 KDAP is easily installed using pip. Assuming pip is installed, just run the
  following command:
 ```bash
pip install kdap 
```

##How to use KDAP
For the full documentation, visit [Read The Docs](https://kdap.readthedocs.io/en/latest/usage/installation.html).

Using kdap is very simple. You only need to create knol: this class will
 create the knol object which can be further used to call the kdap methods. 
 For example:
 ```python3
import kdap
knol = kdap.knol()
knol.get_wiki_article('India',[output_dir])
```
will download the full revision history of India article in KnolMl format, where
 output_dir is an optional argument to be provided without the brackets as a 
 string. kdap makes the data extraction process super simple. Sampling
  dataset from Wikipedia or Stack Exchange requires only a few lines of code.
  
With KnolMl dataset present in local system, you can perform various analysis on
 it. For example:
 ```python3
revisions = knol.get_num_instances(file_list=['India'], granularity='monthly', start='2015-07-01')
```
Will return a dictionary of month wise number of revisions for all the
 articles in the provided directory.
 
 ##Help and Support
 
 Documentation is available at [Read The Docs](https://kdap.readthedocs.io/en/latest/usage/installation.html).
 
 ##Citation
 
 If you make use of this software for your work we would appreciate it if you
  would cite the paper from the Journal of Open Source Software:
 
 ##License
 The kdap package is BSD Licensed.
 
 ##Contributing
 The library is currently in the development phase, feel free to raise an
  issue. We welcome the community to contribute towards KDAP code base and
  ARK dataset. Please check our webpage for more details [GitHub Page](https://kdap.github.io/).
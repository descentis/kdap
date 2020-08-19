[![Build Status](https://travis-ci.org/descentis/kdap.svg?branch=master)](https://travis-ci.org/descentis/kdap)
[![BCH compliance](https://bettercodehub.com/edge/badge/descentis/kdap?branch=master)](https://bettercodehub.com/)
[![PyPI version](https://badge.fury.io/py/kdap.svg)](https://badge.fury.io/py/kdap)
[![Documentation Status](https://readthedocs.org/projects/kdap/badge/?version=latest)](https://kdap.readthedocs.io/en/latest/?badge=latest)


# Knowledge Data Analysis and Processing Platform
This library contains a collection of utilities for efficiently processing and anlyzing the data of Wiki-based and QnA-based portals (eg., Wikipedia, Wikia, Stack Exchange, etc.). The function takes Knol-ML files as input. Most of the functions of this library are implemented in such a way that parallel processing can be achieved.

The library is currently in the development phase, feel free to raise an issue. We welcome the community to contribute towards KDAP code base and ARK dataset.
Please check our webpage for more details [GitHub Page](https://kdap.github.io/)


![Alt Text](https://github.com/descentis/kdap/blob/master/kdap_doc.gif)

## Table of contents
* **[Requirements](#requirements)**
* **[Install](#install)**
* **[Source code](#source-code)**
* **[How to contribute](#how-to-contribute)**
* **[Knol-ML data dump](#Knol-ML-data-dump)**


## REQUIREMENTS

- Python3
- requests==2.21.0
- internetarchive==1.8.5
- numpy
- wikipedia
- psutil>=5.6.6
- mwparserfromhell==0.5.4
- nltk==3.4.5
- matplotlib
- bx-python
- pyunpack
- mwviews

The list of dependencies is shown in `./requirements.txt`, however the installer takes care of installing them for you.

## INSTALL

Installing PyDriller is easily done using pip. Assuming it is installed, just run the following from the command-line:

```
pip install pydriller
```
This will also install the necessary dependencies.

## SOURCE CODE

If you like to clone from source, you can do it with very simple steps.
First, clone the repo:

```
> git clone https://github.com/descentis/kdap.git
> cd kdap
```

## How to contribute
Fork the project and follow the instructions on how to get started with [source code](#source-code). I will be updating the test cases on which you can test your code. Stay tuned.


## License

This software is licensed under the BSD 3-Clause License.

This project has received funding from the CSRI, Department of Science and Technology India via grant no. SR/CSRI/344/2016

## Knol-ML data dump

The data dump can be found [here](https://archive.org/details/KnolML)

.. _intro_toplevel:

==================
Overview / Install
==================

This library contains a collection of utilities for efficiently processing Knol-ML database dumps. There are two important features that this module intends to address: providing standard algorithms and efficient parsing of Knol-ML dump.

Requirements
============

* `Python`_ 3.4 or newer
* `p7zip-full`_

.. _Python: https://www.python.org
.. _p7zip-full: https://itsfoss.com/use-7zip-ubuntu-linux/

Installing kdap
===============

Installing kdap is easily done using `pip`_. Assuming it is installed, just run the following from the command-line:

.. _pip: https://pip.pypa.io/en/latest/installing.html

.. sourcecode:: none

    # pip install kdap


Source Code
===========

kdap's git repo is available on `GitHub <https://github.com/descentis/kdap>`_, and can be cloned using::

    $ git clone https://github.com/descentis/kdap
    $ cd kdap

Optionally (but suggested), make use of virtualenv::

    $ virtualenv -p python3 venv
    $ source venv/bin/activate

Install the requirements::

    $ pip install -r requirements.txt
    $ pip install -r test-requirements.txt
    $ unzip test-repos.zip

and run the tests using pytest::

    $ pytest


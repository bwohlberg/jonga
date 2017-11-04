Overview
========

Jonga is a Python package that generates a directed graph representing
function calls within a block of Python code, intended for inclusion
in Sphinx package documentation. There are a number of
alternative packages with similar goals, including

* `pycallgraph <https://github.com/gak/pycallgraph>`_
* `pyan <https://github.com/davidfraser/pyan>`_
* `snakefood <https://bitbucket.org/blais/snakefood/src>`_

but none of them is entirely suitable for generating function/method call
vizualizations for inclusion within package documentation. In
particular, none of these other packages correctly identifies method
classes within a hierarchy of derived classes.

Jonga is used to generate call graphs to help document the relatively complex class structure in the `SPORCO <http://sporco.readthedocs.io/en/latest/>`_ package, as illustrated in `this example <http://sporco.readthedocs.io/en/latest/_static/jonga/cbpdndl_solve.svg>`_ (note that the method names are clickable, linking to the corresponding entries in the documentation).



Usage Examples
--------------

Scripts illustrating usage of the package can be found in the
``examples`` directory of the source distribution. These examples can
be run from the root directory of the package by, for example

::

   python3 examples/example1.py


To run these scripts prior to installing the package it will be
necessary to first set the ``PYTHONPATH`` environment variable to
include the root directory of the package. For example, in a ``bash``
shell

::

   export PYTHONPATH=$PYTHONPATH:`pwd`


from the root directory of the package.


`Jupyter Notebook <http://jupyter.org/>`_ versions of the example scripts are also available in the same directory. The notebooks can also be viewed online via `nbviewer <https://nbviewer.jupyter.org/github/bwohlberg/jonga/blob/master/index.ipynb>`_, or run interactively at `binder <https://mybinder.org/v2/gh/bwohlberg/jonga/master?filepath=index.ipynb>`_.


Contact
-------

Please submit bug reports, comments, etc. to brendt@ieee.org.




Jonga
=====

.. image:: https://travis-ci.org/bwohlberg/jonga.svg?branch=master
    :target: https://travis-ci.org/bwohlberg/jonga
    :alt: Build Status
.. image:: https://readthedocs.org/projects/jonga/badge/?version=latest
    :target: http://jonga.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://badge.fury.io/py/jonga.svg
    :target: https://badge.fury.io/py/jonga
    :alt: PyPi Release
.. image:: https://static.pepy.tech/personalized-badge/jonga?period=total&left_color=grey&right_color=brightgreen&left_text=downloads
    :target: https://pepy.tech/project/jonga
    :alt: PyPi Downloads
.. image:: https://img.shields.io/conda/vn/conda-forge/jonga.svg
    :target: https://anaconda.org/conda-forge/jonga
    :alt: Conda Forge Release
.. image:: https://img.shields.io/conda/dn/conda-forge/jonga.svg
    :target: https://anaconda.org/conda-forge/jonga
    :alt:  Conda Forge Downloads
.. image:: https://img.shields.io/badge/python-3.3+-green.svg
    :target: https://github.com/bwohlberg/jonga
    :alt: Supported Python Versions
.. image:: https://img.shields.io/pypi/l/jonga.svg
    :target: https://github.com/bwohlberg/jonga
    :alt: Package License
.. image:: http://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/bwohlberg/jonga/master?filepath=examples/index.ipynb
    :alt: Binder
|

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



Requirements
------------

The primary requirement is Python 3.3 or greater (this packages is
*not* compatible with Python 2), imposed by the use of the
``__qualname__`` function attribute and `inspect.getclosurevars
<https://docs.python.org/3/library/inspect.html#inspect.getclosurevars>`_.
The ``__qualname__`` attribute could be replaced in earlier versions
of Python by `qualname <https://github.com/wbolster/qualname>`_, but
there is no obvious replacement for `inspect.getclosurevars
<https://docs.python.org/3/library/inspect.html#inspect.getclosurevars>`_,
which was introduced in Python 3.3.

The other major requirement is `pygraphviz <https://pygraphviz.github.io/>`_.
Under Ubuntu Linux 18.04, this requirement can be installed by the command

::

  sudo apt-get install python3-pygraphviz



Optional
^^^^^^^^

Package `matplotlib <http://matplotlib.org>`_ is required to run the
included `Jupyter Notebook <http://jupyter.org/>`_ examples.

Packages `pytest <https://github.com/pytest-dev/pytest>`_ and
`pytest-runner <https://github.com/pytest-dev/pytest-runner>`_ are
required to run the tests (``python setup.py test`` or ``python3
setup.py test``, depending on the operating system).

Packages `sphinx <http://www.sphinx-doc.org/en/stable>`_,
`sphinx-bootstrap-theme <http://ryan-roemer.github.io/sphinx-bootstrap-theme/README.html>`_,
and `numpydoc <https://github.com/numpy/numpydoc>`_ are required to
build the documentation (``python setup.py build_sphinx`` or
``python3 setup.py build_sphinx``, depending on the operating system).



Usage
-----

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


`Jupyter Notebook <http://jupyter.org/>`__ versions of the example scripts are
also included in the ``examples`` directory, and can be viewed online via
`nbviewer <http://nbviewer.jupyter.org/github/bwohlberg/jonga/blob/master/examples/index.ipynb>`_,
or run interactively at
`binder <https://mybinder.org/v2/gh/bwohlberg/jonga/master?filepath=examples/index.ipynb>`_.



Documentation
-------------

Documentation is available online at
`Read the Docs <http://jonga.rtfd.io/>`_, or can be built from the
root directory of the source distribution by the command

::

   python3 setup.py build_sphinx

in which case the HTML documentation can be found in the
``build/sphinx/html`` directory (the top-level document is
``index.html``).


Contact
-------

Please submit bug reports, comments, etc. to brendt@ieee.org. Bugs and
feature requests can also be reported via the
`GitHub Issues interface <https://github.com/bwohlberg/jonga/issues>`_.




License
-------

This package is made available under the terms of the GNU General
Public License as published by the Free Software Foundation; either
version 2 of the License (see the included ``LICENSE`` file), or
(at your option) any later version.

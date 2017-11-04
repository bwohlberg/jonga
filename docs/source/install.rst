Installation
============

The simplest way to install the most recent release of Jonga from
`PyPI <https://pypi.python.org/pypi/jonga/>`_ is

::

    pip install jonga


Jonga can also be installed from source, either from the development
version from `GitHub <https://github.com/bwohlberg/jonga>`_, or from
a release source package downloaded from `PyPI
<https://pypi.python.org/pypi/jonga/>`_.

To install the development version from `GitHub
<https://github.com/bwohlberg/jonga>`_ do

::

    git clone git://github.com/bwohlberg/jonga.git

followed by

::

   cd jonga
   python setup.py build
   python setup.py install

The install command will usually have to be performed with root
permissions, e.g. on Ubuntu Linux

::

   sudo python setup.py install

The procedure for installing from a source package downloaded from `PyPI
<https://pypi.python.org/pypi/jonga/>`_ is similar.

Note that under Ubuntu Linux, in the commands listed above, ``python``
and ``pip`` should be replaced with ``python3`` and ``pip3``
respectively.



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

The other major requirement is `pygraphviz <https://pygraphviz.github.io/>`_. Under Ubuntu Linux 16.04, this requirement can be installed by the command

::

  sudo apt-get install python3-pygraphviz



Optional
^^^^^^^^

Packages `pytest <https://github.com/pytest-dev/pytest>`_ and
`pytest-runner <https://github.com/pytest-dev/pytest-runner>`_ are
required to run the tests (``python setup.py test`` or ``python3
setup.py test``, depending on the operating system). Packages `sphinx
<http://www.sphinx-doc.org/en/stable>`_ and `sphinx-bootstrap-theme
<http://ryan-roemer.github.io/sphinx-bootstrap-theme/README.html>`_
are required to build the documentation (``python setup.py
build_sphinx`` or ``python3 setup.py build_sphinx``, depending on the
operating system).

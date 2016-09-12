whoarder
========

**whoarder** converts your Kindle's ``My Clippings.txt`` file to a more pleasant, sortable, filterable HTML file:

.. image:: https://github.com/ronjouch/whoarder/raw/master/whoarder-screenshot.png

Installation & Requirements
---------------------------

To install, just ``pip install whoarder`` (`link to PyPI page <https://pypi.python.org/pypi/whoarder/>`_). Requirements are:

* Python ≥3.3 (so far I only tested with 3.3 and 3.4 on Linux, tests and patches to increase compatibility very welcome)

* The ``jinja2`` and ``chardet2`` modules (automatically handled as ``setup.py`` dependencies)

* Only tested on a ``My Clippings.txt`` file produced by a Kindle Paperwhite (ok/ko reports for other devices and test data welcome through `GitHub <https://github.com/ronjouch/whoarder/pulls>`_).

  - Kindle Fire & Kindle Fire HD are not supported, since they do note create the ``My Clippings.txt`` file. If you know where to dig that data for those versions, patches welcome.

Usage
-----

**Command-line**:

Run ``whoarder /path/to/My Clippings.txt [destination]`` . If ``destination`` is omitted, the output HTML will be written in the same place (overwriting any pre-existing HTML).

**As module**::

    from clippings import Clippings
    clippings = Clippings(args.source, args.destination)  # contains a 'clippings' dict containing the information
    clippings.export_to_html()  # exports as HTML

**Tests**:

Test data and ``unittest``-based unit tests are in the ``tests`` folder.

Similar Software
----------------

* Web services

  - `Clippings Converter <http://www.clippingsconverter.com/>`_

  - `Clipper <http://www.claybavor.com/clipper/>`_

* Offline

  - (PHP) `kindle-split-by-book <https://gist.github.com/elvisciotti/1783585>`_

License and contact
-------------------

Licensed under the MIT license, 2013-2016 (see ``LICENSE``), `ronan@jouchet.fr <mailto:ronan@jouchet.fr>`_ / `@ronjouch <https://twitter.com/ronjouch>`_

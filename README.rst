wagtailmodelchooser
======================================

|build-status-image| |pypi-version|

Overview
--------

Wagtail chooser panel generator for generic Django models.

It elegantly completes `wagtail.contrib.modeladmin` and allows a simple selection of
any model instance anywhere in the Wagtail admin.

Requirements
------------

-  Python (2.7, 3.4, 3.5)
-  Django (1.8, 1.9, 1.10)
-  Wagtail (1.5, 1.6)

Installation
------------

Install using ``pip``.

.. code:: bash

    $ pip install wagtailmodelchooser

Example
-------

The most simple usecase, without any customization.

.. code:: python

    from wagtailmodelchooser.edit_handlers import register_chooser_for_model

    ItemChooserPanel = register_chooser_for_model(Item)


For more advanced examples, please refer to the documentation.

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/Naeka/wagtailmodelchooser.svg?branch=master
   :target: http://travis-ci.org/Naeka/wagtailmodelchooser?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/wagtailmodelchooser.svg
   :target: https://pypi.python.org/pypi/wagtailmodelchooser

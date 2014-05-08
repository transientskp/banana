Introduction
============

This is Banana. A new web frontend for TKP. Read all about TKP here on
the `TKP website <http://www.transientskp.org/>`_.

.. image:: https://travis-ci.org/transientskp/banana.png?branch=master 
  :target: https://travis-ci.org/transientskp/banana


Installation
============

to install banana::

    pip install astropy
    pip install -r requirements.txt
    cp bananaproject/settings/local_example.py bananaproject/settings/local.py
    gedit bananaproject/settings/local.py
    ./manage collectstatic
    ./manage runserver


Testing
=======

To run the banana test suite run::

    $ ./manage.py test --settings=testing.settings



Notes
=====

It is possible (and advisable) to run banana in a virtualenv, but matplotlib may
complain about not being able to import the ``PyQT4`` or ``sip`` modules.
The solution to this is to use a non-interactive backend by default.
There is a one-liner matplotlibrc config file included which should be picked
up, at least when running the django-debug server.
For reference however, the necessary edit is to set::

    backend      : agg

Installation
============


Requirements
------------
Banana depends on various 3rd party Python libraries which are defined in
the **requirements.txt** file. You can install the dependencies using `pip
<http://pip.readthedocs.org/>`_::

    $ pip install astropy
    $ pip install -r requirements.txt

Pip cant figure out dependencies correctly in some cases, so you need to
manually install astropy first.


Quick configuration
-------------------

copy the example config file::

    $ cp bananaproject/settings/local_example.py bananaproject/settings/local.py

Now open :mod:`bananaproject.settings.local` in your favorite editor and
configure your database settings.


Runnig the server
-----------------

You can run a Django testing webserver serving the banana project using::

    $ ./manage.py runserver


Deployment
----------

If you want a more permanent implementation and serve Banana so several users it
is adviced to deploy your setup with a dedicated webserver. The Django
project itself has `extended documentation
<https://docs.djangoproject.com/en/1.6/howto/deployment/>`_ on how to do this.


.. note::

    It is possible (and advisable) to run banana in a virtualenv, but matplotlib
    may complain about not being able to import the ``PyQT4`` or ``sip`` modules.
    The solution to this is to use a non-interactive backend by default.
    There is a one-liner matplotlibrc config file included which should be picked
    up, at least when running the django-debug server.
    For reference however, the necessary edit is to set::

        backend      : agg


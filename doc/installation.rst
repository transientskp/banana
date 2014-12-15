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

    $ cp project/settings/local_example.py project/settings/local.py

Now open :mod:`project.settings.local` in your favorite editor and
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

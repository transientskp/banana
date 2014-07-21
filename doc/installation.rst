Installation
============

Requirements
------------
Banana depends on various 3rd party Python libraries which are defined in
the requirements.txt file. You can install the dependencies using `pip
<http://pip.readthedocs.org/>`_::

    $ pip install -r requirements.txt


Deployment
----------

For testing purposes and quick setup a simple **./manage.py runserver** will run
a webserver on localhost, but if you want a more permanent implementation
and serve Banana so several users it is wise to deploy your setup with a
dedicated webserver. The Django project itself has `extended documentation
<https://docs.djangoproject.com/en/1.6/howto/deployment/>`_ on how to do this.


Introduction
============

This is Banana. A new web frontend for TKP. Read all about TKP here on
the `TKP website <http://www.transientskp.org/>`.

.. image:: https://travis-ci.org/transientskp/banana.png?branch=master 
  :target: https://travis-ci.org/transientskp/banana


Installation
============

to install banana::

    pip install -r requirements.txt
    cp bananaproject/settings/local_example.py bananaproject/settings/local.py
    gedit bananaproject/settings/local.py
    ./manage collectstatic
    ./manage runserver


Notes
=====

It is possible (and advisable) to run banana in a virtualenv, but matplotlib may
complain about not being able to import the ``PyQT4`` or ``sip`` modules.
The solution to this is to use a non-interactive backend by default.
There is a one-liner matplotlibrc config file included which should be picked
up, at least when running the django-debug server.
For reference however, the necessary edit is to set::

    backend      : agg



Testing
=======

To run the banana test suite run::

    $ ./manage.py test --settings=testing.settings


Shepherding Banana through schema upgrades
==========================================

Updating the model
------------------

You need to update the ''banana/models.py'' file to reflect the new database
structure. The easy way to do this is as follows:

  - Generate a new database with the schema version you want to upgrade to
    (using, eg, ''tkp-manage.py initdb''). Either MonetDB or Postgres is fine.
  - Get a Banana installation which is able to connect to your database. You'll
    need to edit ''bananaproject/settings/local.py'' to set the appropriate
    hostname, port and password for MonetDB and/or for Postgres. Banana will
    build a list of all the databases on the host you specify, based on the
    assumption that the database name, username and password are all the same.
  - Within your banana directory, dump a set of models representing your new
    database by running: ''./manage.py inspectdb --database=<dbname>'', where
    ''<dbname>'' is just the name of your database (in the case of MonetDB) or
    the string ''postgres_'' followed by the name of your database (for
    Posgtres). This will print the new models to standard out: you'll probably
    want to redirect them to a file (say, ''models-new.py'').
  - Using your favourite tool, update ''banana/models.py'' to reflect the
    additions in ''models-new.py'' (that is, run
    ''vimdiff banana/models.py models-new.py'' or equivalent). Note that
    ''banana/models.py'' has a bunch of useful customization which we don't
    want to lose: **don't** replace it with the new version, but rather
    carefully compare it with the new models and merge only the relevant
    changes.
  - Update the ''schema_version'' variable defined in ''banana/models.py'' to
    reflect the new schema.
  - Check for any templates (stored in ''banana/templates'') which are using
    model fields which you've just removed or renamed, and modify them to use
    the new models.
  - Commit your changes, submit a pull request, and have a cup of tea.


Updating the fixtures
---------------------

The make the test suite pass after a schema change you need to update the
fixtures also:

  - Populate the database with some dataset, not too big but make sure
    all tables are populated (like transient).
  - run ''./manage.py dumpdata --database=postgres_gijs --indent=1 banana > testing/fixtures/initial_data.json''
    to serialize the data into the fixture.
  - Run the test suite and check if all tests are passing
  - If not, fix
  - Issue pull request

Credits
=======

see requirements file, and:

 * Bootstrap
 * Bootstrap-rowlink
 * Highcharts JS

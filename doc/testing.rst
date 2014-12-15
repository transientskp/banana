Testing
=======

You should be careful when running the test suite. Default behavior for Django
is to take your database configuration (which you defined in
:mod:`project.settings.local`, append **_test** to the database name
and attempt to create and destroy this database configuration. You probably
don't want to do this in production. We created a seperate :mod:`testing`
subproject that takes the **banana** configuration but overrides the database
settings to use a safe **sqlite** based database configuration.

Running the test suite
----------------------

To run the banana test suite run::

    $ ./manage.py test --settings=testing.settings



Updating the fixtures
---------------------

Always regenerate the fixtures when you altered the model. You should do this
by populating a TKP database with Mock data.

    - (re)create a database
    - initialise schema with tkp-manage.py initdb
    - run **banana/util/create_content.py** to create mock data. Configure the
      connection using the TKP_DB* environment variables
    - configure the Banana project to use this database
    - dump the db content::

      $ ./manage.py dumpdata --database=%{TK_DBNAME} --indent=1 banana > testing/fixtures/initial_data.json

Travis
------

For every commit to every branch or every issued pull request the `travis build
system <https://travis-ci.org/transientskp/banana>`_ is triggered and will
try to run the test suite for that branch. It will update the github status
page of the branch or pull request according to the test run output (failed or
not).

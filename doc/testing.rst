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

To make the test suite pass after a schema change you need to update the
fixtures also:

  - Populate the database with some dataset, not too big but make sure
    all tables are populated (like transient).
  - to serialize the data into the fixture run::

        $ ./manage.py dumpdata --database=postgres_gijs --indent=1 banana > testing/fixtures/initial_data.json

  - Note that some libraries like **astropy** write things to stdout which ruins
    the json output. Check  the json file to make sure there is no garbage at
    the start of the file.
  - Run the test suite and check if all tests are passing
  - If not, fix
  - Issue pull request


Travis
------

For every commit to every branch or every issued pull request the `travis build
system <https://travis-ci.org/transientskp/banana>`_ is triggered and will
try to run the test suite for that branch. It will update the github status
page of the branch or pull request according to the test run output (failed or
not).

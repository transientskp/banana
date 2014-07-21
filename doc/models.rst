Models
======

**banana.models** contains the Django ORM models. These Object Oriented
representation of a TRAP database. Since you don't initialise the TRAP database
using Django, we need to manually keep the Django models in sync with the TRAP
schema. Below we describe a procedure on how to do this.

Updating the model
------------------

You need to update the **banana/models.py** file to reflect the new database
structure. The easy way to do this is as follows:

  - Generate a new database with the schema version you want to upgrade to
    (using, eg, `tkp-manage.py initdb`). Either MonetDB or Postgres is fine.
  - Get a Banana installation which is able to connect to your database. You'll
    need to edit **bananaproject/settings/local.py** to set the appropriate
    hostname, port and password for MonetDB and/or for Postgres. Banana will
    build a list of all the databases on the host you specify, based on the
    assumption that the database name, username and password are all the same.
  - Within your banana directory, dump a set of models representing your new
    database by running: `./manage.py inspectdb --database=<dbname>`, where
    **<dbname>** is just the name of your database (in the case of MonetDB) or
    the string **postgres_** followed by the name of your database (for
    Posgtres). This will print the new models to standard out: you'll probably
    want to redirect them to a file (say, **models-new.py**).
  - Using your favourite tool, update **banana/models.py** to reflect the
    additions in **models-new.py** (that is, run
    `vimdiff banana/models.py models-new.py` or equivalent). Note that
    **anana/models.py** has a bunch of useful customization which we don't
    want to lose: **don't** replace it with the new version, but rather
    carefully compare it with the new models and merge only the relevant
    changes.
  - Update the **schema_version** variable defined in **banana/models.py** to
    reflect the new schema.
  - Check for any templates (stored in **banana/templates**) which are using
    model fields which you've just removed or renamed, and modify them to use
    the new models.
  - Commit your changes, submit a pull request, and have a cup of tea.
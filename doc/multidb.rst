

Banana and multiple databases
=============================

The way we deploy TRAP and Banana at the University of Amsterdam is that various
scientists create multiple PostgreSQL and MonetDB databases and populate these
with data. We want to be able to visualise the content of all these databases.

We've created various helper functions (:mod:`project.settings.database`)
that assist in automatically populating the Django configuration with our site
specific configuration. It is adviced **not** to use these in production, but
rather build a manual configuration.

The database which is used is based on the URL, specifically the URL variable.
We've crafted a combination of Django middleware and Django database routing
that makes Django use the desired database. Below is the module documentation
for that logic.

Module documentation
--------------------

.. automodule:: project.multidb
   :members:
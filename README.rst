Introduction
============

This is Banana. A new web frontend for TKP. Read all about TKP here on
the `TKP website <http://www.transientskp.org/>`.


Installation
============

to install banana::

    pip install -r requirements.txt
    cp bananaproject/settings/local_example.py bananaproject/settings/local.py
    gedit bananaproject/settings/local.py
    ./manage collectstatic
    ./manage runserver

Finally, it is possible to run banana in a virtualenv, but matplotlib may
complain about not being able to import the ``PyQT4`` or ``sip`` modules.
The solution to this is to use a non-interactive backend by default.
Editing **~/.matplotlib/matplotlibrc** to read::

 backend      : agg

should do the trick.

If running with monetdb, don't forget to run::

  monetdbd set control=yes /path/to/dbfarm
  monetdbd set passphrase=mysecretpassphrase /path/to/dbfarm

And then reboot the monetdb server.


Testing
=======

To run the banana test suite run::

    $ ./manage.py test --settings=testing.settings



Credits
=======

see requirements file, and:

 * Bootstrap
 * Bootstrap-rowlink
 * Highcharts JS

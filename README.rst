Introduction
============

This is Banana. A new web frontend for TKP. Read all about TKP here::

    http://www.transientskp.org/


Installation
============

  $ pip install -r requirements.pip
  $ cp banana/settings/local_example.py banana/settings/local.py
  $ edit banana/settings/local.py
  $ ./manage collectstatic
  $ ./manage runserver


Requirements
============

 * django
 * djonet
 * python-monetdb
 * tkp
 * aplpy

Using
=====

 * Bootstrap
 * Bootstrap-rowlink
 * Highcharts JS

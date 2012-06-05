#!/bin/sh

export PYTHONPATH=${PYTHONPATH}:`pwd`/../djonet
#export PYTHONPATH=${PYTHONPATH}:/home/gijs/Archive/monetdb-python/

monetdb stop django_test
monetdb destroy -f django_test
monetdb create django_test
monetdb release django_test
monetdb start django_test
python manage.py syncdb

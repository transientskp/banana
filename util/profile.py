"""
use this for profiling specific view
"""

# set the view here you want to profile
VIEW = '/postgres_cendesnewaartfaac/dataset/5/'

import os
import cProfile
from django import setup
from django.test import Client

# initialise everything
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
setup()
c = Client()
pr = cProfile.Profile()

# do the profile
pr.enable()
response = c.get(path=VIEW, content_type='text/plain')
pr.disable()
pr.dump_stats('profile.dat')



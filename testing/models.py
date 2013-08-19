"""
sets managed to True for all models in banana so they are created during
syncdb and test commands. Should be only used for testing!
"""

import inspect
from banana.models import *

l = locals()
objects = [l[s] for s in dir()]
models = [c for c in objects if inspect.isclass(c) and
                                issubclass(c, models.Model)]


for m in models:
    m._meta.managed = True

import inspect
from banana.models import *

l = locals()
models = [c for c in [l[s] for s in dir()] if inspect.isclass(c)
                                           and issubclass(c, models.Model)]

for m in models:
    m._meta.managed = True

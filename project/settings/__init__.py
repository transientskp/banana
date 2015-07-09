import logging

msg = "no site specific configuration, please copy " \
      "project/setting/local_example.py to project/settings/local.py"


try:
    from local import *
except ImportError:
    logging.warning(msg)
    from base import *


import logging

msg = "no site specific configuration, please copy " \
      "bananaproject/setting/local_example.py to bananaproject/setting/local.py"


try:
    from local import *
except ImportError:
    logging.warning(msg)
    from base import *


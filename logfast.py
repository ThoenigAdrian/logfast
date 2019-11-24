"""
    Make sure this is the first module you import in your application.
    This makes sure no other call is made first to logging.
    Otherwise other modules/libraries might overwrite the logging settings
    This will allow you to have multiple entrypoints of your application.
"""
import sys
import os
import logging

logging.basicConfig(format='%(asctime)s  %(process)d:%(threadName)s  %(levelname)-10s |%(filename)-s.%(lineno)-4d|   %(message)s',
                    datefmt="%d|%m|%y|%H:%M:%S|%z")

log = logging.getLogger()

if os.environ.get("logfast", False) or any([arg == "logfast" for arg in sys.argv]):
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

"""
    Make sure this is the first module you import in your application.
    This makes sure no other call is made first to logging.
    Otherwise other modules/libraries might overwrite the logging settings
    This allows you to have multiple application entrypoints but have the same logging configuration.
"""
import sys
import os
import logging

logging.basicConfig(format='%(asctime)s  %(process)d:%(threadName)s  %(levelname)-10s |%(filename)-s.%(lineno)-4d|   '
                           '%(message)s',
                    datefmt="%d|%m|%y|%H:%M:%S|%z")

log = logging.getLogger()

getLogger = logging.getLogger
# Pass through for convenience so user doesn't need to import logging
INFO = logging.INFO
DEBUG = logging.DEBUG
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

grey = "\x1b[37;20m"
yellow = "\x1b[33;20m"
green = "\x1b[32;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

class CustomFormatter(logfast.logging.Formatter):
    def __init__(self):
        previous_format = logger.handlers[0].formatter._fmt
        self.formats = {
            logfast.DEBUG: grey + previous_format + reset,
            logfast.INFO: grey + previous_format + reset,
            logfast.WARNING: yellow + previous_format + reset,
            logfast.PASS: green + previous_format + reset,
            logfast.FAIL: red + previous_format + reset,
            logfast.ERROR: red + previous_format + reset,
            logfast.CRITICAL: bold_red + previous_format + reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logfast.logging.Formatter(log_fmt)
        return formatter.format(record)

def setUnittestLogger():
    log.handlers[0].setFormatter(CustomFormatter())
    add_logging_level('SUCCESS', WARNING + 1)
    add_logging_level('FAIL', WARNING + 2)


def add_logging_level(level_name, level_num, method_name=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    5

    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('{} already defined in logger class'.format(method_name))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)


if os.environ.get("logfast") or "logfast" in sys.argv:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

def setLevel(level):
    # Sets the level for all instantiated loggers
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(level)

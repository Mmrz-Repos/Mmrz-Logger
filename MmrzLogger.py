#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import traceback
import logging
import inspect
import os


__FILE__ = os.path.abspath(__file__)
__DIR__ = os.path.dirname(__FILE__)

class MmrzLogger(object):
    def __init__(self, module_name):
        super(self.__class__, self).__init__()

        module_name = os.path.basename(module_name)

        LOG_FILE = os.path.join(__DIR__, "trace.log")
        LOG_LEVEL = logging.DEBUG

        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s %(message)s',
        )

        handler = logging.FileHandler(LOG_FILE)
        handler.setLevel(level=LOG_LEVEL)
        handler.setFormatter(formatter)

        logger = logging.getLogger(module_name)
        logger.setLevel(level=LOG_LEVEL)
        logger.addHandler(handler)

        self._logger = logger

    @property
    def _trace_stack():
        trace_stack = traceback.format_stack()
        last_N_stack = list(trace_stack)[-10:]
        stack_string = "\n" + "".join(last_N_stack)
        return stack_string

    def _log(self, level, msg):
        upper_frame = inspect.currentframe().f_back.f_back
        co_name = upper_frame.f_code.co_name.replace("<", "").replace(">", "")
        co_filename = upper_frame.f_code.co_filename
        self._logger.log(level, "{co_name} - {msg}".format(co_name=co_name, msg=msg))

    def debug(self, msg):
        self._log(logging.DEBUG, msg)

    def info(self, msg):
        self._log(logging.INFO, msg)

    def warn(self, msg):
        self._log(logging.WARNING, msg)

    def error(self, msg):
        self._log(logging.ERROR, msg)


logger = MmrzLogger(__file__)


def error_trace(func, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            logger.error(f"module: {func.__module__}, func: {func.__name__}, msg: {str(e)}, type(e): {type(e)}, exc_traceback: {self._trace_stack}")
    return wrapper

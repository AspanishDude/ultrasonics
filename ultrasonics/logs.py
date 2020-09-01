#!/usr/bin/env python3

"""
logs
The default logging module for ultrasonics, which should be used for logging consistency.

XDGFX, 2020
"""

import logging
import logging.handlers

buffer = {}
handler = {}


def create_log(name):
    # Create logger
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Add streamhandler to logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Add filehandler to logger
    fh = logging.handlers.RotatingFileHandler(
        f"logs/{name}.log",  maxBytes=1048576, backupCount=2)
    fh.setLevel(logging.DEBUG)

    # Apply log formatting
    formatter = []
    formatter.append(logging.Formatter(
        '%(asctime)s: %(name)-22s - %(levelname)-7s - %(message)s'))
    formatter.append(logging.Formatter(
        '%(asctime)s: %(levelname)-7s - %(message)s'))
    ch.setFormatter(formatter[0])
    fh.setFormatter(formatter[1])

    log.addHandler(ch)
    log.addHandler(fh)

    log.debug("LOG CREATED")

    return log


def start_capture(name):
    """
    Start capturing logs for a given module.

    @return: Logger for the selected plugin, should this be needed.
    """
    from io import StringIO

    buffer[name] = StringIO()
    log = logging.getLogger(name)

    handler[name] = logging.StreamHandler(buffer[name])

    formatter = logging.Formatter(
        '%(levelname)-7s - %(message)s')
    handler[name].setFormatter(formatter)

    log.addHandler(handler[name])

    return log


def stop_capture(name):
    """
    Stop capturing logs for a given module.

    @return: Collected logs as string
    """
    log = logging.getLogger(name)
    log.removeHandler(handler[name])

    handler[name].flush()
    buffer[name].flush()

    return buffer[name].getvalue()

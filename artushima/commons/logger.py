"""
The logger for application internal logging.
"""

import os
import time
from datetime import datetime


# Constants for message severity levels
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"


def log(severity, message):
    """
    Log the message to a file with the given severity.
    """

    t = time.time()
    file_timestamp = datetime.fromtimestamp(t).strftime("%Y_%m_%d")
    file_name = "artushima_{}.log".format(file_timestamp)
    file_path = os.path.join("logs", file_name)

    timestamp = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
    message = str(message.encode("utf-8"))[2:-1]
    text = "[{}] ({}): {}\n".format(severity, timestamp, message)

    with open(file_path, "a") as f:
        f.write(text)


def log_info(message):
    """
    Log an info with the given message to a log file.
    """

    log(INFO, message)


def log_warning(message):
    """
    Log a warning with the given message to a log file.
    """

    log(WARNING, message)


def log_error(message):
    """
    Log an error with the given message to a log file.
    """

    log(ERROR, message)

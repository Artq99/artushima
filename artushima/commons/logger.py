import os
import time
import datetime


INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

_LOG_DIR = "logs"
_ENCODING = "utf-8"

_FILE_TIMESTAMP_PATTERN = "%Y_%m_%d"
_FILE_NAME_PATTERN = "artushima_{}.log"
_TIMESTAMP_PATTERN = "%Y-%m-%d %H:%M:%S"
_LOG_PATTERN = "[{}] ({}): {}\n"


def log(severity, message):
    """
    Logs the message to a log file with the given severity.
    """

    t = time.time()
    file_timestamp = datetime.datetime.fromtimestamp(t).strftime(_FILE_TIMESTAMP_PATTERN)
    file_name = _FILE_NAME_PATTERN.format(file_timestamp)
    file_path = os.path.join(_LOG_DIR, file_name)
    timestamp = datetime.datetime.fromtimestamp(t).strftime(_TIMESTAMP_PATTERN)

    message = str(message.encode(_ENCODING))[2:-1]
    text = _LOG_PATTERN.format(severity, timestamp, message)

    with open(file_path, "a") as f:
        f.write(text)


def log_info(message):
    """
    Logs an info with the given message to a log file.
    """

    log(INFO, message)


def log_warning(message):
    """
    Logs a warning with the given message to a log file.
    """

    log(WARNING, message)


def log_error(message):
    """
    Logs an error with the given message to a log file.
    """

    log(ERROR, message)

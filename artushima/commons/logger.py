import os
import time
import datetime

INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"


def log(severity, message):
    """
    Logs the message to a log file with the given severity.
    """

    t = time.time()
    file_timestamp = datetime.datetime.fromtimestamp(t).strftime("%Y_%m_%d")
    file_name = "artushima_%s.log" % file_timestamp
    file_path = os.path.join("logs", file_name)
    timestamp = datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")

    message = str(message.encode("utf-8"))[2:-1]
    text = "[%s] (%s): %s\n" % (severity, timestamp, message)

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

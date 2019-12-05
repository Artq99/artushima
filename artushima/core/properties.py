"""
The module containing methods that deal with the properties loaded from the .env file.
"""

import os

import dotenv

from artushima.commons import logger


ENV_FILE_NAME = "artushima.env"

PROPERTY_APP_SECRET_KEY = "APP_SECRET_KEY"
PROPERTY_APP_HOST = "APP_HOST"
PROPERTY_APP_PORT = "APP_PORT"
PROPERTY_DB_URI = "DB_URI"
PROPERTY_TOKEN_EXPIRATION_TIME = "TOKEN_EXPIRATION_TIME"
PROPERTY_SUPERUSER_PASSWORD = "SUPERUSER_PASSWORD"
PROPERTY_TEST_BEARER_ENABLED = "TEST_BEARER_ENABLED"


def init():
    """
    Load properties from .env file.
    """

    dir_name = os.path.dirname(__name__)
    env_path = os.path.join(dir_name, ENV_FILE_NAME)

    if not os.path.exists(env_path):
        raise RuntimeError("The .env file not found!")

    dotenv.load_dotenv(env_path)

    logger.log_info("Properties initialized.")


def get(property_name):
    """
    Get the application property of the given name.
    """

    property_value = os.getenv(property_name)

    if property_value is None:
        logger.log_warning("Property '{}' not found.".format(property_name))

    return property_value


def get_app_secret_key():
    """
    Get the secret key for the app.

    The secret key is used to encrypt various data throughout the application.
    """

    return get(PROPERTY_APP_SECRET_KEY)


def get_app_host():
    """
    Get the host name on which the application will run.
    """

    return get(PROPERTY_APP_HOST)


def get_app_port():
    """
    Get the port on which the application will run.
    """

    return get(PROPERTY_APP_PORT)


def get_db_uri():
    """
    Get the URI of the database file.
    """

    return get(PROPERTY_DB_URI)


def get_token_expiration_time():
    """
    Get the time, after which the authentication token granted to a user on login will expire.
    """

    return get(PROPERTY_TOKEN_EXPIRATION_TIME)


def get_superuser_password():
    """
    Get the password, that should be given to an autocreated superuser.
    """

    return get(PROPERTY_SUPERUSER_PASSWORD)


def get_test_bearer_enabled():
    """
    Get the property that tells, if the test bearer token should be authenticated.
    """

    return get(PROPERTY_TEST_BEARER_ENABLED).lower() in ["true", "1"]

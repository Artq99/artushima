"""
The factory module for the application object.
"""

import flask

from artushima.commons import logger
from artushima.core import db_access, properties
from artushima.startup import startup_service
from artushima.web_api import auth_endpoint


class App:
    """
    A wrapper class for the flask application object.

    It sets up all settings on initialization and is ready to run via the 'run' method.
    """

    def __init__(self):

        self.flask_app = flask.Flask(__name__)

        properties.init()

        self.host = properties.get_app_host()
        self.port = properties.get_app_port()

        db_access.init()

        # Registering web-service endpoints
        self.flask_app.register_blueprint(auth_endpoint.AUTH_BLUEPRINT)

        session = db_access.Session()
        try:
            if not startup_service.superuser_exists():
                startup_service.create_superuser()
                session.commit()
        except Exception as err:
            session.rollback()
            logger.log_error("Error on application startup: {}".format(str(err)))
            raise err
        finally:
            session.close()

        logger.log_info("Application initialized.")

    def run(self):
        """
        Run the application.
        """

        self.flask_app.run(self.host, self.port)


def create():
    """
    Create and return the application object.
    """

    return App()


def create_and_run():
    """
    Create the application object and run it immediately.
    """

    app = App()
    app.run()

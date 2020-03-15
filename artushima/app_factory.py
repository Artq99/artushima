"""
The factory module for the application object.
"""

import flask

import artushima.auth.persistence.model as auth_model
import artushima.campaign.persistence.model as campaign_model
import artushima.user.persistence.model as user_model
from artushima.commons import logger
from artushima.core import db_access, properties
from artushima.startup import startup_service
from artushima.user import roles, user_roles_service
from artushima.views import index_view
from artushima.web_api import auth_endpoint, users_endpoint, my_campaigns_endpoint


class App:
    """
    A wrapper class for the flask application object.

    It sets up all settings on initialization and is ready to run via the 'run' method.
    """

    def __init__(self):

        # Making sure that all the entities has been imported (i.e. initialized)
        assert auth_model is not None
        assert user_model is not None
        assert campaign_model is not None

        self.flask_app = flask.Flask(__name__)

        properties.init()

        self.host = properties.get_app_host()
        self.port = properties.get_app_port()

        db_access.init()

        # Registering web-service endpoints
        self.flask_app.register_blueprint(auth_endpoint.AUTH_BLUEPRINT)
        self.flask_app.register_blueprint(users_endpoint.USERS_BLUEPRINT)
        self.flask_app.register_blueprint(my_campaigns_endpoint.MY_CAMPAIGNS_BLUEPRINT)

        # Registering views
        self.flask_app.register_blueprint(index_view.INDEX_BLUEPRINT)

        session = db_access.Session()
        try:
            if not startup_service.superuser_exists():
                startup_service.create_superuser()
            else:
                superuser_roles = user_roles_service.get_user_roles("superuser")

                grant_required = False
                for role in roles.ALL_ROLES:
                    if role not in superuser_roles:
                        grant_required = True
                        break

                if grant_required:
                    user_roles_service.grant_roles("SYSTEM", "superuser", roles.ALL_ROLES)

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


def create_for_debug():
    """
    Create and return the inner flask app for debug.
    """

    app = App()
    return app.flask_app


def create_and_run():
    """
    Create the application object and run it immediately.
    """

    app = App()
    app.run()

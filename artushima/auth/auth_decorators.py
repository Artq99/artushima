"""
The module contains the decorators that can be used to control access to a particular resource.
"""

import functools

import flask

from artushima.auth import auth_service
from artushima.commons import logger
from artushima.core import db_access


def allow_authorized(func):
    """
    Allow access only to authorized users.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        token = flask.request.headers.get("Authorization")

        db_session = db_access.Session()

        try:
            if not auth_service.is_token_ok(token):

                return flask.jsonify({
                    "status": "failure",
                    "message": "Błąd autoryzacji"
                }), 401

        except Exception as err:
            logger.log_error(str(err))
            db_session.rollback()

            return flask.jsonify({
                "status": "failure",
                "message": "Błąd aplikacji"
            }), 500

        finally:
            db_session.close()

        return func(*args, **kwargs)

    return wrapper


def allow_authorized_with_roles(roles):
    """
    Allow access only to authorized users that have one of the given roles.
    """

    def wrap_func(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            token = flask.request.headers.get("Authorization")

            db_session = db_access.Session()

            try:
                if not auth_service.is_token_ok(token):

                    return flask.jsonify({
                        "status": "failure",
                        "message": "Błąd autoryzacji"
                    }), 401

                if not auth_service.are_roles_sufficient(token, roles):

                    return flask.jsonify({
                        "status": "failure",
                        "message": "Brak uprawnień"
                    }), 403

            except Exception as err:
                logger.log_error(str(err))
                db_session.rollback()

                return flask.jsonify({
                    "status": "failure",
                    "message": "Błąd aplikacji"
                }), 500

            finally:
                db_session.close()

            return func(*args, **kwargs)

        return wrapper

    return wrap_func

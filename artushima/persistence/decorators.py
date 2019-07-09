"""
The module providing decorators related to the persistence process.
"""

import functools

from artushima.persistence import pu


def transactional_service_method(func):
    """
    Decorator that manages the DB transaction shared throughout the whole service method execution.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if pu.current_session is not None:
            pu.current_session.close()

        pu.current_session = pu.Session()

        try:
            response = func(*args, **kwargs)

            if response["status"] == "success":
                pu.current_session.commit()
            else:
                pu.current_session.rollback()

            return response
        except Exception as e:
            pu.current_session.rollback()
            raise e
        finally:
            pu.current_session.close()
            pu.current_session = None

    return wrapper

"""
The module providing functionalities necessary to access the database.
"""

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from artushima.core import properties

SqlEngine = None
Session = None
BaseEntity = declarative.declarative_base()


def init():
    """
    Initialize the SQL engine.
    """

    global SqlEngine, Session

    db_uri = properties.get_db_uri()

    if not db_uri:
        raise RuntimeError("Property 'DB_URI' not provided.")

    SqlEngine = sqlalchemy.create_engine(db_uri)
    Session = orm.scoped_session(orm.sessionmaker(SqlEngine))

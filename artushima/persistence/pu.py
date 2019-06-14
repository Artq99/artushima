"""
The persistence unit module of the application.
"""

import sqlalchemy
from sqlalchemy import orm

from artushima.commons import properties
from artushima.commons import exceptions


# The class for the SQL engine.
# Not initialised by default.
SqlEngine = None

# The class for the SQL session.
# Not initialised by default.
Session = None


@sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "connect")
def __on_connect(dbapi_connection, connection_record):
    """
    The event turning on the foreign key constraints on the sqlite database instance.
    """

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def init_engine(testing=False):
    """
    Initialise the SQL engine.

    Arguments:
        - testing - if True, an instance of an in-memory sqlite database is created instead of connecting to
                    the file based one.
    """

    global SqlEngine, Session

    if testing:
        SqlEngine = sqlalchemy.create_engine("sqlite:///:memory:")
    else:
        db_file_name = properties.get_db_uri()

        if db_file_name is None:
            raise exceptions.PersistenceError(
                "The property 'DB_URI' not present. Cannot initialise the database.", __name__, init_engine.__name__
            )

        SqlEngine = sqlalchemy.create_engine("sqlite:///" + db_file_name)

    Session = orm.sessionmaker(SqlEngine)


# The object representing the currently used session.
# Not initalised by default
current_session = None

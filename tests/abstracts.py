"""
The module containing abstract base classes for all tests.
"""

import unittest
from unittest import mock

from sqlalchemy import orm

from artushima.commons import logger
from artushima.commons.logger import log as log_default  # backup
from artushima.persistence import pu
from artushima.persistence import model


class AbstractTestClass(unittest.TestCase):
    """
    The base class for all tests.

    It replaces the default log method from the logger module with a mock.
    """

    def setUp(self):
        super().setUp()

        self.log_mock = mock.create_autospec(logger.log)
        logger.log = self.log_mock

    def tearDown(self):
        super().tearDown()

        logger.log = log_default


class AbstractPersistenceTestClass(AbstractTestClass):
    """
    The base class for all persistence tests.

    It initialises the database engine, creates the test session and initialises an another session for the test cases.
    """

    def setUp(self):
        super().setUp()

        pu.init_engine(testing=True)
        model.Base.metadata.create_all(pu.SqlEngine)

        # the session used for creating test data
        self.session = pu.Session()

        pu.current_session = pu.Session()

    def tearDown(self):
        super().tearDown()

        self.session.commit()
        self.session.close()
        self.session = None

        model.Base.metadata.drop_all(pu.SqlEngine)

        if pu.current_session is not None:
            pu.current_session.close()
            pu.current_session = None


class AbstractServiceTestClass(AbstractTestClass):
    """
    The base class for all service tests.

    It mocks the SQL session from the persistence unit, assuring that no data is read from or written to the database.
    """

    def setUp(self):
        super().setUp()

        self.current_session_mock = mock.create_autospec(orm.Session)
        pu.current_session = self.current_session_mock

    def tearDown(self):
        super().tearDown()

        pu.current_session = None

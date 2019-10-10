"""
The test module for the persistence decorators.
"""

from tests import abstracts
from tests import test_data_creator

from artushima.persistence import pu
from artushima.persistence import model
from artushima.persistence.decorators import transactional_service_method
from artushima.services import service_utils


class TransactionalServiceMethodTest(abstracts.AbstractPersistenceTestClass):
    """
    Tests for the decorator transactional_service_method.
    """

    def test_single_transaction(self):
        """
        The test checks if only one single session is used in both repository methods called by the service method,
        decorated with the transactional_service_method decorator.
        """

        # given

        def repository_method_1():
            user = test_data_creator.create_test_user(1, "test_user_1")
            pu.current_session.add(user)
            return str(pu.current_session)

        def repository_method_2():
            user = test_data_creator.create_test_user(2, "test_user_2")
            pu.current_session.add(user)
            return str(pu.current_session)

        @transactional_service_method
        def service_method():
            session1 = repository_method_1()
            session2 = repository_method_2()

            return service_utils.create_response_success(session1=session1, session2=session2)

        # when
        response = service_method()

        # then
        self.assertIsNone(pu.current_session)
        self.assertIsNotNone(response)
        self.assertEqual(response["session1"], response["session2"])
        users = self.session.query(model.UserEntity).all()
        self.assertEqual(2, len(users))

    def test_rollback_on_failure(self):
        """
        The test checks if the transaction is rolled back when the service method returns a failure.
        """

        # given

        def repository_method_1():
            user = test_data_creator.create_test_user(1, "test_user_1")
            pu.current_session.add(user)
            return str(pu.current_session)

        def repository_method_2():
            user = test_data_creator.create_test_user(2, "test_user_2")
            pu.current_session.add(user)
            return str(pu.current_session)

        @transactional_service_method
        def service_method():
            session1 = repository_method_1()
            session2 = repository_method_2()

            return service_utils.create_response_failure(session1=session1, session2=session2)

        # when
        response = service_method()

        # then
        self.assertIsNone(pu.current_session)
        self.assertIsNotNone(response)
        self.assertEqual(response["session1"], response["session2"])
        users = self.session.query(model.UserEntity).all()
        self.assertEqual(0, len(users))

    def test_rollback_on_error(self):
        """
        The test checks if the transaction is rolled back, when an error occures.
        """

        # given

        def repository_method_1():
            user = test_data_creator.create_test_user(1, "test_user_1")
            pu.current_session.add(user)
            return str(pu.current_session)

        def repository_method_2():
            user = test_data_creator.create_test_user(2, "test_user_2")
            pu.current_session.add(user)
            return str(pu.current_session)

        @transactional_service_method
        def service_method():
            repository_method_1()
            repository_method_2()

            raise RuntimeError()

        # when then
        with self.assertRaises(RuntimeError):
            service_method()
        self.assertIsNone(pu.current_session)
        users = self.session.query(model.UserEntity).all()
        self.assertEqual(0, len(users))

    def test_old_session_rollback(self):
        """
        The test checks if the session that existed in the moment of the service method call is rolled back, closed,
        and a new session is initialised.

        Sessions in the persistence unit should be started only by this decorator and closed after the execution, thus,
        the situation when a session exists before the decorated method call is pathological.
        """

        # given
        user_1 = test_data_creator.create_test_user(1, "test_user_1")
        pu.current_session.add(user_1)
        pu.current_session.flush()

        session_1 = str(pu.current_session)

        def repository_method():
            user_2 = test_data_creator.create_test_user(2, "test_user_2")
            pu.current_session.add(user_2)
            pu.current_session.flush()
            return str(pu.current_session)

        @transactional_service_method
        def service_method():
            session_2 = repository_method()

            return service_utils.create_response_success(session_2=session_2)

        # when
        response = service_method()

        # then
        self.assertIsNone(pu.current_session)
        self.assertIsNotNone(session_1)
        self.assertIsNotNone(response["session_2"])
        self.assertNotEqual(session_1, response["session_2"])

        self.assertIsNone(self.session.query(model.UserEntity).filter_by(id=1).first())
        self.assertIsNotNone(self.session.query(model.UserEntity).filter_by(id=2).first())

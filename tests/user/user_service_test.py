"""
The testing module for the user service.
"""

from datetime import datetime
from unittest import TestCase
from unittest.mock import create_autospec

from werkzeug import security

from artushima.core.exceptions import BusinessError
from artushima.user import user_service
from artushima.user.persistence import user_repository
from artushima.user.persistence.model import UserEntity


class GetUserByIdTest(TestCase):

    def setUp(self):
        self.user_repository_mock = create_autospec(user_repository)
        user_service.user_repository = self.user_repository_mock

    def tearDown(self):
        user_service.user_repository = user_repository

    def test_should_get_user_by_id(self):
        # given
        user = UserEntity()
        user.id = 1
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0
        user.password_hash = "test_hash"

        self.user_repository_mock.read_by_id.return_value = user

        # when
        user_data = user_service.get_user_by_id(1)

        # then
        self.assertIsNotNone(user_data)
        self.assertIsInstance(user_data, dict)
        self.assertEqual(user.id, user_data["id"])
        self.assertEqual(user.user_name, user_data["user_name"])
        self.assertEqual(user.created_on, user_data["created_on"])
        self.assertEqual(user.modified_on, user_data["modified_on"])
        self.assertEqual(user.opt_lock, user_data["opt_lock"])
        self.assertEqual(user.password_hash, user_data["password_hash"])

        self.user_repository_mock.read_by_id.assert_called_once_with(1)

    def test_should_get_none_when_user_does_not_exist(self):
        # given
        self.user_repository_mock.read_by_id.return_value = None

        # when
        user_data = user_service.get_user_by_id(1)

        # then
        self.assertIsNone(user_data)

    def test_should_get_business_error_when_user_id_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.get_user_by_id(None)

    def test_should_get_value_error_when_user_id_is_not_str(self):
        # when then
        with self.assertRaises(ValueError):
            user_service.get_user_by_id("1")


class GetUserByUserNameTest(TestCase):

    def setUp(self):
        self.user_repository_mock = create_autospec(user_repository)
        user_service.user_repository = self.user_repository_mock

    def tearDown(self):
        user_service.user_repository = user_repository

    def test_should_get_user_by_user_name(self):
        # given
        user = UserEntity()
        user.id = 1
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0
        user.password_hash = "test_hash"

        self.user_repository_mock.read_by_user_name.return_value = user

        # when
        user_data = user_service.get_user_by_user_name("test_user")

        # then
        self.assertIsNotNone(user_data)
        self.assertIsInstance(user_data, dict)
        self.assertEqual(user.id, user_data["id"])
        self.assertEqual(user.user_name, user_data["user_name"])
        self.assertEqual(user.created_on, user_data["created_on"])
        self.assertEqual(user.modified_on, user_data["modified_on"])
        self.assertEqual(user.opt_lock, user_data["opt_lock"])
        self.assertEqual(user.password_hash, user_data["password_hash"])

        self.user_repository_mock.read_by_user_name.assert_called_once_with("test_user")

    def test_should_get_none_when_user_does_not_exist(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None

        # when
        user_data = user_service.get_user_by_user_name("test_user")

        # then
        self.assertIsNone(user_data)

    def test_should_raise_value_error_when_user_name_is_not_string(self):
        # when then
        with self.assertRaises(ValueError):
            user_service.get_user_by_user_name(1)

    def test_should_raise_business_error_when_user_name_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.get_user_by_user_name(None)

    def test_should_raise_business_error_when_user_name_is_empty_string(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.get_user_by_user_name("")


class GetAllUsersTest(TestCase):

    def setUp(self):
        self.user_repository_mock = create_autospec(user_repository)
        user_service.user_repository = self.user_repository_mock

    def tearDown(self):
        user_service.user_repository = user_repository

    def test_should_get_all_users(self):
        # given
        user_1 = UserEntity()
        user_1.user_name = "test_user_1"
        user_1.created_on = datetime.utcnow()
        user_1.modified_on = datetime.utcnow()
        user_1.opt_lock = 0

        user_2 = UserEntity()
        user_2.user_name = "test_user_2"
        user_2.created_on = datetime.utcnow()
        user_2.modified_on = datetime.utcnow()
        user_2.opt_lock = 0

        self.user_repository_mock.read_all.return_value = [user_1, user_2]

        # when
        found_users = user_service.get_all_users()

        # then
        self.assertIsNotNone(found_users)
        self.assertEqual(2, len(found_users))
        self.assertEqual("test_user_1", found_users[0]["user_name"])
        self.assertEqual("test_user_2", found_users[1]["user_name"])


class CreateUserTest(TestCase):

    def setUp(self):
        self.user_repository_mock = create_autospec(user_repository)
        self.security_mock = create_autospec(security)
        user_service.user_repository = self.user_repository_mock
        user_service.security = self.security_mock

    def tearDown(self):
        user_service.user_repository = user_repository
        user_service.security = security

    def test_should_create_new_user(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None
        self.security_mock.generate_password_hash.return_value = "test_hash"

        # when
        user_service.create_user("test_editor", "test_user", "test_password")

        # then
        self.user_repository_mock.persist.assert_called_once()

        user = self.user_repository_mock.persist.call_args[0][0]
        self.assertIsInstance(user, UserEntity)
        self.assertEqual("test_user", user.user_name)
        self.assertEqual("test_hash", user.password_hash)

        self.assertEqual(1, len(user.user_history_entries))
        history_entry = user.user_history_entries[0]
        self.assertEqual("test_editor", history_entry.editor_name)
        self.assertEqual("Użytkownik test_user został utworzony.", history_entry.message)

    def test_should_create_new_user_with_roles(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None
        self.security_mock.generate_password_hash.return_value = "test_hash"

        # when
        user_service.create_user("test_editor", "test_user", "test_password", ["role_1", "role_2"])

        # then
        self.user_repository_mock.persist.assert_called_once()

        user = self.user_repository_mock.persist.call_args[0][0]
        self.assertEqual(2, len(user.user_roles))
        self.assertEqual("role_1", user.user_roles[0].role_name)
        self.assertEqual("role_2", user.user_roles[1].role_name)

    def test_should_raise_exception_when_editor_name_is_not_str(self):
        # when then
        with self.assertRaises(ValueError):
            user_service.create_user(1, "test_user", "test_password")

    def test_should_raise_exception_when_editor_name_is_empty(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.create_user("", "test_user", "test_password")

    def test_should_raise_exception_when_editor_name_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.create_user(None, "test_user", "test_password")

    def test_should_raise_exception_when_user_name_is_not_str(self):
        # when then
        with self.assertRaises(ValueError):
            user_service.create_user("test_editor", 1, "test_password")

    def test_should_raise_exception_when_user_name_is_empty(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.create_user("test_editor", "", "test_password")

    def test_should_raise_exception_when_user_name_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_service.create_user("test_editor", None, "test_password")

    def test_should_raise_error_when_password_is_not_str(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None

        # when then
        with self.assertRaises(ValueError):
            user_service.create_user("test_editor", "test_user", 1)

    def test_should_raise_error_when_password_is_none(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None

        # when then
        with self.assertRaises(BusinessError):
            user_service.create_user("test_editor", "test_user", None)

    def test_should_raise_error_when_password_is_empty_str(self):
        # given
        self.user_repository_mock.read_by_user_name = None

        # when then
        with self.assertRaises(BusinessError):
            user_service.create_user("test_editor", "test_user", "")

    def test_should_raise_exception_when_roles_arg_is_not_list(self):
        # when then
        with self.assertRaises(ValueError):
            user_service.create_user("test_editor", "test_user", "test_password", 1)

    def test_should_raise_error_when_user_already_exists(self):
        # given
        user = UserEntity()
        user.id = 1
        user.user_name = "test_user"

        self.user_repository_mock.read_by_user_name.return_value = user

        with self.assertRaises(BusinessError):
            user_service.create_user("test_editor", "test_user", "test_password")

"""
The testing module for the user roles service.
"""

from datetime import datetime
from unittest import TestCase
from unittest.mock import create_autospec

from artushima.core.exceptions import BusinessError
from artushima.user import user_roles_service
from artushima.user.persistence import user_repository
from artushima.user.persistence.model import UserEntity, UserRoleEntity


class GetUserRolesTest(TestCase):

    def setUp(self):
        self.user_repository_mock = create_autospec(user_repository)
        user_roles_service.user_repository = self.user_repository_mock

    def tearDown(sefl):
        user_roles_service.user_repository = user_repository

    def test_should_get_all_user_roles(self):
        # given
        user = UserEntity()
        user.id = 1
        user.user_name = "test_user"

        role_1 = UserRoleEntity()
        role_1.id = 1
        role_1.role_name = "test_role_1"
        role_1.user = user

        role_2 = UserRoleEntity()
        role_2.id = 2
        role_2.role_name = "test_role_2"
        role_2.user = user

        self.user_repository_mock.read_by_user_name.return_value = user

        # when
        found_roles = user_roles_service.get_user_roles("test_user")

        # then
        self.assertIsNotNone(found_roles)
        self.assertEqual(2, len(found_roles))
        self.assertIn("test_role_1", found_roles)
        self.assertIn("test_role_2", found_roles)

    def test_should_raise_exception_when_user_does_not_exist(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None

        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.get_user_roles("test_user")

    def test_should_raise_exception_when_user_name_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.get_user_roles(None)

    def test_should_raise_exception_when_user_name_is_empty_str(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.get_user_roles("")

    def test_should_raise_exception_when_user_name_is_not_str(self):
        # when then
        with self.assertRaises(ValueError):
            user_roles_service.get_user_roles(1)


class GrantRolesTest(TestCase):

    def setUp(self):
        self.user_repository_mock = create_autospec(user_repository)
        user_roles_service.user_repository = self.user_repository_mock

    def tearDown(self):
        user_roles_service.user_repository = user_repository

    def test_should_raise_exception_when_editor_name_is_not_str(self):
        # when then
        with self.assertRaises(ValueError):
            user_roles_service.grant_roles(1, "test_user", ["test_role_1"])

    def test_should_raise_exception_when_editor_name_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.grant_roles(None, "test_user", ["test_role_1"])

    def test_should_raise_exception_when_editor_name_is_empty(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.grant_roles("", "test_user", ["test_role_1"])

    def test_should_raise_exception_when_user_name_is_not_str(self):
        # when then
        with self.assertRaises(ValueError):
            user_roles_service.grant_roles("test_editor", 1, ["test_role_1"])

    def test_should_raise_exception_when_user_name_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.grant_roles("test_editor", None, ["test_role_1"])

    def test_should_raise_exception_when_user_name_is_empty(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.grant_roles("test_editor", "", ["test_role_1"])

    def test_should_raise_exception_when_roles_arg_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.grant_roles("test_editor", "test_user", None)

    def test_should_raise_exception_when_roles_arg_is_not_list(self):
        # when then
        with self.assertRaises(ValueError):
            user_roles_service.grant_roles("test_editor", "test_user", 1)

    def test_should_raise_exception_when_user_does_not_exist(self):
        # given
        self.user_repository_mock.read_by_user_name.return_value = None

        # when then
        with self.assertRaises(BusinessError):
            user_roles_service.grant_roles("test_editor", "test_user", ["test_role_1"])

    def test_should_grant_new_roles_to_user(self):
        # given
        test_user = UserEntity()
        test_user.user_name = "test_user"

        self.user_repository_mock.read_by_user_name.return_value = test_user

        # when
        user_roles_service.grant_roles("test_editor", "test_user", ["test_role_1", "test_role_2"])

        # then
        self.user_repository_mock.persist.assert_called_once_with(test_user)
        self.assertEqual(2, len(test_user.user_roles))
        self.assertEqual("test_role_1", test_user.user_roles[0].role_name)
        self.assertEqual("test_role_2", test_user.user_roles[1].role_name)

    def test_should_not_modify_old_role_when_granting_new_one(self):
        # given
        test_user = UserEntity()
        test_user.user_name = "test_user"

        old_role = UserRoleEntity()
        old_role.role_name = "old_role"
        old_role.created_on = datetime(2010, 1, 1)
        old_role.user = test_user

        self.user_repository_mock.read_by_user_name.return_value = test_user

        # when
        user_roles_service.grant_roles("test_editor", "test_user", ["old_role", "new_role"])

        # then
        self.assertEqual(2, len(test_user.user_roles))
        self.assertEqual("old_role", test_user.user_roles[0].role_name)
        self.assertEqual(datetime(2010, 1, 1), test_user.user_roles[0].created_on)

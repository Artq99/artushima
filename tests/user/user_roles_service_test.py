"""
The testing module for the user roles service.
"""

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

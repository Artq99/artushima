"""
The test module for the error_handler module.
"""

from tests import abstracts
from tests import test_utils

from artushima import messages
from artushima.commons import error_handler


class HandleTest(abstracts.AbstractTestClass):
    """
    Tests for the method error_handler.handle.
    """

    def test_persistence_error(self):
        """
        The test checks if the method returns a correct error message for an instance of the PersistenceError.
        """

        # given
        error = test_utils.create_persistence_error()

        # when
        message = error_handler.handle(error)

        # then
        self.assertEqual(messages.PERSISTENCE_ERROR, message)

    def test_token_expiration_error(self):
        """
        The test checks if the method returns a correct error message for an instance of the TokenExpirationError.
        """

        # given
        error = test_utils.create_token_expiration_error()

        # when
        message = error_handler.handle(error)

        # then
        self.assertEqual(messages.TOKEN_EXPIRED, message)

    def test_token_invalid_error(self):
        """
        The test checks if the method returns a correct error message for an instance of the TokenInvalidError.
        """

        # given
        error = test_utils.create_token_invalid_error()

        # when
        message = error_handler.handle(error)

        # then
        self.assertEqual(messages.AUTHENTICATION_FAILED, message)

    def test_missing_input_data_error_known_argument(self):
        """
        The test checks if the method returns a correct error message including a translated argument name for
        an instance of the MissingInputDataError.
        """

        # given
        arg_name = "user_name"
        error = test_utils.create_missing_input_data_error(arg_name)

        # when
        message = error_handler.handle(error)

        # then
        self.assertEqual(messages.INPUT_DATA_MISSING.format(messages.ARG_NAMES[arg_name]), message)

    def test_missing_input_data_error_unknown_argument(self):
        """
        The test checks if the method returns a correct error message including an argument name for an instance of
        the MissingInputDataError.
        """

        # given
        arg_name = "unknown_arg"
        error = test_utils.create_missing_input_data_error(arg_name)

        # when
        message = error_handler.handle(error)

        # then
        self.assertEqual(messages.INPUT_DATA_MISSING.format(arg_name), message)

    def test_business_error(self):
        """
        The test checks if the method returns a correct error message for an instance of the BusinessError.
        """

        # given
        error = test_utils.create_business_error()

        # when
        message = error_handler.handle(error)

        # then
        self.assertEqual(messages.APPLICATION_ERROR, message)

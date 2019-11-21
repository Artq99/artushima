from tests.abstracts import AbstractIntegrativeTestClass

from artushima.constants import RESPONSE_STATUS_SUCCESS
from artushima.commons import properties


class LogInTest(AbstractIntegrativeTestClass):

    def test_should_log_in_superuser(self):
        # given
        request_body = {
            "userName": "superuser",
            "password": properties.get_superuser_password()
        }

        # when
        response = self.client.post("/api/auth/login", json=request_body)

        # then
        self.assertEqual(RESPONSE_STATUS_SUCCESS, response.json["status"])
        self.assertEqual("superuser", response.json["currentUser"]["userName"])
        self.assertTrue(len(response.json["currentUser"]["token"]) > 0)

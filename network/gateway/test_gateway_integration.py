import os
import sys
import unittest
from unittest.mock import patch


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)


from app import app
from auth import create_token


class GatewayIntegrationTests(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
        )

        self.client = app.test_client()

    @staticmethod
    def authorization_header(username, role="Officer"):

        token = create_token(
            username=username,
            role=role,
        )

        return {
            "Authorization": f"Bearer {token}"
        }

    def test_gateway_health_endpoint(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["project"],
            "Zero Trust Cruise Platform",
        )

        self.assertEqual(
            data["gateway"],
            "ONLINE",
        )

    def test_missing_authorization_header_returns_401(self):

        response = self.client.get("/bridge")

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "Authorization header missing",
        )

    def test_invalid_token_returns_401(self):

        response = self.client.get(
            "/bridge",
            headers={
                "Authorization": "Bearer invalid-token"
            },
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "Invalid or expired token",
        )

    @patch("routes.is_identity_blocked")
    @patch("routes.evaluate_policy")
    def test_blocked_identity_returns_403_before_opa(
        self,
        mock_evaluate_policy,
        mock_is_identity_blocked,
    ):

        mock_is_identity_blocked.return_value = True

        response = self.client.get(
            "/bridge",
            headers=self.authorization_header(
                "intruder.user"
            ),
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.get_json()["reason"],
            "Identity blocked by automated incident response",
        )

        mock_evaluate_policy.assert_not_called()

    @patch("routes.forward_request")
    @patch("routes.is_identity_blocked")
    @patch("routes.evaluate_policy")
    def test_allowed_identity_reaches_backend(
        self,
        mock_evaluate_policy,
        mock_is_identity_blocked,
        mock_forward_request,
    ):

        mock_is_identity_blocked.return_value = False
        mock_evaluate_policy.return_value = True

        mock_forward_request.return_value = (
            {
                "service": "bridge",
                "status": "ONLINE",
            },
            200,
        )

        response = self.client.get(
            "/bridge",
            headers=self.authorization_header(
                "captain"
            ),
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.get_json()["user"],
            "captain",
        )

        mock_evaluate_policy.assert_called_once()

        mock_forward_request.assert_called_once_with(
            "bridge"
        )

    @patch("routes.forward_request")
    @patch("routes.is_identity_blocked")
    @patch("routes.evaluate_policy")
    def test_opa_denial_returns_403_and_backend_not_called(
        self,
        mock_evaluate_policy,
        mock_is_identity_blocked,
        mock_forward_request,
    ):

        mock_is_identity_blocked.return_value = False
        mock_evaluate_policy.return_value = False

        response = self.client.get(
            "/bridge",
            headers=self.authorization_header(
                "captain"
            ),
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.get_json()["error"],
            "Access denied by OPA",
        )

        mock_forward_request.assert_not_called()

    @patch("routes.is_identity_blocked")
    @patch("routes.evaluate_policy")
    def test_opa_exception_returns_503(
        self,
        mock_evaluate_policy,
        mock_is_identity_blocked,
    ):

        mock_is_identity_blocked.return_value = False

        mock_evaluate_policy.side_effect = RuntimeError(
            "OPA unavailable"
        )

        response = self.client.get(
            "/bridge",
            headers=self.authorization_header(
                "captain"
            ),
        )

        self.assertEqual(response.status_code, 503)

        self.assertEqual(
            response.get_json()["error"],
            "Authorization service unavailable",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
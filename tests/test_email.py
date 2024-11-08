import unittest
from unittest.mock import MagicMock, patch

from saas.saas_secrets import secrets
from saas.rxext.utils.email_util import ResendAPIEmailSender, ResendSDKEmailSender


class TestEmailUtil(unittest.TestCase):
    def setUp(self):
        self.email_from = secrets.email_from
        self.email_to = secrets.email_to
        self.subject = "Test Email"
        self.html_content = "<p>This is a test email.</p>"

    @unittest.skip("Skip this test unless you want to send a real email.")
    def test_reset_sdk_real(self):
        sender = ResendSDKEmailSender()
        result = sender.send_email(
            self.email_from, self.email_to, self.subject, self.html_content
        )
        self.assertTrue("id" in result and result["id"] is not None)

    @patch("saas.utils.email_util.resend.Emails.send")
    def test_resend_sdk_email_sender(self, mock_send):
        mock_response = MagicMock()
        mock_response.id = "email_123"
        mock_send.return_value = mock_response

        sender = ResendSDKEmailSender()
        result = sender.send_email(
            self.email_from, self.email_to, self.subject, self.html_content
        )

        mock_send.assert_called_once_with(
            {
                "from": self.email_from,
                "to": [self.email_to],
                "subject": self.subject,
                "html": self.html_content,
            }
        )
        self.assertEqual(result.id, "email_123")

    @patch("saas.utils.email_util.requests.post")
    def test_resend_api_email_sender(self, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"id": "email_456"}
        mock_post.return_value = mock_response

        sender = ResendAPIEmailSender()
        result = sender.send_email(
            self.email_from, self.email_to, self.subject, self.html_content
        )

        expected_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {secrets.resend_api_key}",
        }
        expected_payload = {
            "from": self.email_from,
            "to": [self.email_to],
            "subject": self.subject,
            "html": self.html_content,
        }

        mock_post.assert_called_once_with(
            "https://api.resend.com/emails",
            headers=expected_headers,
            json=expected_payload,
        )
        self.assertEqual(result, {"id": "email_456"})


if __name__ == "__main__":
    unittest.main()

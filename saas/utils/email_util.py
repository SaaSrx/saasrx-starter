import re

import requests
import resend
from supabase import Client, create_client

from saas.rxext import console
from saas.saas_secrets import secrets

resend_api_key = secrets.resend_api_key
resend.api_key = resend_api_key

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)
# ---- Generic Utils


def invalid_email(email_str: str) -> bool:
    """
    Checks if the provided email string is invalid.

    Args:
        email_str (str): The email address to validate.

    Returns:
        bool: True if the email address is invalid, False otherwise.
    """
    return not re.match(r"[^@]+@[^@]+\.[^@]+", email_str)


# ---- Sending Email Related
class EmailSender:
    def send_email(self, from_email: str, to_email: str, subject: str, html_content: str) -> dict:
        raise NotImplementedError("send_email method not implemented")


class ResendSDKEmailSender(EmailSender):
    resend.api_key = secrets.resend_api_key

    def send_email(self, from_email: str, to_email: str, subject: str, html_content: str) -> dict:
        params: resend.Emails.SendParams = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        email: resend.Email = resend.Emails.send(params)
        return email


class ResendAPIEmailSender(EmailSender):
    api_key = secrets.resend_api_key

    def send_email(self, from_email: str, to_email: str, subject: str, html_content: str) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {resend_api_key}",
        }

        payload = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }

        response = requests.post("https://api.resend.com/emails", headers=headers, json=payload)

        if response.ok:
            return response.json()
        else:
            response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful


# Example usage
def send_email_using_resend_sdk(from_email: str, to_email: str, subject: str, html_content: str) -> dict:
    sender = ResendSDKEmailSender()
    return sender.send_email(from_email, to_email, subject, html_content)


def send_email_using_resend_api(from_email: str, to_email: str, subject: str, html_content: str) -> dict:
    sender = ResendAPIEmailSender()
    return sender.send_email(from_email, to_email, subject, html_content)


def signin_with_otp(email: str):
    should_create_user = True
    redirect_to = "https://localhost/success"
    response = supabase.auth.sign_in_with_otp(
        {
            "email": "example@email.com",
            "options": {
                # set this to false if you do not want the user to be automatically signed up
                "should_create_user": should_create_user,
                "email_redirect_to": "https://example.com/welcome",
            },
        }
    )


def verify_otp(params: dict):
    console.log(f"verifying otp {params=}")
    response = supabase.auth.verify_otp(params)
    return response


# Uncomment to test
# if __name__ == '__main__':
#     try:
#         data = send_email_using_resend_sdk("onboarding@resend.dev", "delivered@resend.dev", "Hello World", "<strong>it works!</strong>")
#         print(json.dumps(data, indent=2))
#         data = send_email_using_resend_api("Acme <onboarding@resend.dev>", "delivered@resend.dev", "hello world", "<strong>it works!</strong>")
#         print(json.dumps(data, indent=2))
#     except requests.exceptions.HTTPError as err:
#         print(f"Error: {err}")

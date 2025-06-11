# pyright: reportMissingImports=false

import re
from functools import cache, partial

import requests
import resend
from supabase import Client, create_client

from rxext import console  # type: ignore[import-not-found]


# ---- Generic Utils


def invalid_email(email_str: str, pattern: str = r"[^@]+@[^@]+\.[^@]+") -> bool:
    """
    Checks if the provided email string is invalid.

    Args:
        email_str (str): The email address to validate.
        pattern (str): The regex pattern.  The default is a standard email pattern but can allow looser emails for various reasons

    Returns:
        bool: True if the email address is invalid, False otherwise.
    """
    return not re.match(pattern, email_str)


dev_invalid_email = partial(
    invalid_email, pattern=r"[^@]+@[^@]+"
)  # allow test/dev email


# ---- Sending Email Related
class EmailSender:
    def __init__(self, api_key: str, **kwargs):
        raise NotImplementedError(
            "EmailSender is an abstract class and cannot be instantiated"
        )

    def send_email(
        self, from_email: str, to_email: str, subject: str, html_content: str
    ) -> dict[str, str]:
        raise NotImplementedError("send_email method not implemented")


class ResendSDKEmailSender(EmailSender):
    def __init__(self, api_key: str):
        self.resend = resend
        self.resend.api_key = api_key

    def send_email(
        self, from_email: str, to_email: str, subject: str, html_content: str
    ) -> dict:
        params: resend.Emails.SendParams = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        email: resend.Email = self.resend.Emails.send(params)
        return email


class ResendAPIEmailSender(EmailSender):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        html_content: str,
    ) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }

        response = requests.post(
            "https://api.resend.com/emails", headers=headers, json=payload
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()


# Convenience wrappers


def send_email_using_resend_sdk(
    from_email: str,
    to_email: str,
    subject: str,
    html_content: str,
    api_key: str,
    **kwargs,
) -> dict:
    sender = ResendSDKEmailSender(api_key)
    return sender.send_email(from_email, to_email, subject, html_content)


def send_email_using_resend_api(
    from_email: str,
    to_email: str,
    subject: str,
    html_content: str,
    api_key: str,
    **kwargs,
) -> dict:
    sender = ResendAPIEmailSender(api_key)
    return sender.send_email(from_email, to_email, subject, html_content)


@cache
def _make_supabase_client(supabase_url: str, supabase_key: str) -> Client:
    return create_client(supabase_url, supabase_key)


def verify_otp(
    params: dict,
    supabase_client: Client | None = None,
    supabase_url: str | None = None,
    supabase_key: str | None = None,
):
    if not supabase_client:
        supabase_client = _make_supabase_client(supabase_url, supabase_key)
    console.log(f"verifying otp {params=}")
    return supabase_client.auth.verify_otp(params)

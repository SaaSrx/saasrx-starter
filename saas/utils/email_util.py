import requests
import resend

from saas.saas_config import secrets

resend_api_key = secrets.resend_api_key
resend.api_key = resend_api_key


class EmailSender:
    def send_email(
        self, from_email: str, to_email: str, subject: str, html_content: str
    ) -> dict:
        raise NotImplementedError("send_email method not implemented")


class ResendSDKEmailSender(EmailSender):
    resend.api_key = secrets.resend_api_key

    def send_email(
        self, from_email: str, to_email: str, subject: str, html_content: str
    ) -> dict:
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

    def send_email(
        self, from_email: str, to_email: str, subject: str, html_content: str
    ) -> dict:
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

        response = requests.post(
            "https://api.resend.com/emails", headers=headers, json=payload
        )

        if response.ok:
            return response.json()
        else:
            response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful


# Example usage
def send_email_using_resend_sdk(
    from_email: str, to_email: str, subject: str, html_content: str
) -> dict:
    sender = ResendSDKEmailSender()
    return sender.send_email(from_email, to_email, subject, html_content)


def send_email_using_resend_api(
    from_email: str, to_email: str, subject: str, html_content: str
) -> dict:
    sender = ResendAPIEmailSender()
    return sender.send_email(from_email, to_email, subject, html_content)


# Uncomment to test
# if __name__ == '__main__':
#     try:
#         data = send_email_using_resend_sdk("onboarding@resend.dev", "delivered@resend.dev", "Hello World", "<strong>it works!</strong>")
#         print(json.dumps(data, indent=2))
#         data = send_email_using_resend_api("Acme <onboarding@resend.dev>", "delivered@resend.dev", "hello world", "<strong>it works!</strong>")
#         print(json.dumps(data, indent=2))
#     except requests.exceptions.HTTPError as err:
#         print(f"Error: {err}")

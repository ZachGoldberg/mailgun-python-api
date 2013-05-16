import json
import requests


class MailgunAPI(object):
    def __init__(self, api_key, api_list_name, test_mode=False,
                 default_from_email=None):
        self.api_key = api_key
        self.api_list_name = api_list_name
        self.test_mode = test_mode
        self.default_from_email = default_from_email

    def _api_request(self, path, data, method="post"):
        try:
            http_func = getattr(requests, method.lower())
            response = http_func(
                "https://api.mailgun.net/v2/%s/%s" % (
                    self.api_list_name, path),
                auth=("api", self.api_key),
                data=data,
            )
            response_json = json.loads(response.content)
            success = response.ok
            reason = response_json['message']

        except BaseException as error:
            reason = error

        return (success, reason)

    def send_email(self, subject,
                   plain_text, html_text, to_email,
                   from_email=None):

        if isinstance(to_email, basestring):
            to_email = (to_email, )

        if not from_email:
            from_email = self.default_from_email

        data = {
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "text": plain_text,
            "o:testmode": self.test_mode,
            "html": html_text,
            }

        return self._api_request("messages", data)

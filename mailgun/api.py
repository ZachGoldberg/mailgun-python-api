import json
import requests
import urllib


class MailgunException(Exception):
    pass


class MailgunAPI(object):
    def __init__(self, api_key, api_list_name, test_mode=False,
                 default_from_email=None):
        self.api_key = api_key
        self.api_list_name = api_list_name
        self.test_mode = test_mode
        self.default_from_email = default_from_email

        # Some awkward fiddling to make the API namespace pretty
        from mailinglist import MailingList
        if self.__class__ != MailingList:
            self.MailingList = MailingList(api_key, api_list_name,
                                           test_mode, default_from_email)

    def _api_request(self, path, data, method=None):
        response_json = None
        success = False

        if not method:
            if data:
                method = "POST"
            else:
                method = "GET"

        query_string = ""
        if method.lower() == "get" and data:
            query_string = urllib.urlencode(data)
            data = None

        try:
            http_func = getattr(requests, method.lower())
            response = http_func(
                "https://api.mailgun.net/v2%s?%s" % (
                    path, query_string),
                auth=("api", self.api_key),
                data=data,
            )

            response_json = json.loads(response.content)
            success = response.ok
            reason = response_json.get('message')

        except BaseException as error:
            reason = error

        if not success:
            raise MailgunException(reason)

        return response_json

    def send_email(self, subject,
                   plain_text, html_text, to_email,
                   from_email=None, cc=None, bcc=None):

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

        if cc:
            data["cc"] = cc

        if bcc:
            data["bcc"] = bcc

        return self._api_request("/%s/messages" % self.api_list_name, data)

from mailgun import MailgunAPI


class MailingList(object):
    def __init__(self, api, address):
        self.address = address
        self.api = api

    @classmethod
    def from_api(cls, api, data):
        obj = cls(api, data.get("address"))
        for key, val in data.iteritems():
            setattr(obj, key, val)

        return obj

    def add_member(self, address,
                   name=None,
                   optional_vars=None,
                   subscribed=True):
        return self.api._api_request(
            "/lists/%s/members" % self.address,
            data={
                "address": address,
                "name": name,
                "vars": optional_vars,
                "subscribed": subscribed,
                "upsert": True,
                },
            method="POST")

    def remove_member(self, member_address):
        return self.api._api_request(
            "/lists/%s/members/%s" % (self.address,
                                      member_address),
            data={},
            method="DELETE")

    def get_members(self, subscribed=None):
        for member in self.api._api_list("/lists/%s/members" % self.address,
                                         method="GET"):
            yield member

    def email(self, subject, body, from_email, headers=None):
        return self.api.send_email(
            subject, body, body,
            to_email=self.address,
            from_email=from_email,
            headers=headers)

    def save(self):
        fields = ["description", "name", "access_level"]
        data = {}
        for field in fields:
            if getattr(self, field, None):
                data[field] = getattr(self, field)

        return self.api._api_request("/lists/%s" % self.address,
                              data=data,
                              method="PUT")

    def __unicode__(self):
        return self.address

    def __str__(self):
        return unicode(self)


class MailingLists(MailgunAPI):
    ACCESS_READONLY = "readonly"
    ACCESS_MEMBERS = "members"
    ACCESS_EVERYONE = "everyone"

    def get(self, address=None, lookup=True):
        if not lookup:
            return MailingList(self, address)

        data = {}
        if address:
            data["address"] = address

        for item in self._api_list("/lists",
                              data,
                              method="GET"):
            return MailingList.from_api(self, item)

    def list(self, address=None):
        data = {}
        if address:
            data["address"] = address

        for item in self._api_list("/lists",
                              data,
                              method="GET"):
            yield MailingList.from_api(self, item)

    def new(self, address, name, description,
            access_level=ACCESS_MEMBERS):
        return self._api_request(
            "/lists", method="POST", data={
                "address": address,
                "name": name,
                "description": description,
                "access_level": access_level,
                })



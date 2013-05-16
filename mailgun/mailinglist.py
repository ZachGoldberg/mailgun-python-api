from mailgun import MailgunAPI


class MailingList(MailgunAPI):

    def get(self, address=None):
        if address:
            result = self._api_request("/lists/%s" % address)

        skip = 0
        limit = 100
        while True:
            results = self._api_request(
                "/lists",
                data={
                    "skip": skip,
                    "limit": limit,
                    },
                method="GET")

            for item in results["items"]:
                yield item

            skip += limit
            if skip >= results["total_count"]:
                return

import requests
import sys
import re


class Hsts:

    def __init__(self, domain, age=10368000):
        self.domain = domain
        self.age = age
        if not self._get_hsts_enabled():
            print(
                "Failing HSTS status check: no"
                "HSTS header or max-age too short")
            sys.exit(1)

        print("Successful HSTS status check")

    def _get_hsts_enabled(self) -> bool:
        """
        For a given domain, return a bool to signal if expected HSTS header is
        present

        Expected behaviour is that HSTS should be set, with max-age of at least
        10368000 seconds (120 days), or other seconds if specified

        Returns:
        bool: True or False

        """
        try:
            print("Starting GET request to http://{}".format(self.domain))
            r = requests.get('https://{}'.format(self.domain), timeout=60,
                             allow_redirects=False)
        except Exception as e:
            print(
                "Exception connecting to https://{} with {}"
                .format(self.domain, str(e)))
            return False
        else:
            print(
                "Strict-Transport-Security header on https://{} returned {}"
                .format(self.domain, r.headers.get(
                        'Strict-Transport-Security')))
            m = re.search(r'max-age=(\d+)',
                          r.headers.get('Strict-Transport-Security', ''))
            max_age = -1
            if m:
                max_age = int(m.group(1))
            return max_age >= self.age

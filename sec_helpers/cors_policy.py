import requests
import sys


class CorsPolicy:

    def __init__(self, domain):
        self.domain = domain
        if not self._scan():
            sys.exit(1)

    def _scan(self):
        res = requests.get('https://{}'.format(self.domain), timeout=20,
                           allow_redirects=False)
        res_head = res.headers.get('Access-Control-Allow-Origin')

        if not res_head:
            print("Failing policy test: No Allowed Origins Specified")
            return False
        if str(res_head) == '*':
            print("Failing policy test: No Specific Origins Specified")
            return False

        print("Passing policy test: Allowed Origins Specified")
        return True

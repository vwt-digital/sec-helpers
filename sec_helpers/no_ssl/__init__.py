import subprocess  # nosec
import sys


class NoSsl:

    def __init__(self, domain):
        self.domain = domain
        if not self.test_process():
            sys.exit(1)

    def test_process(self):
        ossl = subprocess.run(  # nosec
            ['openssl', 's_client', '-connect', '{}:443'.format(self.domain), '-ssl3'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)

        if str(ossl.stderr).find("Option unknown option -ssl3") != -1:
            print("openssl does not support SSLv3")
            return False

        if str(ossl.stderr).find("no protocols available") != -1:
            print("no protocols available")
            return False

        if ossl.returncode == 1:
            print('No sign of SSLv3 allowance found')
            return True

        print('SSLv3 seems to be allowed')
        return False

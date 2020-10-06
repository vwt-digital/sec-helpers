import re
import subprocess  # nosec
import sys


class NoSsl:

    def __init__(self, domain):
        self.domain = domain
        if not self.test_process():
            sys.exit(1)

    def test_process(self):
        ossl_version = \
            str(subprocess.check_output(['openssl', 'version']))  # nosec
        if str(re.findall('([0-9]\\.[0-9]\\.[0-9]).',
                          ossl_version)[0]) != '1.0.2':
            print(
                '{} is not the right version. Download a compatible version'
                '(1.0.2): '
                'https://www.openssl.org/source/old/1.0.2'.format(
                    ossl_version))
            return True
        else:
            try:
                print(subprocess.check_output(  # nosec
                    ['/usr/local/bin/openssl', 's_client',
                     '-connect', '{}:443'.format(
                        self.domain),
                     '-ssl3'], timeout=15))
            except subprocess.CalledProcessError:
                print('No sign of SSLv3 allowance found')
                return True
            print('SSLv3 seems to be allowed')
            return False

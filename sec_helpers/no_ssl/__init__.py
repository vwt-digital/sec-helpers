import re
import subprocess  # nosec
from os import path
import sys


class NoSsl:

    def __init__(self, domain):
        ossl_version = \
            str(subprocess.check_output(['openssl', 'version']))  # nosec
        if str(re.findall('([0-9]\\.[0-9]\\.[0-9]).',
                          ossl_version)[0]) != '1.0.2':
            print(
                '{} is not the right version. Download a compatible version'
                '(1.0.2): '
                'https://www.openssl.org/source/old/1.0.2'.format(
                    ossl_version))
        elif subprocess.call(['bash',  # nosec
                              '{}/ssl3.sh'.format(path.dirname(  # nosec
                                  path.realpath(__file__))), domain]):
            sys.exit(1)

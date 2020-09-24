import argparse
import ssl
import re
import subprocess  # nosec

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    args = parser.parse_args()

    if str(re.findall('([0-9]\\.[0-9]\\.[0-9]).', ssl.OPENSSL_VERSION)[0]) != '1.0.2':
        print(
            '{} is not the right version. Download a compatible version (1.0.2): '
            'https://www.openssl.org/source/old/1.0.2'.format(
                ssl.OPENSSL_VERSION))
        exit(1)

    subprocess.call(['sh', 'verify-no-ssl/ssl3.sh', args.domain])  # nosec

import requests
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Secured API url')

    return parser.parse_args()


def scan(arguments):
    res = requests.get('https://{}'.format(arguments.domain), timeout=20, allow_redirects=False)
    res_head = res.headers.get('Access-Control-Allow-Origin')

    if not res_head or str(res_head) == '*':
        print("Failing policy test: No Allowed Origins Specified")
        return False

    print("Passing policy test: Allowed Origins Specified")
    return True


if __name__ == '__main__':
    args = parse_args()

    sys.exit(0 if scan(args) else 1)

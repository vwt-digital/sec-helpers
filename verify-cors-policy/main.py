import requests
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Secured API url')
    parser.add_argument('type', type=str, help='type')
    parser.add_argument('resource', type=str, help='Resources to scan')

    return parser.parse_args()


def scan_resource(resource, target):
    global passed
    res = requests.get('https://{}'.format(target), timeout=20, allow_redirects=False)
    res_head = str(res.headers.get('Access-Control-Allow-Origin'))
    print("Allowed Origins: " + res_head)
    loc_passed = res_head == resource
    if passed:
        passed = loc_passed
    return loc_passed


if __name__ == '__main__':
    passed = True
    args = parse_args()
    if not args.resource or args.type != 'api':
        print("Skipping cors policy test")
        sys.exit(0)
    print(str(args.resource) + (' \033[92mpassed\033[0m' if scan_resource(str(args.resource), args.domain) else ' \033[91mfailed\033[0m'))
    sys.exit(0 if passed else 1)

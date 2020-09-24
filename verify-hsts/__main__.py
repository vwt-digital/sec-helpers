import requests
import argparse
import sys
import re


def get_hsts_enabled(domain: str, age: int) -> bool:
    """
    For a given domain, return a bool to signal if expected HSTS header is present

    Expected behaviour is that HSTS should be set, with max-age of at least 10368000 seconds (120 days)

    Parameters:
    mydomain (string): A DNS domain, like e.g. dev.corp.example

    Returns:
    bool: True or False

    """
    try:
        print("Starting GET request to http://{}".format(domain))
        r = requests.get('https://{}'.format(domain), timeout=60, allow_redirects=False)
    except Exception as e:
        print("Exception connecting to https://{} with {}".format(domain, str(e)))
        return False
    else:
        print("Strict-Transport-Security header on https://{} returned {}".format(domain, r.headers.get(
            'Strict-Transport-Security')))
        m = re.search(r'max-age=(\d+)', r.headers.get('Strict-Transport-Security', ''))
        max_age = int(m.group(1))
        return max_age >= age


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    parser.add_argument('age', type=str, required=False, default=10368000, help='Minimal Max-Age (Default = 10368000)')
    args = parser.parse_args()

    if not get_hsts_enabled(args.domain, args.age):
        print("Failing HSTS status check: no HSTS header or max-age too short")
        sys.exit(1)

    print("Successful HSTS status check")
    sys.exit(0)

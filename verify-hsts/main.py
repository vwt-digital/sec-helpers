import requests
import argparse
import sys
import re
import json

def get_hsts_enabled(mydomain):
    """
    For a given domain, return a bool to signal if expected HSTS header is present

    Expected behaviour is that HSTS should be set, with max-age of at least 10368000 seconds (120 days)

    Parameters:
    mydomain (string): A DNS domain, like e.g. dev.corp.example

    Returns:
    bool: True or False

    """
    try:
        print("Starting GET request to http://{}".format(mydomain))
        r = requests.get('https://{}'.format(mydomain), timeout=20, allow_redirects=False)
    except Exception as e:
        print("Exception connecting to https://{} with {}".format(mydomain,str(e)))
        return False
    else:
        print("Strict-Transport-Security header on https://{} returned {}".format(mydomain,r.headers.get('Strict-Transport-Security')))
        m = re.search(r'max-age=(\d+)', r.headers.get('Strict-Transport-Security', ''))
        max_age = int(m.group(1))
        if max_age >= 10368000:
            return True
        else:
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    args = parser.parse_args()
    if not get_hsts_enabled(args.domain):
        print("Failing HSTS status check: no HSTS header or max-age too short")
        sys.exit(1)
    else:
        print("Successful HSTS status check")
        sys.exit(0)

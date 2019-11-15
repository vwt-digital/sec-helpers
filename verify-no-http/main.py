import requests
import argparse
import sys

def get_http_enabled(mydomain):
    """
    For a given domain, return a bool to signal if expected http behaviour is implemented.

    Expected behaviour is that http should be disabled, or 304-redirecting to https://

    Parameters:
    mydomain (string): A DNS domain, like e.g. dev.corp.example

    Returns:
    bool: True or False

    """
    try:
        print("Starting GET request to http://{}".format(mydomain))
        r = requests.get('http://{}'.format(mydomain), timeout=20)
    except Exception as e:
        print("Exception connecting to {} with {}".format(mydomain,str(e)))
        return False
    else:
        print("GET request to {} returned status {}".format(mydomain,r.status_code))
        if r.status_code == 301:
            return False
        else:
            return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    args = parser.parse_args()
    if get_http_enabled(args.domain):
        print("Failing http status check: http is enabled or not redirecting properly to https")
        sys.exit(1)
    else:
        print("Successful http status check: http is disabled or redirects to https")
        sys.exit(0)

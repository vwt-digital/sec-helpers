import requests
import argparse
import sys


def get_protocol_enabled(domain: str, url_pre: str = "http") -> bool:
    """
    For a given domain, return a bool to signal if expected http behaviour is implemented.

    Expected behaviour is that http should be disabled, or 304-redirecting to https://

    Parameters:
    domain (string): A DNS domain, like e.g. dev.corp.example
    url_pre (string): Category of protocol (secure or not secure)

    Returns:
    bool: True or False

    """
    try:
        print("Starting GET request to {}://{}".format(url_pre, domain))
        r = requests.get('{}://{}'.format(url_pre, domain), timeout=60, allow_redirects=False)
    except Exception as e:
        print("Exception connecting to {}://{} with {}".format(url_pre, domain, str(e)))
        return not url_pre == 'http'
    else:
        print("GET request to {}://{} returned status {}".format(url_pre, domain, r.status_code))
        return not (r.status_code == 301 or (r.status_code == 302 and url_pre == 'http'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    args = parser.parse_args()
    if get_protocol_enabled(args.domain):
        print("Failing http status check: http is enabled or not redirecting properly to https")
        sys.exit(1)
    if not get_protocol_enabled(args.domain, "https"):
        print("Failing https status check: https is not enabled")
        sys.exit(1)
    print("Successful http status check: http is disabled or redirects to https")
    sys.exit(0)

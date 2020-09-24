from socket import gaierror, create_connection
import sys
from ssl import SSLContext, SSLError
from typing import List
import argparse
import urllib.request
import json
from .protocol import DefinedProtocol

_configurations = []


def load_recommendations() -> List:
    protocols = []

    with urllib.request.urlopen("https://ssl-config.mozilla.org/guidelines/latest.json") as url:
        data = json.loads(url.read().decode())
        for configuration, level in data['configurations'].items():
            for version in level['tls_versions']:
                if version not in _configurations:
                    protocols.append(DefinedProtocol(version, configuration))
                    _configurations.append(version)
    return protocols


def check_protocols(hostname: str, protocols: List, force_passed: bool = False) -> int:
    exit_code = 0
    for protocol in protocols:
        print("\n-------\nProtocol: {}\nShould be active: {}".format(protocol.protocol, protocol.is_allowed()))
        try:
            with create_connection((hostname, 443)) as sock:
                ctx = SSLContext(protocol.get_ssl_attribute())
                for opposite in protocol.get_opposite_ssl_as_op_no(_configurations):
                    ctx.options |= opposite
                with ctx.wrap_socket(sock, server_hostname=hostname) as context_sock:
                    print("Connected with: {}".format(context_sock.version()))
                    print("Using cipher: {}".format(context_sock.cipher()))
                    failed = False
        except gaierror:
            print("{} is not valid".format(hostname))
            return 1
        except (ValueError, SSLError):
            failed = True

        if (failed and protocol.is_allowed()) or (not failed and not protocol.is_allowed()):
            print("\033[91m\tWrong configuration\033[0m")
            exit_code = 1

    print("\nTest on {} \033[91mfailed\033[0m".format(hostname) if exit_code == 1 else "\033[94mpassed\033[0m")
    if force_passed and exit_code:
        print("But we'll let it slide for now (you are testing an appspot domain)")
    return exit_code if not force_passed else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    parser.add_argument('--slide', action='store_true', help='Let exit code slide if not 0')
    args = parser.parse_args()

    sys.exit(check_protocols(args.domain, load_recommendations(), args.slide))

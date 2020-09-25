import sys
from socket import gaierror, create_connection
from ssl import SSLContext, SSLError
from typing import List
import urllib.request
import json
from .protocol import DefinedProtocol

_configurations = []


def load_recommendations() -> List:
    protocols = []

    with urllib.request.urlopen(  # nosec
            "https://ssl-config.mozilla.org/guidelines"  # nosec
            "/latest.json") as url:  # nosec
        data = json.loads(url.read().decode())
        for configuration, level in data['configurations'].items():
            for version in level['tls_versions']:
                if version not in _configurations:
                    protocols.append(DefinedProtocol(version, configuration))
                    _configurations.append(version)
    return protocols


class HighTls:

    def __init__(self, domain, slide=False):
        self.domain = domain
        self.slide = slide
        if self._check_protocols(load_recommendations()):
            sys.exit(1)

    def _check_protocols(self, protocols: List) -> int:
        exit_code = 0
        for protocol in protocols:
            print("\n-------\nProtocol: {}\nShould be active: {}"
                  .format(protocol.protocol, protocol.is_allowed()))
            try:
                with create_connection((self.domain, 443)) as sock:
                    ctx = SSLContext(protocol.get_ssl_attribute())
                    for opposite in protocol \
                            .get_opposite_ssl_as_op_no(_configurations):
                        ctx.options |= opposite
                    with ctx.wrap_socket(sock, server_hostname=self.domain) \
                            as context_sock:
                        print("Connected with: {}"
                              .format(context_sock.version()))
                        print("Using cipher: {}"
                              .format(context_sock.cipher()))
                        failed = False
            except gaierror:
                print("{} is not valid".format(self.domain))
                return 1
            except (ValueError, SSLError):
                failed = True

            if (failed and protocol.is_allowed()) or \
                    (not failed and not protocol.is_allowed()):
                print("\033[91m\tWrong configuration\033[0m")
                exit_code = 1

        print("\nTest on {} \033[91mfailed\033[0m".format(
            self.domain) if exit_code == 1 else "\033[94mpassed\033[0m")
        if self.slide and exit_code:
            print(
                "But we'll let it slide for now"
                "(you are testing an appspot domain)")
        return exit_code if not self.slide else 0

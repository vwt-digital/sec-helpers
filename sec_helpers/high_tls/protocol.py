import ssl
from typing import List


class DefinedProtocol:

    def __init__(self, protocol: str, configuration: str):
        self.protocol = protocol
        self.configuration = configuration

    def get_ssl_attribute(self):
        try:
            return getattr(ssl, f"PROTOCOL_{self.protocol.replace('.', '_')}")
        except AttributeError:
            if self.is_allowed:
                return ssl.PROTOCOL_TLS

    def is_allowed(self) -> bool:
        return self.configuration in ['modern', 'intermediate']

    def get_opposite_ssl_as_op_no(self, versions) -> List:
        opposite_versions = []
        for version in versions:
            if not version == self.protocol:
                opposite_versions \
                    .append(getattr(ssl, f"OP_NO_{version.replace('.', '_')}"))

        return opposite_versions

from OpenSSL import SSL
import ssl
_protocols = {
    "SSL 2": {
        "denied": True,
        "notation": SSL.SSLv2_METHOD
    },
    "SSL 3": {
        "denied": False,
        "notation": SSL.SSLv3_METHOD
    },
    "TLS1.0": {
        "denied": True,
        "notation": ssl.PROTOCOL_TLSv1
    },
    "TLS1.1": {
        "denied": True,
        "notation": ssl.PROTOCOL_TLSv1_1
    },
    "TLS1.2": {
        "denied": False,
        "notation": ssl.PROTOCOL_TLSv1_2
    }
}

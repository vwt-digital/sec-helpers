import ssl
_protocols = {
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

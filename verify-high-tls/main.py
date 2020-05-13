from socket import gaierror, create_connection
from sys import exit, argv
from protocol import _protocols
from ssl import SSLContext, SSLError

if len(argv) != 2:
    print("Expected one argument: hostname")
    exit(1)

hostname = argv[1]
exit_code = 0

for protocol in _protocols:

    failed = False
    connected_with = None
    cipher = None
    try:
        with create_connection((hostname, 443)) as sock:
            with SSLContext(_protocols[protocol]["notation"]).wrap_socket(sock, server_hostname=hostname) as ssock:
                connected_with = ssock.version()
                cipher = ssock.cipher()
                failed = False
    except gaierror:
        print("{hostname} is not valid".format(hostname=hostname))
        exit(1)
    except ValueError:
        failed = True
    except SSLError:
        failed = True

    print("\nProtocol: {protocol}:\nActive: {failed}\nShould be active: {denied}".format(protocol=protocol, failed=not failed,
                                                                                         denied=not _protocols[protocol]['denied']))
    if connected_with:
        print("Connected with: {connected_with}".format(connected_with=connected_with))
    if cipher:
        print("Using cipher: {cipher}".format(cipher=cipher))
    if (not failed and _protocols[protocol]["denied"]) or \
            (failed and not _protocols[protocol]["denied"]):
        print("\033[91m\tWrong configuration\033[0m")
        exit_code = 1

print("\nTest on {hostname} ".format(hostname=hostname) + ("\033[91mfailed\033[0m" if exit_code == 1 else "\033[94mpassed\033[0m"))
exit(exit_code)

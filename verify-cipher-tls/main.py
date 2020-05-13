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
    try:
        with create_connection((hostname, 443)) as sock:
            with SSLContext(_protocols[protocol]["notation"]).wrap_socket(sock, server_hostname=hostname):
                failed = False
    except gaierror:
        print(f"{hostname} is not valid")
        exit(1)
    except ValueError:
        failed = True
    except SSLError:
        failed = True

    print(f"\nProtocol: {protocol}:\nActive: {not failed}\nShould be active: {not _protocols[protocol]['denied']}")
    if (not failed and _protocols[protocol]["denied"]) or \
            (failed and not _protocols[protocol]["denied"]):
        print(f"\033[91m\tWrong configuration\033[0m")
        exit_code = 1

print(f"\nTest on {hostname} " + ("\033[91mfailed\033[0m" if exit_code == 1 else "\033[94mpassed\033[0m"))
exit(exit_code)

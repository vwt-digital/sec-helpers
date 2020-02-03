import time
import sys
import argparse
import ssllabsscanner


def get_grades(mydomain):
    """
    For a given domain, return a list of TLS rating grades from ssllabs.com API

    Parameters:
    myurl (string): A DNS domain, like e.g. dev.corp.example

    Returns:
    list: A list of TLS rating grades, e.g. ['A+', 'A']

    """
    retry = 0
    grades = []
    while retry < 10:
        try:
            data = ssllabsscanner.resultsFromCache(mydomain)
        except Exception as e:
            print("Exception in ssllabsscanner, " +
                  "trying again in 60 secs. {}".format(str(e)), flush=True)
            time.sleep(60)
            retry = retry+1
        else:
            grades = [key.get('grade', '') for key in data.get('endpoints', {})]
            if data.get('status', None) == 'READY':
                break
            else:
                print("Result not yet in cache, trying again in 60 secs",
                      flush=True)
                time.sleep(60)
                retry = retry+1
    return grades


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    args = parser.parse_args()
    grades = get_grades(args.domain)
    if bool(set(grades).intersection(['A', 'A+', 'B', 'B+'])):
        print("Successful grades: {}".format(grades))
        sys.exit(0)
    else:
        print("Failing grades: {}".format(grades))
        sys.exit(1)

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
    retry=0
    grades = []
    while retry<5:
        data = ssllabsscanner.resultsFromCache(mydomain)
        grades = [ key.get('grade','') for key in data.get('endpoints',{}) ]
        if data.get('status', None) =='READY':
            break
        else:
            print("Not yet in cache, trying again in 60 secs")
            time.sleep(60)
            retry=retry+1
    return grades

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    args = parser.parse_args()
    grades = get_grades(args.domain)
    if 'A' in grades or 'A+' in grades:
        print("Successful grades: {}".format(grades))
        sys.exit(0)
    else:
        print("Failing grades: {}".format(grades))
        sys.exit(1)

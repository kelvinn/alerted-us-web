import requests
import sys

if __name__ == '__main__':
    host_address = sys.argv[1:][0]
    if not host_address:
        print "[ERROR] when selecting host address"
        sys.exit(2)
    else:
        get_urls = ['/accounts/signup/', '/accounts/login/']
        for url in get_urls:
            r = requests.get(host_address + url, verify=False)
            if r.status_code != 200:
                print "[ERROR] when calling [" + url + "] got back HTTP response code: " + str(r.status_code)
                sys.exit(1)
            else:
                print "[SUCCESS] when calling [" + url + "]"
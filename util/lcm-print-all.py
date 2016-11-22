#!/usr/bin/python

# Print (tab delim) basic info for ALL clusters, dcs, nodes,
# repos, configs, ssh creds

import json
import requests
import sys

numargs = len(sys.argv) - 1 # ignore self in count
if ( numargs != 1 ):
    print("ERROR: Need OpsCenter URL, eg 8.7.6.5:8888")
    print("ERROR: {n} args passed, exactly 1 expected, exiting".format(n=numargs))
    sys.exit()

opsc_url = sys.argv[1]
things = ['nodes','datacenters','clusters','machine_credentials','config_profiles','repositories']

def printeach(response):
    for r in response['results']:
        print("\"{n}\"\t{id}\t{l}".format(n=r['name'],id=r['id'],l=r['href']))

for thing in things:
    print("LCM {t}:".format(t=thing))
    req = requests.get("http://{url}/api/v1/lcm/{t}/".format(url=opsc_url,t=thing)).json()
    printeach(req)
    print("")

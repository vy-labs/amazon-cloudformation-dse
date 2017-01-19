#!/usr/bin/python

# Delete ALL clusters, dcs, nodes,
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

def pretty(data):
    print json.dumps(data, sort_keys=True, indent=4)

# If clusters are deleted via the api dc's and nodes ARE deleted
# --> no message printed
# If done via the LCM gui, they AREN'T. I think Bug?
def deleteall(response):
    for r in response['results']:
        deleted = requests.delete(r['href'])
        print("Deleted: {d}".format(d=deleted.json()))

for thing in things:
    print("Deleting all {t} from LCM...".format(t=thing))
    req = requests.get("http://{url}/api/v1/lcm/{t}/".format(url=opsc_url,t=thing)).json()
    deleteall(req)

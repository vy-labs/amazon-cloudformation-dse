#!/usr/bin/python

import requests
import time
import json

opsc_url = '52.8.42.111:8888'

repojson = json.dumps({'use-proxy': True, 'name': 'dse repo', 'username': 'collin.poczatek@gmail.com', 'password': '73Por914'})
print repojson
repo = requests.post("http://{url}/api/v1/lcm/repositories/".format(url=opsc_url), data=repojson).json()
repos = requests.get("http://{url}/api/v1/lcm/repositories/".format(url=opsc_url)).json()
print repos

# can't use '~/' w/o cannonicalizing
f = open('/home/collin/.ssh/dse-keypair-us-west-1.pem', 'r')
privkey = f.read()
postdata=json.dumps({"become-mode":"sudo", "use-ssh-keys":True, "name":"ssh-creds", "login-user":"ubuntu","ssh-private-key":privkey})
print postdata

cred = requests.post("http://{url}/api/v1/lcm/machine_credentials/".format(url=opsc_url), data=postdata).json()
print cred

configjson = json.dumps({"datastax-version":"5.0.3", "name":"default","comment":"default profile"})
# add field like: "json":{"cassandra-yaml":{"gc_warn_threshold_in_ms":1500} } for customization
# should add num_tokens?

config = requests.post("http://{url}/api/v1/lcm/config_profiles/".format(url=opsc_url), data=configjson).json()
print config

clusterjson = json.dumps({"name":"test_cluster", "machine-credential-id": cred['id'], "repository-id": repo['id'], "config-profile-id": config['id']})
cluster = requests.post("http://{url}/api/v1/lcm/clusters/".format(url=opsc_url), data=clusterjson).json()

dc0json = json.dumps({"name": "dc0", "cluster-id": cluster['id']})
dc1json = json.dumps({"name": "dc1", "cluster-id": cluster['id']})

dc0 = requests.post("http://{url}/api/v1/lcm/datacenters/".format(url=opsc_url), data=dc0json).json()
dc1 = requests.post("http://{url}/api/v1/lcm/datacenters/".format(url=opsc_url), data=dc1json).json()

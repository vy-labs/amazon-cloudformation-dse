#!/usr/bin/python

import requests
import json

metadata_url = '169.254.169.254/latest/meta-data'
opsc_url = '52.8.42.111:8888'
lcm_url = opsc_url + '/api/v1/lcm'

# will need eventually
clusters = requests.get("http://{url}/clusters/".format(url=lcm_url)).json()
clusterid = clusters['results'][0]['id']

# assume 1 dc as of now
dcs = requests.get("http://{url}/datacenters/".format(url=lcm_url)).json()
dcid = dcs['results'][0]['id']
node_url = dcs['results'][0]['related-resources']['nodes']
nodecount = requests.get(dcs['results'][0]['related-resources']['nodes']).json()['count']
# assume 1 config
configid = requests.get("http://{url}/api/v1/lcm/config_profiles/".format(url=opsc_url)).json()['results'][0]['id']
# assume 1 ssh-creds
sshcredid = requests.get("http://{url}/api/v1/lcm/machine_credentials/".format(url=opsc_url)).json()['results'][0]['id']

# r = requests.get(url)
# r.status_code == 200 -> True
privateip = requests.get("http://{url}/local-ipv4".format(url=metadata_url)).text
publicip = requests.get("http://{url}/public-ipv4".format(url=metadata_url)).text

postdata = json.dumps({'name':'node'+str(nodecount),
                       'datacenter-id': dcid,
                       'ssh-management-address': publicip,
                       'listen-address': privateip,
                       'rpc-address': privateip,
                       'broadcast-address': publicip,
                       'broadcast-rpc-address': publicip,
                       'config-profile-id': configid,
                       'machine-credential-id': sshcredid})

node = requests.post("http://{url}/nodes/".format(url=lcm_url), data=postdata).json()

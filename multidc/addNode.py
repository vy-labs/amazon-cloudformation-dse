#!/usr/bin/python
import requests
import json
import time
import argparse
import utilLCM as lcm

# TODO!
# - addThing methods should return id value, or None with failure


def setupArgs():
    parser = argparse.ArgumentParser(description='Add calling instance to an LCM managed DSE cluster.')
    required = parser.add_argument_group('Required named arguments')
    required.add_argument('--opsc-ip', required=True, type=str,
                          help='Public ip of OpsCenter instance.')
    required.add_argument('--clustername', required=True, type=str,
                          help='Name of cluster.')
    required.add_argument('--dcname', required=True, type=str, help='Name of datacenter.')
    parser.add_argument('--dcsize', type=int, default=3,
                        help='Number of nodes in datacenter, default 3.')
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Verbose flag, right now a NO-OP.' )
    return parser

def writepubkey(pubkey):
    #No-op, this should happen up in the IaaS?
    return True

def main():
    parser = setupArgs()
    args = parser.parse_args()

    clustername = args.clustername
    lcm.opsc_url = args.opsc_ip+':8888'
    #datacenters = ['dc0','dc1','dc2']
    dcname = args.dcname
    dcsize = args.dcsize
    #pubkey = args.pubkey

    lcm.waitForOpsC()  # Block waiting for OpsC to spin up

    #writepubkey(pubkey)
    # ^^^ no-op, should happen up in the IaaS?

    # Check if the DC --this-- node should belong to exists, if not add DC
    c = lcm.checkForDC(dcname)
    if (c == False):
        print("Datacenter {n} doesn't exist, creating...".format(n=dcname))
        clusters = requests.get("http://{url}/api/v1/lcm/clusters/".format(url=lcm.opsc_url)).json()
        cid = clusters['results'][0]['id']
        lcm.addDC(dcname,cid)
    else:
        print("Datacenter {d} exists".format(d=dcname))

    # kludge, assuming ony one cluster
    dcid = ""
    datacenters = requests.get("http://{url}/api/v1/lcm/datacenters/".format(url=lcm.opsc_url)).json()
    for d in datacenters['results']:
        if (d['name'] == dcname):
            dcid = d['id']


    # always add self to DC
    nodes = requests.get("http://{url}/api/v1/lcm/datacenters/{dcid}/nodes/".format(url=lcm.opsc_url,dcid=dcid)).json()
    nodecount = nodes['count']
    nodename = 'node'+str(nodecount)
    privateip = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4").content
    nodeconf = json.dumps({
            'name': nodename,
            "datacenter-id": dcid,
            "ssh-management-address": privateip})
    node = requests.post("http://{url}/api/v1/lcm/nodes/".format(url=lcm.opsc_url),data=nodeconf).json()
    print("Added node '{n}', json:".format(n=nodename))
    lcm.pretty(node)

    nodes = requests.get("http://{url}/api/v1/lcm/datacenters/{dcid}/nodes/".format(url=lcm.opsc_url,dcid=dcid)).json()
    nodecount = nodes['count']
    if (nodecount == dcsize):
        print("Last node added, triggering install job...")
        lcm.triggerInstall(dcid)

# ----------------------------
if __name__ == "__main__":
    main()

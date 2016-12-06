#!/usr/bin/python
import requests
import json
import time
import argparse

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

def pretty(data):
    print '\n', json.dumps(data, sort_keys=True, indent=4), '\n'

def waitForOpsC(opsc_url):
    # Constants that should go elsewhere?
    maxtrys = 100 #connection attempts
    timeout = 0.1 # connection timeout in sec
    pause = 6 # sleep between attempts in sec
    # maxtrys * pause = 600 sec or 10 min, should be enough time for
    # OpsC instance to come up.
    count = 0
    while(True):
        count += 1
        if (count > maxtrys):
            print("Error: OpsC connection failed after {n} trys".format(n=maxtrys))
            return
        try:
            meta = requests.get("http://{url}/meta".format(url=opsc_url), timeout=timeout)
        except requests.exceptions.Timeout as e:
            print("Request {c} to OpsC timeout, wait {p} sec...".format(c=count,p=pause))
            time.sleep(pause)
            continue
        except requests.exceptions.ConnectionError as e:
            print("Request {c} to OpsC refused, wait {p} sec...".format(c=count,p=pause))
            time.sleep(pause)
            continue
        except Exception as e:
            # Do something?
            raise
        if (meta.status_code == 200):
            data = meta.json()
            print("Found OpsCenter version: {version}".format(version=data['version']))
            return

def checkForCluster(cname):
    try:
        clusters = requests.get("http://{url}/api/v1/lcm/clusters/".format(url=opsc_url)).json()
        # This is a weak test. Assuming if there's any cluster,
        # it's the one we want. Done in the name of expedience, to change.
        if (clusters['count']==1):
            return True
        else:
            return False
    except requests.exceptions.Timeout as e:
        print("Request for cluster config timed out.")
        return False
    except requests.exceptions.ConnectionError as e:
        print("Request for cluster config refused.")
        return False
    except Exception as e:
        # Do something?
        raise
    return (cname in clusterconf)

def checkForDC(dcname):
    try:
        dcs = requests.get("http://{url}/api/v1/lcm/datacenters/".format(url=opsc_url)).json()
        exists = False
        for dc in dcs['results']:
            if (dc['name'] == dcname):
                exists = True
        return exists
    except requests.exceptions.Timeout as e:
        print("Request to add repo timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print("Request to add repo refused.")
        return None
    except Exception as e:
        # Do something?
        raise

def addDC(dcname, cid):
    try:
        dc = json.dumps({
            'name': dcname,
            'cluster-id': cid})
        dcconf = requests.post("http://{url}/api/v1/lcm/datacenters/".format(url=opsc_url),data=dc).json()
        print("Added datacenter {n}, json:".format(n=dcname))
        pretty(dcconf)
        return dcconf['id']
    except requests.exceptions.Timeout as e:
        print("Request to add repo timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print("Request to add repo refused.")
        return None
    except Exception as e:
        # Do something?
        raise

def triggerInstall(dcid):
    data = json.dumps({
            "job-type":"install",
            "job-scope":"datacenter",
            "resource-id":dcid,
            "auto-bootstrap":True,
            "continue-on-error":False})
    response = requests.post("http://{url}/api/v1/lcm/actions/install".format(url=opsc_url),data=data).json()
    pretty(response)

def main():
    parser = setupArgs()
    args = parser.parse_args()

    clustername = args.clustername
    opsc_url = opsc-ip+':8888'
    #datacenters = ['dc0','dc1','dc2']
    dcname = args.dcname
    dcsize = args.dcsize
    #pubkey = args.pubkey

    waitForOpsC(opsc_url)  # Block waiting for OpsC to spin up

    #writepubkey(pubkey)
    # ^^^ no-op, should happen up in the IaaS?

    # return config instead of bool?
    c = checkForCluster(clustername)
    if (c == False): # cluster doesn't esist -> must be 1st node -> do setup
        print("Cluster {n} doesn't exist, creating...".format(n=clustername))
        cred = addCred(dsecred)
        repo = addRepo(dserepo)
        conf = addConfig(defaultconfig)
        cid = addCluster(clustername, cred['id'], repo['id'], conf['id'])
    else:
        print("Cluster {n} exists".format(n=clustername))

    # Check if the DC --this-- node should belong to exists, if not create-stack
    c = checkForDC(dcname)
    if (c == False):
        print("Datacenter {n} doesn't exist, creating...".format(n=dcname))
        clusters = requests.get("http://{url}/api/v1/lcm/clusters/".format(url=opsc_url)).json()
        addDC(dcname,cid)
    else:
        print("Datacenter {d} exists".format(d=dcname))

    # kludge, assuming ony one cluster
    dcid = ""
    datacenters = requests.get("http://{url}/api/v1/lcm/datacenters/".format(url=opsc_url)).json()
    for d in datacenters['results']:
        if (d['name'] == dcname):
            dcid = d['id']

    # always add self to DC
    nodes = requests.get("http://{url}/api/v1/lcm/datacenters/{dcid}/nodes/".format(url=opsc_url,dcid=dcid)).json()
    nodecount = nodes['count']
    nodename = 'node'+str(nodecount)
    privateip = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4").content
    nodeconf = json.dumps({
            'name': nodename,
            "datacenter-id": dcid,
            "ssh-management-address": privateip})
    node = requests.post("http://{url}/api/v1/lcm/nodes/".format(url=opsc_url),data=nodeconf).json()
    print("Added node '{n}', json:".format(n=nodename))
    pretty(node)

    nodes = requests.get("http://{url}/api/v1/lcm/datacenters/{dcid}/nodes/".format(url=opsc_url,dcid=dcid)).json()
    nodecount = nodes['count']
    if (nodecount == dcsize):
        print("Last node added, triggering install job...")
        triggerInstall(dcid)

# ----------------------------
if __name__ == "__main__":
    main()

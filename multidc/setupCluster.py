#!/usr/bin/python
import requests
import json
import time
import argparse
import os


def setupArgs():
    parser = argparse.ArgumentParser(description='Setup LCM managed DSE cluster, repo, config, and ssh creds')
    required = parser.add_argument_group('Required named arguments')
    required.add_argument('--opsc-ip', required=True, type=str,
                          help='public ip of OpsCenter instance')
    required.add_argument('--clustername', required=True, type=str,
                          help='Name of cluster.')
    required.add_argument('--privkey', required=True, type=str,
                          help='private key (public key on all nodes) to be used by OpsCenter')
    parser.add_argument('--verbose',
                        action='store_true',
                        help='verbose flag, right now a NO-OP' )
    return parser


def addCluster(cname, credid, repoid, configid):
    try:
        conf = json.dumps({
            'name': cname,
            'machine-credential-id': credid,
            'repository-id': repoid,
            'config-profile-id': configid})
        clusterconf = requests.post("http://{url}/api/v1/lcm/clusters/".format(url=opsc_url),data=conf).json()
        print("Added cluster, json:")
        pretty(clusterconf)
        return clusterconf['id']
    except requests.exceptions.Timeout as e:
        print("Request for cluster config timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print("Request for cluster config refused.")
        return None
    except Exception as e:
        # Do something?
        raise
    return clusterconf

def addCred(cred):
    try:
        creds = requests.get("http://{url}/api/v1/lcm/machine_credentials/".format(url=opsc_url)).json()
        if (creds['count']==0):
            creds = requests.post("http://{url}/api/v1/lcm/machine_credentials/".format(url=opsc_url),data=cred).json()
            print("Added default dse creds, json:")
            pretty(creds)
            return creds
    except requests.exceptions.Timeout as e:
        print("Request to add ssh creds timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print("Request to add ssh creds refused.")
        return None
    except Exception as e:
        # Do something?
        raise

def addConfig(conf):
    try:
        configs = requests.get("http://{url}/api/v1/lcm/config_profiles/".format(url=opsc_url)).json()
        if (configs['count']==0):
            config = requests.post("http://{url}/api/v1/lcm/config_profiles/".format(url=opsc_url),data=conf).json()
            print("Added default condig profile, json:")
            pretty(config)
            return config
    except requests.exceptions.Timeout as e:
        print("Request to add config profile timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print("Request to add config profile refused.")
        return None
    except Exception as e:
        # Do something?
        raise

def addRepo(repo):
    try:
        repos = requests.get("http://{url}/api/v1/lcm/repositories/".format(url=opsc_url)).json()
        if (repos['count']==0):
            repconf = requests.post("http://{url}/api/v1/lcm/repositories/".format(url=opsc_url),data=dserepo).json()
            print("Added default repo, json:")
            pretty(repconf)
            return repconf
    except requests.exceptions.Timeout as e:
        print("Request to add repo timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print("Request to add repo refused.")
        return None
    except Exception as e:
        # Do something?
        raise

# Copying code! Should move all LCM calls out to util file
def waitForOpsC(opsc_url):
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


def pretty(data):
    print '\n', json.dumps(data, sort_keys=True, indent=4), '\n'

def main():
    parser = setupArgs()
    args = parser.parse_args()
    clustername = args.clustername
    opsc_url = args.opsc_ip+':8888'
    keypath = os.path.abspath(args.privkey)
    with open(keypath, 'r') as keyfile:
        privkey=keyfile.read()

# sYay globals!
# These should move to a config file, passed as arg maybe ?
    dserepo = json.dumps({
        "name":"DSE repo",
        "username":"collin.poczatek+awstesting@gmail.com",
        "password":"Cassandra1"})

    dsecred = json.dumps({
        "become-mode":"sudo",
        "use-ssh-keys":True,
        "name":"dse creds",
        "login-user":"ubuntu",
        "ssh-private-key":privkey,
        "become-user":None})

    defaultconfig = json.dumps({
        "name":"Default config",
        "datastax-version": "5.0.3",
        "json": {'cassandra-yaml': {"authenticator":"com.datastax.bdp.cassandra.auth.AllowAllAuthenticator"}}})

    waitForOpsC(opsc_url)  # Block waiting for OpsC to spin up


# ----------------------------
if __name__ == "__main__":
    main()

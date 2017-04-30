#!/usr/bin/python
import requests
import json
import time
import argparse
import os
import utilLCM as lcm

def setupArgs():
    parser = argparse.ArgumentParser(description='Setup LCM managed DSE cluster, repo, config, and ssh creds')
    required = parser.add_argument_group('Required named arguments')
    required.add_argument('--opsc-ip', required=True, type=str,
                          help='public ip of OpsCenter instance')
    required.add_argument('--clustername', required=True, type=str,
                          help='Name of cluster.')
    required.add_argument('--privkey', required=True, type=str,
                          help='abs path to private key (public key on all nodes) to be used by OpsCenter')
    parser.add_argument('--verbose',
                        action='store_true',
                        help='verbose flag, right now a NO-OP' )
    parser.add_argument('--dse_username',
                        help='username')
    parser.add_argument('--dse_password',
                         help='password')
    return parser

def main():
    parser = setupArgs()
    args = parser.parse_args()
    clustername = args.clustername
    lcm.opsc_url = args.opsc_ip+':8888'
    username = args.dse_username
    password = args.dse_password
    keypath = os.path.abspath(args.privkey)
    with open(keypath, 'r') as keyfile:
        privkey=keyfile.read()

    print "Create cluster {c} at {u} with keypath {k}".format(c=clustername, u=lcm.opsc_url, k=keypath)
# Yay globals!
# These should move to a config file, passed as arg maybe ?
    dserepo = json.dumps({
        "name":"DSE repo",
        "username": username,
        "password": password})

    dsecred = json.dumps({
        "become-mode":"sudo",
        "use-ssh-keys":True,
        "name":"DSE creds",
        "login-user":"ubuntu",
        "ssh-private-key":privkey,
        "become-user":None})

    defaultconfig = json.dumps({
        "name":"Default config",
        "datastax-version": "5.1",
        "json": {
           'cassandra-yaml': {
              "authenticator":"PasswordAuthenticator",
              "authorizer": "CassandraAuthorizer",
              "num_tokens":256,
              "endpoint_snitch":"GossipingPropertyFileSnitch"
           },
           'spark-env-sh':{
              "spark-master-webui-port": 7080
           }
        }})

    lcm.waitForOpsC()  # Block waiting for OpsC to spin up

    # return config instead of bool?
    c = lcm.checkForCluster(clustername)
    if (c == False): # cluster doesn't esist -> must be 1st node -> do setup
        print("Cluster {n} doesn't exist, creating...".format(n=clustername))
        cred = lcm.addCred(dsecred)
        repo = lcm.addRepo(dserepo)
        conf = lcm.addConfig(defaultconfig)
        cid = lcm.addCluster(clustername, cred['id'], repo['id'], conf['id'])
    else:
        print("Cluster {n} exists".format(n=clustername))



# ----------------------------
if __name__ == "__main__":
    main()

#!/usr/bin/python
import requests
import json
import time

def pretty(data):
    print json.dumps(data, sort_keys=True, indent=4)

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

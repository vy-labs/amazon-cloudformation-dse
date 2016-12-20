# Intro

There are 3 steps the [lcm install scripts](../lcm/) go through.
- **setupCluster.py**: LCM API calls to create definitions for *cluster, config set, ssh credentials,* and *repo*
- **addNode.py**: LCM API calls to create *datacenter* (if needed) and *node*.
- **gen_address_yaml.sh**: creates file */var/lib/datastax-agent/conf/address.yaml* for DSE agent (to be depriacated)

The *setupCluster.py* script is called **once**, and *addNode.py* and *gen_address_yaml.sh* called **on each node**. These scripts should be fairly portable as they don't themselves depend on any AWS service. Theoretically, the python scripts could be called from anywhere and not necessarily on the OpsCenter or node instances as they are in this project.

Note that the scripts need the *requests* library which can be installed with `sudo pip install requests`

The scripts themselves are self documented and understand the usual *-h* | *--help* flag.

# setupCluster.py

```
./setupCluster.py --help
usage: setupCluster.py [-h] --opsc-ip OPSC_IP --clustername CLUSTERNAME
                       --privkey PRIVKEY [--verbose]

Setup LCM managed DSE cluster, repo, config, and ssh creds

optional arguments:
  -h, --help            show this help message and exit
  --verbose             verbose flag, right now a NO-OP

Required named arguments:
  --opsc-ip OPSC_IP     public ip of OpsCenter instance
  --clustername CLUSTERNAME
                        Name of cluster.
  --privkey PRIVKEY     abs path to private key (public key on all nodes) to
                        be used by OpsCenter
```

# addNode.py

```
./addNode.py --help
usage: addNode.py [-h] --opsc-ip OPSC_IP --clustername CLUSTERNAME --dcname
                  DCNAME --nodeid NODEID --privip PRIVIP --pubip PUBIP
                  [--dcsize DCSIZE] [--verbose]

Add calling instance to an LCM managed DSE cluster.

optional arguments:
  -h, --help            show this help message and exit
  --dcsize DCSIZE       Number of nodes in datacenter, default 3.
  --verbose             Verbose flag, right now a NO-OP.

Required named arguments:
  --opsc-ip OPSC_IP     Public ip of OpsCenter instance.
  --clustername CLUSTERNAME
                        Name of cluster.
  --dcname DCNAME       Name of datacenter.
  --nodeid NODEID       Unique node id.
  --privip PRIVIP       Private ip of node.
  --pubip PUBIP         Public ip of node.

```

# gen_address_yaml.sh
The *gen_address_yaml.sh* script takes 2 positional arguments for private and public ip's of the node and **prints** the yaml file. These can be retrieved by calls to the AWS metadata service (or similar service.)

```
privateip=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4
publicip=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4
./gen_address_yaml.sh $privateip $publicip
```

# Example Usage
Below is example bash on how to call the scripts. This is similar to (but not necessarily identical to) what's in the templates. Note, some commands may require `sudo` depending on your environment.

## On OpsCenter instance
```
cd ~/.ssh/
ssh-keygen -t rsa -N '' -f lcm.pem
pip install requests
wget https://github.com/DSPN/amazon-cloudformation-dse/archive/master.zip
unzip master.zip
cd amazon-cloudformation-dse-master/lcm/
pubip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
privkey=$(readlink -f ~ubuntu/.ssh/lcm.pem)
./setupCluster.py \
  --opsc-ip $pubip \
  --clustername "mycluster" \
  --privkey $privkey
```

## On Each Node
In the CFn templates we're passing in values for: *pubkey, opsc-ip, clustername, dcsize,* and *dcname*; curls calls the the AWS metadata service can be replaced with similar calls or a command like `hostname -I`
```
pubkey="" #pubkey must be defined!
pip install requests
cd ~/
echo $pubkey >> .ssh/authorized_keys
wget https://github.com/DSPN/amazon-cloudformation-dse/archive/master.zip
unzip master.zip
cd amazon-cloudformation-dse-master/lcm/
pubip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
privip=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
nodeid=$(curl http://169.254.169.254/latest/meta-data/instance-id)
./addNode.py \
  --opsc-ip "1.2.3.4" \
  --clustername "mycluster" \
  --dcsize 5 \
  --dcname "dc0" \
  --pubip $pubip \
  --privip $privip \
  --nodeid $nodeid
```
After adding the node you also need to call `gen_address_yaml.sh`

```
privateip=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4
publicip=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4
dir=/var/lib/datastax-agent/conf/
mkdir -p $dir
./gen_address_yaml.sh $privateip $publicip > $dir/address.yaml
```

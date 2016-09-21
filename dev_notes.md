

# For development only, unfit for human consumption.

## General points
- Don't try anything smaller than a t2.medium, I don't think even the install finishes correctly.
- Looks like the VPC takes presidence over the cloudformation template?

Calling `create-key-pair` returns json w/ private key, key-name, and fingerprint.
Assuming it would return text if pref set that way.

```
collin@Cpoczatek-M3800:AWS$ aws ec2 create-key-pair --key-name jcp-keypair
{
    "KeyMaterial": "-----BEGIN RSA PRIVATE KEY-----[[[string of actual private key, with \n's]]]-----END RSA PRIVATE KEY-----",
    "KeyName": "jcp-keypair",
    "KeyFingerprint": "5e:6a:d2:a8:58:00:c0:86:95:84:52:0c:1b:fe:5d:dc:e5:c8:fd:0e"
}
```

New instance for either OpsC or node
```
sudo apt-get -y install unzip && \
wget https://github.com/DSPN/install-datastax-ubuntu/archive/master.zip && \
unzip master.zip && \
cd install-datastax-ubuntu-master/bin/
```
dse.sh:
```
cloud_type=$1
seed_nodes_dns_names=$2
data_center_name=$3
opscenter_dns_name=$4

# Try by hand

ubuntu@ip-172-31-22-27:~/install-datastax-ubuntu-master/bin$ sudo ./dse.sh "aws" "ip-172-31-22-27" "dc0" "ip-172-31-22-26" 2>1 | tee ~ubuntu/dse.log

# other instance

ubuntu@ip-172-31-22-26:~/install-datastax-ubuntu-master/bin$ sudo ./opscenter.sh "aws" "ip-172-31-22-27" 2>1 | tee ~ubuntu/opsc.log

```

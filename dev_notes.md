

# For development only, unfit for human consumption.

## General points
- Don't try anything smaller than a t2.medium, I don't think even the install finishes correctly.
- Looks like the VPC takes presidence over the cloudformation template? Specifying the VPC in the template works, but the instances show up in the default VPC? I think maybe this was a silent-ish failure (I didn't see any errors) since I didn't create a subnet in that VPC. So it errored out and put things in the default vpc?
- List or delete stack `aws cloudformation {list-stacks, delete-stack --stack-name name}`
- Calling `create-key-pair` returns json w/ private key, key-name, and fingerprint. Assuming it would return text if pref set that way.
```
collin@Cpoczatek-M3800:AWS$ aws ec2 create-key-pair --key-name jcp-keypair
{
    "KeyMaterial": "-----BEGIN RSA PRIVATE KEY-----[[[string of actual private key, with \n's]]]-----END RSA PRIVATE KEY-----",
    "KeyName": "jcp-keypair",
    "KeyFingerprint": "5e:6a:d2:a8:58:00:c0:86:95:84:52:0c:1b:fe:5d:dc:e5:c8:fd:0e"
}
```
- Node for OpsCenter failing to complete cloudinit? I think this was due to not explicitly setting _SecutityGroups_ (notice the s):
```
You seriously can't copy from the AWS web console?
It looked like there was a cloudinit error...
```
- If every Resource doesn't signal `CREATE_COMPLETE` stooop, the stack will get torn down.

- Aha! You can set an ip for an instance in a VPC

```
http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html
PrivateIpAddress
    The private IP address for this instance.

    Important
    If you make an update to an instance that requires replacement, you must
    assign a new private IP address. During a replacement, AWS CloudFormation
    creates a new instance but doesn't delete the old instance until the stack
    has successfully updated. If the stack update fails, AWS CloudFormation uses
    the old instance in order to roll back the stack to the previous working
    state. The old and new instances cannot have the same private IP address.

    (Optional) If you're using Amazon VPC, you can use this parameter to assign
    the instance a specific available IP address from the subnet (for example,
    10.0.0.25). By default, Amazon VPC selects an IP address from the subnet for
    the instance.

    Required: No
    Type: String
    Update requires: Replacement

New instance for either OpsC or node
```
```
sudo apt-get -y install unzip && \
wget https://github.com/DSPN/install-datastax-ubuntu/archive/master.zip && \
unzip master.zip && \
cd install-datastax-ubuntu-master/bin/

dse.sh:
cloud_type=$1
seed_nodes_dns_names=$2
data_center_name=$3
opscenter_dns_name=$4
```

Trying fixed IPs for OpsC and seed node, 172.31.16.10 and 172.31.16.20

OpsC instance doesn't finish cloud-init:
manage_existing_cluster.sh not returning ->
opscenter.sh note returning ->
cfn-init not returning SUCCESS.

Fixed (typo): Template bug for cloud-init on SeedNodeInstance
Error occurred during build: No configuration found with name: install_des

On Agents panel of OpsC seed node had private IP, rest public? Causing problems?
You can use curl to the public or local ip from within an instance:
```
ubuntu@ip-172-31-16-10:~$ curl http://169.254.169.254/latest/meta-data/public-ipv4
52.88.228.221
ubuntu@ip-172-31-16-10:~$ curl http://169.254.169.254/latest/meta-data/local-ipv4
172.31.16.10
```

I was confusing cloud-init and cfn-init, and the [pip install](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html) is the way for cfn-init.

Kludge to pause OpsC install
```
"head -n $(grep -n \"./opscenter/start.sh\" opscenter.sh | cut -f1 -d:) opscenter.sh > trim.sh \n",
"chmod 755 ./trim.sh \n",
"./trim.sh $cloud_type $seed_node_dns_name $data_center_name &\n"
```

Get info on seed_node from seed_node:
```
"seed_node_dns_name=\"$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)\" \n",
```
Get info from other instance:
```
{ "Fn::GetAtt" : [ "OpsCenterInstance" , "PublicDnsName" ] }
```

trim Kludge
```
"head -n $(grep -n \"./opscenter/start.sh\" opscenter.sh | cut -f1 -d:) opscenter.sh > trim.sh \n",
"chmod 755 ./trim.sh \n",
"./trim.sh $cloud_type $seed_node_dns_name $data_center_name &\n"
```
un-kludge
```
"./opscenter.sh $cloud_type $seed_node_dns_name $data_center_name &\n"
```

First try of deploy-dse.sh. ~~There's a bug with $region~~ Fixed

```
collin@zazen:singledc$ aws ec2 create-vpc --region us-east-1 --cidr-block 10.0.0.0/16
{
    "Vpc": {
        "VpcId": "vpc-33fad254",
        "InstanceTenancy": "default",
        "State": "pending",
        "DhcpOptionsId": "dopt-528b4c36",
        "CidrBlock": "10.0.0.0/16",
        "IsDefault": false
    }
}
collin@zazen:singledc$
collin@zazen:singledc$
collin@zazen:singledc$ ./deploy-dse.sh -r "us-east-1" -v "vpc-33fad254"
./deploy-dse.sh: illegal option -- r
Invalid option -
Using parameters:
email ->	 donotreply@datastax.com
key ->		 dse-keypair-us-west-2
vpc ->		 vpc-631fd407
size ->		 4
dcname ->	 dc0
instance ->	 t2.medium
sshlocation ->	 0.0.0.0/0
region ->	 us-west-2

Validating template...
{
    "StackId": "arn:aws:cloudformation:us-west-2:819041172558:stack/dse-stack/7e445fb0-8673-11e6-b10f-50a68a201256"
}
collin@zazen:singledc$
```


# Info and Prerequisites

The purpose of the files in this directory are to make is quick and simple to deploy a multi-datacenter DSE cluster across AWS regions, however it can be used for a single region deployment. Note, this is under active development and will change in the future, namely deployment will be reduced to a single command. Also at this time the scripts don't take any arguments, changeable parameters are at the top of each script.

These scripts and templates use OpsCenter's Lifecycle Manager (LCM) to install and configure DSE. This is discussed [here](./LCM.md).

## Prerequisites

The only setup required is to install and configure the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Documentation for the AWS CLI is [here](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cli.html).  To configure the AWS CLI run the command `aws configure` and follow the prompts.

These deploy scripts don't create any keypairs needed to deploy the EC2 instances used for OpsCenter or the DSE nodes. Before running them create a key for each region you are going to deploy to by running the command below setting `region` and `keyname`, or you can use existing keys. Note, omitting `--region $region` in the command below uses your account default.

```
region="us-west-1"
keyname="mykey"
aws ec2 create-key-pair --region $region --key-name $keyname --query 'KeyMaterial' --output text > ~/.ssh/$keyname.pem
```

# Deploying OpsCenter

To deploy OpsCenter run `deploy_opscenter.sh` setting the two variables `keyname` and `clustername` at the top of the script.

```
jcp@tenkara:multidc$ ./deploy_opscenter.sh

{
    "StackId": "arn:aws:cloudformation:us-east-1:819041172558:stack/opscenter-stack/3987ae10-c2f8-11e6-a2b5-50d5cd2758d2"
}
```
You can watch its progress either from the AWS web console [CloudFormation](https://console.aws.amazon.com/cloudformation/home) page or by running `aws cloudformation describe-stacks --stack-name opscenter-stack --query 'Stacks[0].StackStatus' `. Once the stataus of the stack is `CREATE_COMPLETE` You can view the outputs of the stack in the web console or with the command below.

```
aws cloudformation describe-stacks --stack-name opscenter-stack --query 'Stacks[0].Outputs[*]'

[
    {
        "Description": "URL for OpsCenter",
        "OutputKey": "OpsCenterURL",
        "OutputValue": "http://ec2-34-195-78-169.compute-1.amazonaws.com:8888"
    },
    {
        "Description": "URL for Lifecycle Manager",
        "OutputKey": "LCMURL",
        "OutputValue": "http://ec2-34-195-78-169.compute-1.amazonaws.com:8888/opscenter/lcm.html"
    },
    {
        "Description": "Public IP for OpsCenter",
        "OutputKey": "OpsCenterPublicIP",
        "OutputValue": "34.195.78.169"
    }
]
```
Opening the URL for Lifecycle Manager in a browser will let you monitor the deployment of the datacenters. (\*: there's a known bug that LCM won't load immediately after `CREATE_COMPLETE`, please wait ~2 minutes)

# Deploying a Datacenter

Simply running `deploy_datacenter.sh` will deploy a 5 node cluster in the same region as the `opscenter-stack` using the same key. You can change `dcname,region, dcsize` or `key` in the script. Note that the `key` used must exist in the `region` used.

```
./deploy_datacenter.sh

Using opscenter ip: 34.195.39.250
Using cluster name: mycluster
Using public key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCQ4mXBWiv1Iuyxccn18viVfC06kAtWpfazruJJI4QVAheHmJvhXnnE9DrURGINP6ZcMd9zXtWTauUs1dpDvXVt+um4e1sdYd71yk6Pw5Mvgjl9AtHUlpbEG1mqvJfcRp4ynrAqDtQPSDShgqYvaG9SNYpbr+FOEQKUHEoRjSLbrd15MAyNJvmsUp3PJ5qP1rvqAydseAkiu9knNVPzWVlLwG0uR8pVA8o7ITOxg4W/pL1Xm/+kSOs4It/D1iV/6dxKY1Bo4/k9A7BVJZqT6dSDxpPVtX1Lt39SNOkV8D8SG9E+zf/fks0PDXnldTNzJLt8TgFabC4QPXgkCXXdI++/ root@ip-172-31-50-123
Using stack name: dc-us-east-stack

{
    "StackId": "arn:aws:cloudformation:us-east-1:819041172558:stack/dc-us-east-stack/35577fa0-c2fd-11e6-97fe-503aca4a58d1"
}

```


# Deploying another Datacenter

- At a minimum you need to only change the `dcname` variable in `deploy_datacenter.sh` to deploy another datacenter.
- You can deploy to another region by changing `region` and `key` to be a keypair in the new region.
- Changing the number of nodes in the datacenter `dcsize` has no effect on other values.


```
./deploy_datacenter.sh

Using opscenter ip: 34.195.39.250
Using cluster name: mycluster
Using public key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCQ4mXBWiv1Iuyxccn18viVfC06kAtWpfazruJJI4QVAheHmJvhXnnE9DrURGINP6ZcMd9zXtWTauUs1dpDvXVt+um4e1sdYd71yk6Pw5Mvgjl9AtHUlpbEG1mqvJfcRp4ynrAqDtQPSDShgqYvaG9SNYpbr+FOEQKUHEoRjSLbrd15MAyNJvmsUp3PJ5qP1rvqAydseAkiu9knNVPzWVlLwG0uR8pVA8o7ITOxg4W/pL1Xm/+kSOs4It/D1iV/6dxKY1Bo4/k9A7BVJZqT6dSDxpPVtX1Lt39SNOkV8D8SG9E+zf/fks0PDXnldTNzJLt8TgFabC4QPXgkCXXdI++/ root@ip-172-31-50-123
Using stack name: dc-us-west-stack

{
    "StackId": "arn:aws:cloudformation:us-west-1:819041172558:stack/dc-us-west-stack/ce07f7d0-c31f-11e6-878d-500cf8eeb899"
}
```
# Teardown

The deploy scripts write the stack name and region to the tempfile `teardown.txt`. Running `teardown.sh` deletes these stacks and then the tempfile.

```
./teardown.sh
deleting stack: opscenter-stack 	 us-east-1 ...
deleting stack: dc-us-east-stack 	 us-east-1 ...
deleting stack: dc-us-west-stack 	 us-west-1 ...
Stacks deleted: 3
```

# Single Node

This is an Amazon CloudFormation template that will deploy a single node DataStax Enterprise cluster.

To run the template you will need to have the AWS CLI installed.  Instruction on that are available [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Documentation for the AWS CLI is [here](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cli.html).  To configure the AWS CLI run the command:

    aws configure

## Creating a Single Node
Note: _deploy-single.sh_ and _single-node.json_ are for didactic or testing purposed only, they are not intended to be used to build a cluster.

To create a single node run the command:

    ./deploy-single.sh myteststack key-pair

It takes 2 arguments, the name of the stack to create and the name of a key-pair.  The script then validates the template and deploys it to create a cluster (printing json as shown below).

```
$ ./deploy-single.sh myteststack test-keypair

{
    "Description": "AWS CloudFormation Sample Template DataStax Enterprise: Create a DSE stack using a single EC2 instance. This template demonstrates using the AWS CloudFormation bootstrap scripts to install the packages and files necessary to deploy DSE. **WARNING** This template creates an Amazon EC2 instance. You will be billed for the AWS resources used if you create a stack from this template.",
    "Parameters": [
        {
            "NoEcho": false,
            "Description": "Name of an existing EC2 KeyPair to enable SSH access to the instance",
            "ParameterKey": "KeyName"
        },
        {
            "DefaultValue": "0.0.0.0/0",
            "NoEcho": false,
            "Description": " The IP address range that can be used to SSH to the EC2 instances",
            "ParameterKey": "SSHLocation"
        },
        {
            "DefaultValue": "t2.medium",
            "NoEcho": false,
            "Description": "WebServer EC2 instance type",
            "ParameterKey": "InstanceType"
        }
    ]
}
{
    "StackId": "arn:aws:cloudformation:us-west-2:631542882297:stack/dsestack/a6772730-6a0b-11e6-ac3f-500c593b9a36"
}
```
Once the instance is running (which may take several minutes) you can ssh to its public ip and see that DSE is running.
```
$ ssh -i ~/.ssh/test-keypair.pem ubuntu@52.88.228.9
.......
ubuntu@ip-172-31-22-164:~$ cqlsh
Connected to Test Cluster at 127.0.0.1:9042.
[cqlsh 5.0.1 | Cassandra 3.0.7.1159 | DSE 5.0.1 | CQL spec 3.4.0 | Native protocol v4]
Use HELP for help.
cqlsh>

```
Tip: if you're changing the template and creating/destroying the instance you may need to delete the key's entry from *~/.ssh/known_hosts*

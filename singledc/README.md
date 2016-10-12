# Quick Start

This is an Amazon CloudFormation template that will deploy a single datacenter DataStax Enterprise cluster.

To run the template you will need to have the AWS CLI installed.  Instruction on that are available [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Documentation for the AWS CLI is [here](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cli.html).  To configure the AWS CLI run the command:

    aws configure

## Creating a Cluster

This part of the repo contains 2 files to spin up a DSE cluster: _deploy-dse.sh_ which references *cloudformation_dse.json* an AWS CloudFormation template which describes the architecture of the cluster. After installing the AWS CLI, you can spin up a cluster simply by calling:
```
collin@zazen:singledc$ ./deploy-dse.sh
No key-pair passed, generating key-pair...
Key saved to ~/.ssh/dse-key-us-west-1.pem
Using parameters:
email ->       donotreply@datastax.com
key ->         dse-keypair-us-west-1
vpc ->         vpc-e82f3a8d
size ->        4
dcname ->      dc0
instance ->    m4.large
sshlocation -> 0.0.0.0/0
region ->      us-west-1

Validating template...
{
    "StackId": "arn:aws:cloudformation:us-west-1:819041172558:stack/dse-stack/f1a2a160-867d-11e6-b821-500c2171ae8e"
}
```
When no arguments are passed the default values seen above are used. Note that all the default values are defined in the template except _region_ and _vpc_ which are AWS account defaults. Calling `deploy-dse.sh -h` prints a help message describing all the options the script understands:
```
---------------------------------------------------
Usage:
deploy-dse.sh [-h] [-e email] [-k keypair] [-v vpc] [-s size] [-d dcname]
              [-i instance] [-l sshlocation] [-r region]

Options:

 -h             : display this message and exit
 -e email       : email to send stack updates, default donotreply@datastax.com
 -k keypair     : keypair name, if not passed a new key named dse-keypair-$region
                  will be generated and saved to ~/.ssh
 -v vpc         : VPC, VPC to spin up cluster in, if not passed account default VPC used
 -s size        : cluster size (number of Cassandra nodes), if not passed template
                  default 4 (3+1 seed) used
 -d dcname      : datacenter name, default 'dc0'
 -i instance    : instance type, default m4.large
 -l sshlocation : CIDR block instances will accept ssh connections from, if not passed
                  template default 0.0.0.0/0 (everywhere) used
 -r region      : AWS region, if not passed account default used

---------------------------------------------------

```
After calling the script the cluster should spin up in about 15min. You can watch its progress from the web interface at  _CloudFormation -> Stack List -> Stack Detail: dse-stack_ or with some of the commands listed in the *Working with a Cluster* section. After the stack has completed in the _Outputs_ section there's a link to the OpsCenter web interface which will be something like `http://ec2-52-52-131-168.us-west-1.compute.amazonaws.com:8888/`. This URL can also be found by running `aws cloudformation describe-stacks`

## Notes and Caveats

- Currently these scripts have basic functionality and bugs certainly exist.
- Currently all instances use ephemeral storage.
- If not using the default _vpc_ it must be created **prior** to calling the script. This can be done by calling a command like the one below. The _--region_ argument is optional while _--cidr-block_ is manditory
```
aws ec2 create-vpc --region us-east-1 --cidr-block 10.0.0.0/16
```
- The _key-pair_ and _vpc_ used must be created in the region being used. The generated key-pair and default vpc satisfy this requirement.
- The template is currently only valid for the 3 US regions: _us-west-1 us-west-2 us-east-1_
- The instance type _t2.medium_ is included only for testing purposes and should not be used for a real cluster.
- This template uses an _AutoScalingGroup_ to bring up non-seed nodes. This group isn't intended to be dynamically scaled. While growing the size of this group most likely will work, shrinking it will have unknown side effects.

## Working with a Cluster
You can get information about a stack via the AWS web interface (go to _CloudFormation_ -> _Stack List_) or the CLI as described below.

You can get a list of existing stacks by running the command:

    aws cloudformation list-stacks

Log information is viewable by running the command:

    aws cloudformation describe-stack-events --stack-name myteststack

This command will give a list of resources in the stack:

    aws cloudformation list-stack-resources --stack-name myteststack

This command will delete the stack and the cluster contained in it:

    aws cloudformation delete-stack --stack-name myteststack

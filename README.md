# amazon-cloudformation-dse

These don't work yet.  Sorry.

This is an Amazon CloudFormation template that will deploy a single or multiple datacenter DataStax Enterprise cluster.  

To run the templates you will need to have the AWS CLI installed.  Instruction on that are available [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Documentation for the AWS CLI is [here](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cli.html).  To configure the AWS CLI run the command:

    aws configure

To ensure the template is valid you can run the command:

    aws cloudformation validate-template --template-body file://main.json

## Creating a Cluster

The [deploy.sh](./deploy.sh) script will deploy a cluster using the aws cli create stack command and this template.

## Working with a Cluster

You can get a list of existing stacks by running the command:

    aws cloudformation list-stacks

Log information is viewable by running the command:

    aws cloudformation describe-stack-events --stack-name myteststack

This command will give a list of resources in the stack:

    aws cloudformation list-stack-resources --stack-name myteststack

## Deleting a Cluster

This command will delete the stack and the cluster contained in it:

    aws cloudformation delete-stack --stack-name myteststack

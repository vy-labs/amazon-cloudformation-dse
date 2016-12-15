#!/bin/bash -e

dcname="dc-us-east"
region="us-east-1"

# Comment out/uncomment vvv to use a different key from opscenter
key=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`KeyName`].ParameterValue' --output text)
#key="dse-keypair-us-west-1"

cname=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`ClusterName`].ParameterValue' --output text)
pubkey=$(../util/getpubkey.sh)
stack="$dcname-stack"

echo "Using cluster name: $cname"
echo "Using public key: $pubkey"
echo "Using stack name: $stack"

aws cloudformation create-stack \
--region $region \
--stack-name $stack \
--template-body file://$(readlink -f cfn-datacenter-lcm.json) \
--parameters \
ParameterKey=KeyName,ParameterValue=$key \
ParameterKey=PublicKey,ParameterValue=$pubkey
ParameterKey=ClusterName,ParameterValue=$cname \
ParameterKey=OpsCenterPubIP,ParameterValue=$opscip \
ParameterKey=DataCenterName,ParameterValue=$dcname

#[PublicKey, ClusterName, OpsCenterPubIP, DataCenterName] must have values

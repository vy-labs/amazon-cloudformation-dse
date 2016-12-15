#!/bin/bash -e

#
# Changeable parameters
#
dcname="dc-us-east"
region="us-east-1"
dcsize=5

# Comment out/uncomment vvv to use a different key from opscenter,
# necessary when provisioning in a different region.
# Note! key and region must match
key=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`KeyName`].ParameterValue' --output text)
#key="dse-keypair-us-west-1"

opscip=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Outputs[] | [?OutputKey==`OpsCenterPublicIP`].OutputValue' --output text)
cname=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`ClusterName`].ParameterValue' --output text)
pubkey=$(../util/getpubkey.sh)
stack="$dcname-stack"

echo "Using opscenter ip: $opscip"
echo "Using cluster name: $cname"
echo "Using public key: $pubkey"
echo "Using stack name: $stack"
echo ""

aws cloudformation create-stack \
--region $region \
--stack-name $stack \
--template-body file://$(readlink -f cfn-datacenter-lcm.json) \
--parameters \
ParameterKey=KeyName,ParameterValue="$key" \
ParameterKey=PublicKey,ParameterValue="$pubkey" \
ParameterKey=ClusterName,ParameterValue="$cname" \
ParameterKey=OpsCenterPubIP,ParameterValue="$opscip" \
ParameterKey=DataCenterName,ParameterValue="$dcname" \
ParameterKey=DataCenterSize,ParameterValue=$dcsize

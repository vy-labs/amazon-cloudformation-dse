#!/bin/bash -e

# Changeable parameters
####################################################
dcname="dc-us-east"
region="us-east-1"
dcsize=5
instance="t2.medium"

# Comment out/uncomment vvv to use a different key from the opscenter stack,
# necessary when provisioning in a different region.
# Note! key and region must match
key=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`KeyName`].ParameterValue' --output text)
#key="dse-keypair-us-west-1"
####################################################

template="$PWD/cfn-datacenter-lcm.json"
opscip=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Outputs[] | [?OutputKey==`OpsCenterPublicIP`].OutputValue' --output text)
cname=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`ClusterName`].ParameterValue' --output text)
pubkey=$(../util/getpubkey.sh)
stack="$dcname-stack"

echo "Using opscenter ip: $opscip"
echo "Using cluster name: $cname"
echo "Using dcsize: $dcsize"
echo "Using public key: $pubkey"
echo "Using stack name: $stack"
echo "Using template: $template"
echo ""

aws cloudformation create-stack \
--region $region \
--stack-name $stack \
--template-body file://$template \
--parameters \
ParameterKey=KeyName,ParameterValue="$key" \
ParameterKey=PublicKey,ParameterValue="$pubkey" \
ParameterKey=ClusterName,ParameterValue="$cname" \
ParameterKey=OpsCenterPubIP,ParameterValue="$opscip" \
ParameterKey=DataCenterName,ParameterValue="$dcname" \
ParameterKey=DataCenterSize,ParameterValue=$dcsize \
ParameterKey=InstanceType,ParameterValue=$instance

echo "$stack $region" >> teardown.txt

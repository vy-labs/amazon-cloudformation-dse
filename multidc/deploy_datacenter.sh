#!/bin/bash -e

# Changeable parameters
####################################################
if [[ $1 = "spark" ]]; then
    dcname="dc-us-east-spark"
    region="us-east-1"
    dcsize=2
    instance="m4.2xlarge"
    spark=1
    volume=800
    instance_name="cassandra-spark"
else
    dcname="dc-us-east"
    region="us-east-1"
    dcsize=3
    instance="m4.xlarge"
    spark=0
    volume=800
    instance_name="cassandra"
fi

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
echo "Spark enabled:  $spark"
echo "Volume Size:  $volume"

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
ParameterKey=InstanceType,ParameterValue=$instance \
ParameterKey=Spark,ParameterValue=$spark \
ParameterKey=Volume,ParameterValue=$volume \
ParameterKey=InstanceName,ParameterValue=$instance_name

echo "$stack $region" >> teardown.txt

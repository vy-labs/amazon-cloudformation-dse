#!/bin/bash

# Changable parameters
####################################################
keyname="dse-keypair-us-east-1"
clustername="mycluster"
####################################################

template="$PWD/cfn-opscenter.json"
stack="opscenter-stack"
aws cloudformation create-stack \
--stack-name $stack \
--template-body file://$template \
--parameters \
ParameterKey=KeyName,ParameterValue=$keyname \
ParameterKey=ClusterName,ParameterValue=$clustername

region=$(aws configure get default.region)
echo "$stack $region" >> teardown.txt

#!/bin/bash

# Changable parameters
####################################################
keyname="dse-keypair-us-east-1"
clustername="mycluster"
####################################################

stack="opscenter-stack"
aws cloudformation create-stack \
--stack-name $stack \
--template-body file://$(readlink -f cfn-opscenter.json) \
--parameters \
ParameterKey=KeyName,ParameterValue=$keyname \
ParameterKey=ClusterName,ParameterValue=$clustername

region=$(aws configure get default.region)
echo "$stack $region" >> teardown.txt

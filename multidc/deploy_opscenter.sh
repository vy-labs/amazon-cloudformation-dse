#!/bin/bash

# Changable parameters
####################################################
keyname="aws-production-cassandra"
clustername="cassandra"
username="xxx"
password="xxx"
####################################################

template="$PWD/cfn-opscenter.json"
stack="opscenter-stack"
aws cloudformation create-stack \
--stack-name $stack \
--template-body file://$template \
--parameters \
ParameterKey=KeyName,ParameterValue=$keyname \
ParameterKey=ClusterName,ParameterValue=$clustername \
ParameterKey=Username,ParameterValue=$username \
ParameterKey=Password,ParameterValue=$password

region=$(aws configure get default.region)
echo "$stack $region" >> teardown.txt

#!/bin/bash

# Changable parameters
####################################################
keyname="vycapital-v3"
clustername="cassandra"
username="xxxxdseusernamexx"
password="xxxxdsepasswordxx"
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

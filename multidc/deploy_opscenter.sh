#!/bin/bash

# Changable parameters
keyname="dse-keypair-us-east-1"
clustername="mycluster"

aws cloudformation create-stack \
--stack-name opscenter-stack \
--template-body file://$(readlink -f cfn-opscenter.json) \
--parameters \
ParameterKey=KeyName,ParameterValue=$keyname \
ParameterKey=ClusterName,ParameterValue=$clustername

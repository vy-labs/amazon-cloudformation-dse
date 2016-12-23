#!/bin/bash

# Changable parameters
####################################################
keyname="dse-keypair-us-east-1"
clustername="mycluster"
####################################################

osxpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ "$(uname)" == "Darwin" ]; then
    echo "Running on MacOS..."
    operatingSystem="MacOS"
    template=$(osxpath "./findos.sh")
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "Running on Linux..."
    operatingSystem="Linux"
    template=$(readlink -e cfn-opscenter.json)
fi

stack="opscenter-stack"
aws cloudformation create-stack \
--stack-name $stack \
--template-body file://$template \
--parameters \
ParameterKey=KeyName,ParameterValue=$keyname \
ParameterKey=ClusterName,ParameterValue=$clustername \
ParameterKey=Secret,ParameterValue="mysecret"

region=$(aws configure get default.region)
echo "$stack $region" >> teardown.txt

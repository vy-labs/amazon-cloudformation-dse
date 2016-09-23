#!/bin/bash

# Usage: deploy-single.sh stack-name key-pair

aws cloudformation validate-template \
--template-body "$(cat ./onemachine.json)"

aws cloudformation create-stack \
--stack-name $1 \
--template-body "$(cat ./onemachine.json)" \
--parameters \
ParameterKey=KeyName,ParameterValue=$2

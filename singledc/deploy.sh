#!/bin/bash

aws cloudformation validate-template \
--template-body "$(cat ./onemachine.json)"

aws cloudformation create-stack \
--stack-name $1 \
--template-body "$(cat ./onemachine.json)" \
--parameters \
ParameterKey=KeyName,ParameterValue="dse_keypair"

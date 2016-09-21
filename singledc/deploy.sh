#!/bin/bash

aws cloudformation validate-template \
--template-body "$(cat ./cloudformation_dse_with_autoscale.json)"

aws cloudformation create-stack \
--stack-name $1 \
--template-body "$(cat ./cloudformation_dse_with_autoscale.json)" \
--parameters \
ParameterKey=KeyName,ParameterValue="jcp-keypair" \
ParameterKey=OperatorEMail,ParameterValue="collin.poczatek@datastax.com" \
ParameterKey=VpcId,ParameterValue="jcp-vpc"

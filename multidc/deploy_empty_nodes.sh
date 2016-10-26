#!/bin/bash

aws cloudformation create-stack \
--stack-name empty-stack \
--template-body file://$(readlink -f cfn-empty_dc.json) \
--parameters \
ParameterKey=KeyName,ParameterValue=dse-keypair-us-west-1

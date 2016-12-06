#!/bin/bash

aws cloudformation create-stack \
--stack-name opscenter-stack \
--template-body file://$(readlink -f cfn-opscenter.json) \
--parameters \
ParameterKey=KeyName,ParameterValue=dse-keypair-us-east-1

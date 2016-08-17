#!/bin/bash

aws cloudformation validate-template --template-body file://onemachine.json

KeyName=datastax
aws cloudformation create-stack --stack-name myteststack --template-body file://onemachine.json --parameters  ParameterKey=KeyName,ParameterValue=$KeyName

#!/bin/bash

STACK=$1

# This uses clusterParameters.json as input and writes output to generatedTemplate.json
python main.py

aws cloudformation validate-template --template-body file://generatedTemplate.json
# aws cloudformation create-stack --stack-name $STACK --template-body file://generatedTemplate.json
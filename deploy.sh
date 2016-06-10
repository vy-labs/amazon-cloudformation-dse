#!/bin/bash


# This uses clusterParameters.json as input and writes output to generatedTemplate.json
python main.py

aws cloudformation validate-template --template-body file://main.json
# aws cloudformation create-stack --stack-name myteststack --template-body file://main.json

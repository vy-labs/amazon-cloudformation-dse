#!/bin/bash

keyname=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Parameters[] | [?ParameterKey==`KeyName`].ParameterValue' --output text)
key=$HOME/.ssh/$keyname.pem
opscip=$(aws cloudformation describe-stacks --query 'Stacks[?StackName==`opscenter-stack`].Outputs[] | [?OutputKey==`OpsCenterPublicIP`].OutputValue' --output text)
ssh -o "StrictHostKeyChecking no" -i $key ubuntu@$opscip 'cat ~/.ssh/lcm.pem.pub'

#!/bin/bash

aws cloudformation create-stack \
--stack-name empty-stack \
--template-body file://$(readlink -f cfn-empty_dc.json) \
--parameters \
ParameterKey=KeyName,ParameterValue=dse-keypair-us-east-1 \
ParameterKey=PublicKey,ParameterValue="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDb1hhKRQFY6LIixGx+5fWBsDgjKutXpdhNVTbJ9nSmAvLZkUysesoAfJf17x9FadEJfUhMrk7MZCgXEUig1x6Hb+S0XLzU1i+4i6R2gAJq0NNMqlBmd0iMxsD3YFYOPvtz8VKwITkSBJjP7KC73tulFn4l749oBoiPyxwjTsVTxuQhiQoRM/L5QzPZIwRy12va47MMjLCqXA5/1Wbc6r7ZLR4inqRPBbIYVd1ycp7OLTs0ERymGiOoJviwzmDy5mvtWiJcke5LmKREof8WA0A49hitlbXXm/iopBGBiGqfl5yreVOsXdH2wj5o30WnG237nHd0Jlwq3XX38qur5zbz root@ip-172-31-54-44" \
ParameterKey=ClusterName,ParameterValue=testcluster \
ParameterKey=OpsCenterPubIP,ParameterValue=34.193.85.2 \
ParameterKey=DataCenterName,ParameterValue=dc0

#[PublicKey, ClusterName, OpsCenterPubIP, DataCenterName] must have values

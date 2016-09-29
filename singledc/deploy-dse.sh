#!/bin/bash

# options defaults, validity check at template call by aws cli
#
email="donotreply@datastax.com" # a no-op
region=$(aws configure get region)
vpc=$(aws ec2 describe-vpcs --filter Name="isDefault",Values="true" --output text | cut -f7)
#^^^ default for account, use --query instead of cut?
size=3 # +1 seednode
dcname="dc0"
instance="m4.large"
sshlocation="0.0.0.0/0"

usage="---------------------------------------------------
Usage:
deploy-dse.sh [-h] [-e email] [-k keypair] [-v vpc] [-s size] [-d dcname]
              [-i instance] [-l sshlocation] [-r region]

Options:

 -h		: display this message and exit
 -e email	: email to send stack updates, default donotreply@datastax.com
 -k keypair	: keypair name, if not passed a new key named dse-keypair-\$region
		  will be generated and saved to ~/.ssh
 -v vpc		: VPC, VPC to spin up cluster in, if not passed account default VPC used
 -s size	: cluster size (number of Cassandra nodes), if not passed template
		  default 4 (3+1 seed) used
 -d dcname	: datacenter name, default 'dc0'
 -i instance	: instance type, default m4.large
 -l sshlocation	: CIDR block instances will accept ssh connections from, if not passed
		  template default 0.0.0.0/0 (everywhere) used
 -r region	: AWS region, if not passed account default used

---------------------------------------------------"

while getopts 'he:k:v:s:d:i:l:r:' opt; do
  case $opt in
    h) echo -e "$usage"
       exit 1
    ;;
    e) email="$OPTARG"
    ;;
    k) keypair="$OPTARG"
    ;;
    v) vpc="$OPTARG"
    ;;
    s) size="$OPTARG"
    ;;
    d) dcname="$OPTARG"
    ;;
    i) instance="$OPTARG"
    ;;
    l) sshlocation="$OPTARG"
    ;;
    r) region="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
        exit 1
    ;;
  esac
done

# Generate keypair for region
if [ -e ~/.ssh/dse-keypair-$region.pem ] && [ -z "$key" ]
then
  echo -e "Default key exists"
  key=dse-keypair-$region
elif [ -z "$key" ]
then
  echo "No key-pair passed, generating key-pair..."
  aws ec2 create-key-pair --region $region --key-name dse-keypair-$region --query 'KeyMaterial' --output text > ~/.ssh/dse-keypair-$region.pem
  if [ $? -gt 0 ]
  then
    echo "Key generation error. Exiting..."
  fi
  chmod 600 ~/.ssh/dse-keypair-$region.pem
  key=dse-keypair-$region
  echo "Key saved to ~/.ssh/dse-keypair-"$region".pem"
fi

# for info
echo -e "\nUsing parameters:"
echo -e "email ->\t" $email "\nkey ->\t\t" $key "\nvpc ->\t\t"  $vpc "\nsize ->\t\t" $(($size+1))
echo -e "dcname ->\t" $dcname "\ninstance ->\t" $instance
echo -e "sshlocation ->\t" $sshlocation "\nregion ->\t" $region "\n"

# validate template and exit on error
echo -e "Validating template..."

aws cloudformation validate-template \
--template-body "$(cat ./cloudformation_dse.json)" \
1>/dev/null

if [ $? -gt 0 ]
then
  echo -e "Template validation error. Exiting..."
fi

echo -e "Calling: aws cloudformation create-stack...\n"
# Actually call create-stack
# Note, we're passing all params, even if the same as the
# template defaults to avoid param checking logic
aws cloudformation create-stack \
--stack-name "dse-stack" \
--region $region \
--template-body "$(cat ./cloudformation_dse.json)" \
--parameters \
ParameterKey=KeyName,ParameterValue=$key \
ParameterKey=OperatorEMail,ParameterValue=$email \
ParameterKey=VpcId,ParameterValue=$vpc \
ParameterKey=ClusterSize,ParameterValue=$size \
ParameterKey=DataCenterName,ParameterValue=$dcname \
ParameterKey=InstanceType,ParameterValue=$instance \
ParameterKey=SSHLocation,ParameterValue=$sshlocation

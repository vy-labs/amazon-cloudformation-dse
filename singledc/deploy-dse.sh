#!/bin/bash

# options defaults, validity check at template call by aws cli
#
email="donotreply@datastax.com" # a no-op
region=$(aws configure get region)
key=dse-keypair-$region
vpc=$(aws ec2 describe-vpcs --filter Name="isDefault",Values="true" --output text | cut -f7)
#^^^ default for account, use --query instead of cut?
size=3 # +1 seednode
dcname="dc0"
instance="t2.medium"
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
 -i instance	: instance type, default XXX
 -l sshlocation	: CIDR block instances will accept ssh connections from, if not passed
		  template default 0.0.0.0/0 (everywhere) used
 -r region	: AWS region, if not passed account default used

---------------------------------------------------"

while getopts 'he:k:v:s:d:i:l:' opt; do
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
    ;;
  esac
done

# Generate keypair for region
if [ -z "$key" ]
then
  echo "No key-pair passed, generating key-pair..."
#  aws ec2 create-key-pair --key-name dse-key-$region --query 'KeyMaterial' --output text > ~/.ssh/dse-key-$region.pem
  echo "Key saved to ~/.ssh/dse-key-"$region".pem"
fi

# for debug
echo -e "Using parameters:"
echo -e "email ->\t" $email "\nkey ->\t\t" $key "\nvpc ->\t\t"  $vpc "\nsize ->\t\t" $(($size+1))
echo -e "dcname ->\t" $dcname "\ninstance ->\t" $instance
echo -e "sshlocation ->\t" $sshlocation "\nregion ->\t" $region "\n"



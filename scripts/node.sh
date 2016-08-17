#!/usr/bin/env bash

cloud_type="aws"
seed_node_dns_name="dc0vm0"
data_center_name=$1

echo "Configuring nodes with the settings:"
echo cloud_type $cloud_type
echo seed_node_dns_name $seed_node_dns_name
echo data_center_name $data_center_name

apt-get -y install unzip

wget https://github.com/DSPN/install-datastax-ubuntu/archive/5.0.1-4.zip
unzip 5.0.1-4.zip
cd install-datastax-ubuntu-5.0.1-4/bin

./dse.sh $cloud_type $seed_node_dns_name $data_center_name

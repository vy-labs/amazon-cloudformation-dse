#!/usr/bin/env bash

cloud_type="ec2"
seed_node_dns_name="dc0vm0"

echo "Configuring nodes with the settings:"
echo cloud_type $cloud_type
echo seed_node_dns_name $seed_node_dns_name

apt-get -y install unzip

wget https://github.com/DSPN/install-datastax-ubuntu/archive/5.0.1-4.zip
unzip 5.0.1-4.zip
cd install-datastax-ubuntu-5.0.1-4/bin

# Let's try from the repo head...
#sudo apt-get -y install unzip && \
#wget https://github.com/DSPN/install-datastax-ubuntu/archive/master.zip && \
#unzip master.zip && \
#cd install-datastax-ubuntu-master/bin/

./opscenter.sh $cloud_type $seed_node_dns_name

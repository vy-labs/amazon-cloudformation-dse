#!/bin/bash

cd ~ubuntu
cloud_type='aws'
sudo apt-get install -y unzip
wget https://github.com/DSPN/install-datastax-ubuntu/archive/master.zip
unzip master.zip

cd install-datastax-ubuntu-master/bin/
sudo ./os/install_java.sh
sudo ./opscenter/install.sh $cloud_type
sudo ./opscenter/start.sh

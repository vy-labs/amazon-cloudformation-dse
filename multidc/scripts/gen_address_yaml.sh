#!/bin/bash

privateip=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
publicip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)

echo -e "agent_rpc_interface: $privateip
agent_rpc_broadcast_address: $publicip
stomp_interface: $publicip
use_ssl: 0
"

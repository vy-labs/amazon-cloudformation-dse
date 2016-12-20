#!/bin/bash

privateip=$1
publicip=$2

echo -e "agent_rpc_interface: $privateip
agent_rpc_broadcast_address: $publicip
stomp_interface: $publicip
use_ssl: 0
"

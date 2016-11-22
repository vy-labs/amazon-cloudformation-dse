#!/bin/bash

OPSCIP=$1
echo "OpsCenter ip: $OPSCIP"
while true; do
  sleep 5;
  echo "curl http://$OPSCIP:8888/api/v1/lcm/ ...";
  curl -s -I -m 2 http://$OPSCIP:8888/api/v1/lcm/ 2>&1 | tee watchforopsc.txt;
done

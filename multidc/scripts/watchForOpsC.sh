#!/bin/bash

OPSCIP='107.23.208.9'

while true; do
  sleep 5;
  echo "curl opsc -----------------------------";
  curl -s -I -m 2 http://$OPSCIP:8888/api/v1/lcm/ 2>&1 | tee watchforlcm.txt;
done

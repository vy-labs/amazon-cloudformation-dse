#!/bin/bash
set -euo pipefail

count=0

while read line
do
    stack=$(echo "$line" | cut -d " " -f 1)
    region=$(echo "$line" | cut -d " " -f 2)
    echo -e "deleting stack: $stack \t $region ..."
    aws cloudformation delete-stack --stack-name $stack --region $region
    count=$(($count+1))
done < teardown.txt

echo "Stacks deleted: $count"
rm teardown.txt

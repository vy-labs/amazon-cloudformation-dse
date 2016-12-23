#!/bin/bash


echo "Replacing 'master' -> 'dev'"
for var in "$@"
do
  echo -e "$var ... "
  sed -i 's/master/dev/g' $var
done

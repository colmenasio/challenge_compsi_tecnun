#!/bin/bash

total=0

for id in $(seq 2006901 2006907);
do
	for file in ${1}/20*.csv;
	do
		total=$(($(cat $file | grep -i "${id}" | wc -l) + $total))
	done
done
echo $total


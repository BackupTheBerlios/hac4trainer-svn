#!/bin/bash

for unittest in `ls *Test.py`; do
	echo
	echo "****"
	echo "running $unittest";
	echo
	python $unittest;
done

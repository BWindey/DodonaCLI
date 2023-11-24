#!/bin/bash

if [[ $SHELL =~ "bash" ]]; then
	echo "source $(realpath completion_script.sh)" >> ~/.bashrc
	source completion_script.sh
	pip install -r requirements.txt
else
	echo "not bash =("
fi

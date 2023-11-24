#!/bin/bash

if [[ $SHELL =~ "bash" ]]; then
	pip install -r requirements.txt
	chmod u+x main.py
	echo "alias dodona=python3 $(realpath main.py) $*" >> ~/.bashrc
	echo "source $(realpath completion_script.sh)" >> ~/.bashrc
	source "${HOME}/.bashrc"
else
	echo "Script only works for bash for now, see the README.md for other platforms"
fi

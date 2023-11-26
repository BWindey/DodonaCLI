#!/bin/bash

if [[ $SHELL =~ "bash" ]]; then
	pip install -r requirements.txt
	chmod u+x main.py
	echo "alias dodona=python3 $(realpath main.py) $*" >> ~/.bashrc
	echo "source $(realpath completion_script.sh)" >> ~/.bashrc
	source "${HOME}/.bashrc"

elif [[ $SHELL =~ "zsh" ]]; then
	pip install -r requirements.txt
	chmod u+x main.py
	echo "alias dodona=python3 $(realpath main.py) $*" >> ~/.zshrc
	echo "source $(realpath completion_script.sh)" >> ~/.zshrc
	source "${HOME}/.zshrc"

else
	echo "Script only works for bash and zsh for now, see the README.md for other platforms"
fi

#!/bin/bash

directory=$(realpath $(dirname "$0")) 

# Create a python virtual environment and install the packages.
rm -rf "$directory/.venv"
python3 -m venv "$directory/.venv"
# Activate the virtual environment
source "$directory/.venv/bin/activate"

# Check if pip is installed, if not, install it
if ! "$directory"/.venv/bin/python3 -m pip --version; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    "$directory"/.venv/bin/python3 get-pip.py
    rm get-pip.py
fi


"$directory"/.venv/bin/python3 -m pip install "$directory/risk-shared" "$directory/risk-helper" "$directory/risk-engine"
#!/bin/sh

# Abort the script if any command fails
set -e

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -U coveralls && coveralls

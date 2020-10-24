#!/bin/sh

# Abort the script if any command fails
set -e

virtualenv .venv
source .venv/bin/activate
python -m pip install -U docker-compose

docker-compose build

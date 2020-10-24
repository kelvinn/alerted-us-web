#!/bin/sh

# Abort the script if any command fails
set -e

virtualenv ~/venv
source ~/venv/bin/activate
pip install -U docker-compose

docker-compose stop && docker-compose rm -f

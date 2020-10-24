#!/bin/bash

# Abort the script if any command fails
set -e

# Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install coveralls and report
python -m pip install -U coveralls && coveralls

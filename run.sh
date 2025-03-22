#!/bin/bash

# Install required packages
pip install -r requirements.txt

# Load environment variables from edge.env file
if [ -f edge.env ]; then
  set -o allexport
  source edge.env
  set +o allexport
fi

# Set the PYTHONPATH to the project's root directory
export PYTHONPATH=$(pwd)

# Run the Python application
python Controllers/Main.py
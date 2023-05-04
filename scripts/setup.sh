#!/bin/bash

if [ ! -d ~/env ]; then
  # Create Python virtual environment if it does not exist 
  python -m venv env
  
  # Activate the Python virtual environment 
  source env/bin/activate
  
  # Install the requirements of the project if not installed
  python -m pip install -r requirements.txt
fi

exit 0

#!/bin/bash
# Create a new virtual environment 
python -m venv venv
# Activate virtual environment
source /path/to/virtualenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000

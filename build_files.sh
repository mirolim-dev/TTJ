#!/bin/bash

echo "BUILD START"

# Install Python dependencies
python3.12 -m pip install -r requirements.txt

# Run collectstatic
python3.12 manage.py collectstatic

echo "BUILD END"

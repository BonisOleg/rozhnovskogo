#!/usr/bin/env bash
# exit on error
set -o errexit

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

chmod +x start.sh

python3 manage.py collectstatic --no-input
python3 manage.py migrate

# Note: Run 'python3 manage.py seed' manually via SSH or Render Shell for initial data population.
# Do not run it automatically here to avoid resetting data on every deploy.

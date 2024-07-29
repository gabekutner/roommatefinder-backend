#!/bin/bash

# Date: 07/28/2024
# Author: Gabe Kutner
# This script intializes the development environment for the roommatefinder-backend repository.
# https://github.com/gabekutner/roommatefinder-backend.git
#
# This script requires the jq runtime dependency : https://jqlang.github.io/jq/download/

# Usage: $ bash commands/dev-init.sh "<database>" "<email>" "<email-passphrase>"
## NOTE: For development, I use the same string - "postgres" - for DATABASE_NAME, DATABASE_USER AND DATABASE_PASSWORD

# Check parameters
if [ "$#" -ne 3 ]; then
    echo "$ bash commands/dev-init.sh <database> <email> <email-passphrase>"
    exit 1
fi

# Add python3 to your development path
PYTHON3PATH=$(which python3) 
PATH+=:PYTHON3PATH

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "python3 could not be found. Please install Python 3."
    exit 1
fi

# Initialize script variables
# Generate a secret key for Django settings
SECRETKEY=$(python3 -c 'import random; result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]); print(result)')
PROJECTPATH="./src/roommatefinder"

# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Download development requirements
python3 -m pip install -r "${PROJECTPATH}/requirements/_base.txt"

# Write the sample_secrets.json file
jq -n --arg secret_key "$SECRETKEY" \
      --arg database_name $1 \
      --arg database_user $1 \
      --arg database_password $1 \
      --arg database_host "localhost" \
      --argjson database_port 5432 \
      --arg email_host "smtp.gmail.com" \
      --arg email_port 587 \
      --arg email_host_user $2 \
      --arg email_host_password $3 \
'{
  SECRET_KEY: $secret_key,
  DATABASE_NAME: $database_name,
  DATABASE_USER: $database_user,
  DATABASE_PASSWORD: $database_password,
  DATABASE_HOST: $database_host,
  DATABASE_PORT: $database_port,
  EMAIL_HOST: $email_host,
  EMAIL_PORT: $email_port,
  EMAIL_HOST_USER: $email_host_user,
  EMAIL_HOST_PASSWORD: $email_host_password
}' > "${PROJECTPATH}/roommatefinder/settings/sample_secrets.json"
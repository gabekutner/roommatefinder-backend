#!/bin/bash

# Date: 07/28/2024
# Author: Gabe Kutner
# This script intializes the development environment for the roommatefinder-backend repository.
# https://github.com/gabekutner/roommatefinder-backend.git
#
# This script requires the jq runtime dependency : https://jqlang.github.io/jq/download/

# Usage: $ bash commands/dev-init.sh "<email>" "<passphrase-1>" "<passphrase-2>" "<passphrase-3>" "<passphrase-4>" "<database>"
## NOTE: For development, I use the same string - "postgres" - for DATABASE_NAME, DATABASE_USER AND DATABASE_PASSWORD

# Check parameters
if [ "$#" -ne 6 ]; then
    echo "$ bash commands/dev-init.sh <email> <passphrase-1> <passphrase-2> <passphrase-3> <passphrase-4> <database>"
    echo "## Passphrases for email app passwords are 4 letters long. Enter them after the associated email. "
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

# Log
echo "🥽 Created venv"

# Download development requirements
python3 -m pip install -r "${PROJECTPATH}/requirements/dev.txt"

# Log
echo "🐍 Installed project dependencies"

# Write the sample_secrets.json file
jq -n --arg secret_key "$SECRETKEY" \
      --arg database_name $6 \
      --arg database_user $6 \
      --arg database_password $6 \
      --arg database_host "localhost" \
      --argjson database_port 5432 \
      --arg email_host "smtp.gmail.com" \
      --arg email_port 587 \
      --arg email_host_user $1 \
      --arg email_host_password "$2 $3 $4 $5" \
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

# Log
echo "🔑 Created secrets file"
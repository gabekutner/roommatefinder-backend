#!/usr/bin/env bash

# Create a secret key
SECRETKEY=$(python3 -c 'import random; result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]); print(result)')

# Write the sample_secrets.json file
jq -n --arg secret_key "$SECRETKEY" \
      --arg database_name postgres \
      --arg database_user postgres \
      --arg database_password postgres \
      --arg database_host "localhost" \
      --argjson database_port 5432 \
      --arg email_host "smtp.gmail.com" \
      --arg email_port 587 \
      --arg email_host_user example@gmail.com \
      --arg email_host_password "123 123 123 123" \
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
}' > "src/roommatefinder/roommatefinder/settings/sample_secrets.json"
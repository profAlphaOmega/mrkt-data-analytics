#!/bin/sh

function KmsDecrypt() {
  local KEYRING="redacted"
  local KEY="redacted"

  local CIPHERTEXT="${1}"
  local PLAINTEXT=$(echo ${CIPHERTEXT} | \
    gcloud kms decrypt \
      --ciphertext-file=- \
      --plaintext-file=- \
      --keyring ${KEYRING} \
      --key ${KEY} \
      --location global
    )

  echo "${PLAINTEXT}"
}

# Get configs
ENV=${ENV:-"dev"}
cd conf
source ./base.env
cd -
echo "Env variables:"
env | sort

# Start flask web application
twistd -n web --wsgi src.main.app --port tcp:8080
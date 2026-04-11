#!/bin/sh
set -eu

ENDPOINT="http://object-storage-server:9000"
ACCESS_KEY="minioadmin"
SECRET_KEY="minioadmin"
ALIAS="local"

echo "Waiting for MinIO at ${ENDPOINT}..."
until mc alias set "${ALIAS}" "${ENDPOINT}" "${ACCESS_KEY}" "${SECRET_KEY}" >/dev/null 2>&1; do
  sleep 2
done

echo "Creating buckets..."
mc mb --ignore-existing "${ALIAS}/profile-pics"
mc mb --ignore-existing "${ALIAS}/documents"

echo "Uploading seed files..."
mc rm --force --recursive "${ALIAS}/profile-pics/avatar.jpg" >/dev/null 2>&1 || true
mc rm --force --recursive "${ALIAS}/documents/report.pdf" >/dev/null 2>&1 || true
mc cp /seed/avatar.jpg "${ALIAS}/profile-pics/avatar.jpg"
mc cp /seed/report.pdf "${ALIAS}/documents/report.pdf"

echo "Setting public download policy for profile-pics..."
mc anonymous set download "${ALIAS}/profile-pics"

echo "MinIO bootstrap completed successfully."
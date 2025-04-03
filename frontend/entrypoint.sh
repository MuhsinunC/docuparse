#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Frontend Entrypoint: Activating Conda environment 'docuparse-frontend' ---"
# Activate Conda environment
# Using source /opt/conda/etc/profile.d/conda.sh first ensures conda command is available
source /opt/conda/etc/profile.d/conda.sh
conda activate docuparse-frontend # Ensure this matches the name in frontend/conda.yml

echo "--- Frontend Entrypoint: Executing command: $@ ---"
# Execute the command passed as arguments (from CMD)
exec "$@" 
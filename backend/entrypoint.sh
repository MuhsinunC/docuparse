#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Entrypoint: Activating Conda environment 'docuparse-backend' ---"
# Activate Conda environment
# Using source /opt/conda/etc/profile.d/conda.sh first ensures conda command is available
source /opt/conda/etc/profile.d/conda.sh
conda activate docuparse-backend

echo "--- Entrypoint: Executing command: $@ ---"
# Execute the command passed as arguments (from CMD)
exec "$@"
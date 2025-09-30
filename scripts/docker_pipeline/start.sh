#!/bin/bash

echo "Starting ASI Ecosystem Pipeline Container"
echo "=========================================="

# Run the main pipeline
python run_ecosystem_pipeline.py

# Keep container running
echo "Pipeline execution completed. Container remains active for inspection."
echo "Use 'docker exec -it <container-name> bash' to access the container."
echo "Output files available in /app/output/"

# Keep container alive
tail -f /dev/null

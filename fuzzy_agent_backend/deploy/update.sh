#!/bin/bash
# Pull latest code from GitHub and restart backend (no manual python app.py needed).
# Run on GCP VM whenever you push new code to GitHub.
#
# Usage: bash update.sh

set -euo pipefail

INSTALL_DIR="${INSTALL_DIR:-$HOME/fuzzy}"
BACKEND_DIR="$INSTALL_DIR/fuzzy_agent_backend/backend"
SERVICE_NAME="fuzzy-api"

echo "==> Pulling latest from GitHub..."
cd "$INSTALL_DIR"
git pull

echo "==> Updating Python dependencies..."
cd "$BACKEND_DIR"
source venv/bin/activate
pip install -r requirements.txt

echo "==> Restarting service..."
sudo systemctl restart "${SERVICE_NAME}"

echo "==> Health check..."
sleep 2
curl -s http://localhost:5000/api/health
echo ""
echo "Done! Backend updated and running."

#!/bin/bash
# Pull latest code and restart backend.
# Run from: ~/Fuzzy_sets/fuzzy_agent_backend/deploy
#   bash update.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_INSTALL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
BACKEND_DIR="$INSTALL_DIR/fuzzy_agent_backend/backend"
SERVICE_NAME="fuzzy-api"

echo "==> Using repo at: $INSTALL_DIR"
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

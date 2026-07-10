#!/bin/bash
# One-time GCP VM setup: auto-start backend on boot.
# Run from anywhere inside the cloned repo:
#   cd ~/Fuzzy_sets/fuzzy_agent_backend/deploy
#   bash setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# deploy/ -> fuzzy_agent_backend/ -> repo root (Fuzzy_sets, fuzzy, etc.)
DEFAULT_INSTALL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

GITHUB_REPO="${GITHUB_REPO:-}"
INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
BACKEND_DIR="$INSTALL_DIR/fuzzy_agent_backend/backend"
SERVICE_NAME="fuzzy-api"
OLLAMA_MODEL="${OLLAMA_MODEL:-phi3}"
USERNAME="$(whoami)"

echo "==> Using repo at: $INSTALL_DIR"

if [ ! -d "$INSTALL_DIR/.git" ] && [ -z "$GITHUB_REPO" ]; then
  echo "ERROR: No git repo found at $INSTALL_DIR"
  echo "Clone first: git clone https://github.com/ddevguru/Fuzzy_sets.git ~/Fuzzy_sets"
  exit 1
fi

echo "==> Installing system packages..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

echo "==> Updating repository..."
if [ -d "$INSTALL_DIR/.git" ]; then
  cd "$INSTALL_DIR"
  git pull || true
elif [ -n "$GITHUB_REPO" ]; then
  git clone "$GITHUB_REPO" "$INSTALL_DIR"
fi

if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
  echo "ERROR: Backend not found at $BACKEND_DIR"
  exit 1
fi

echo "==> Creating Python virtualenv..."
cd "$BACKEND_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Installing systemd service (auto-start on boot)..."
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null <<EOF
[Unit]
Description=Fuzzy Logic Voice Tutor API
After=network.target

[Service]
User=${USERNAME}
WorkingDirectory=${BACKEND_DIR}
Environment="PATH=${BACKEND_DIR}/venv/bin"
Environment="PORT=5000"
Environment="OLLAMA_HOST=http://localhost:11434"
Environment="OLLAMA_MODEL=${OLLAMA_MODEL}"
ExecStart=${BACKEND_DIR}/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl restart "${SERVICE_NAME}"

echo ""
echo "============================================"
echo "  Setup complete!"
echo "  Repo:    $INSTALL_DIR"
echo "  Service: ${SERVICE_NAME}"
echo "  Status:  sudo systemctl status ${SERVICE_NAME}"
echo "  Logs:    sudo journalctl -u ${SERVICE_NAME} -f"
echo "  Health:  curl http://localhost:5000/api/health"
echo "  Public:  curl http://35.234.218.138:5000/api/health"
echo "============================================"
sudo systemctl status "${SERVICE_NAME}" --no-pager || true

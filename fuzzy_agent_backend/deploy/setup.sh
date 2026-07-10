#!/bin/bash
# One-time GCP VM setup: clone from GitHub (SSH) + auto-start backend on boot.
# Run on Ubuntu VM after: git clone ... OR curl this script from repo.
#
# Usage:
#   export GITHUB_REPO="git@github.com:YOUR_USER/fuzzy.git"
#   bash setup.sh

set -euo pipefail

GITHUB_REPO="${GITHUB_REPO:-}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/fuzzy}"
BACKEND_DIR="$INSTALL_DIR/fuzzy_agent_backend/backend"
SERVICE_NAME="fuzzy-api"
USERNAME="$(whoami)"

if [ ! -d "$INSTALL_DIR/.git" ] && [ -z "$GITHUB_REPO" ]; then
  echo "ERROR: Set GITHUB_REPO or clone the repo to $INSTALL_DIR first."
  echo '  export GITHUB_REPO="git@github.com:YOUR_USER/fuzzy.git"'
  exit 1
fi

echo "==> Installing system packages..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

echo "==> Cloning or updating repository..."
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "Repo already at $INSTALL_DIR — pulling latest..."
  cd "$INSTALL_DIR"
  git pull
elif [ -n "$GITHUB_REPO" ]; then
  git clone "$GITHUB_REPO" "$INSTALL_DIR"
else
  echo "ERROR: No repo at $INSTALL_DIR"
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
echo "  Service: ${SERVICE_NAME}"
echo "  Status:  sudo systemctl status ${SERVICE_NAME}"
echo "  Logs:    sudo journalctl -u ${SERVICE_NAME} -f"
echo "  Health:  curl http://localhost:5000/api/health"
echo "============================================"
sudo systemctl status "${SERVICE_NAME}" --no-pager || true

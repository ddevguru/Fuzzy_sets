#!/bin/bash
# Install Ollama on GCP VM + auto-start on boot (systemd).
# Run once on VM: bash install_ollama.sh
#
# e2-micro (1 GB RAM) ke liye chhota model use karo: phi3 ya tinyllama

set -euo pipefail

OLLAMA_MODEL="${OLLAMA_MODEL:-phi3}"

echo "==> Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "==> Enabling Ollama service (auto-start on boot)..."
sudo systemctl enable ollama
sudo systemctl start ollama

echo "==> Waiting for Ollama to start..."
sleep 5

echo "==> Pulling model: ${OLLAMA_MODEL} (yeh 2-5 min le sakta hai)..."
ollama pull "${OLLAMA_MODEL}"

echo "==> Testing Ollama..."
curl -s http://localhost:11434/api/tags | head -c 200
echo ""

echo ""
echo "============================================"
echo "  Ollama ready!"
echo "  Model:   ${OLLAMA_MODEL}"
echo "  Status:  sudo systemctl status ollama"
echo "  Logs:    sudo journalctl -u ollama -f"
echo ""
echo "  Backend service mein yeh env vars set karo:"
echo "    OLLAMA_HOST=http://localhost:11434"
echo "    OLLAMA_MODEL=${OLLAMA_MODEL}"
echo "============================================"

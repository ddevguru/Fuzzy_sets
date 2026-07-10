# Google Cloud Deploy — GitHub SSH + Auto-Start Backend

Backend **ek baar setup** karo — uske baad VM restart par bhi automatically chalega.  
Code update ke liye sirf `git pull` + `update.sh` chalao, `python app.py` manually nahi.

## Tumhari GCP VM (current)

| Field | Value |
|-------|-------|
| Instance | `instance-20260710-132743` |
| Zone | `asia-south1-a` |
| External IP | **`35.234.218.138`** |
| Internal IP | `10.160.0.2` |
| Backend URL | `http://35.234.218.138:5000` |
| Ollama (VM par local) | `http://localhost:11434` |

Flutter app mein IP already set hai: `api_service.dart` → `http://35.234.218.138:5000`

---

## Part A — GitHub par code daalo (ek baar, apne PC par)

### A1. GitHub par naya repo banao

1. [github.com/new](https://github.com/new) kholo
2. Repository name: `fuzzy` (ya jo naam chaho)
3. **Private** ya Public — apni marzi
4. README / .gitignore mat add karo (humare paas already hai)
5. **Create repository**

### A2. SSH key setup (agar pehle se nahi hai)

**Windows PowerShell:**

```powershell
# SSH key banao (Enter dabate raho)
ssh-keygen -t ed25519 -C "your-email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_github

# Public key copy karo
Get-Content $env:USERPROFILE\.ssh\id_ed25519_github.pub
```

GitHub → **Settings → SSH and GPG keys → New SSH key** → paste karo.

SSH config (optional, agar default key alag ho):

```
# C:\Users\YOUR_USER\.ssh\config
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
```

Test:
```powershell
ssh -T git@github.com
# "Hi username! You've successfully authenticated..." aana chahiye
```

### A3. Local repo se GitHub par push karo

```powershell
cd c:\fuzzy

git init
git add .
git commit -m "Fuzzy logic voice tutor — Flutter app + Flask backend"

# Apna GitHub username/repo naam badlo:
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/fuzzy.git
git branch -M main
git push -u origin main
```

---

## Part B — GCP VM par GitHub se fetch + auto-start (ek baar)

### B1. GCP project (tumne already bana liya)

Console: [console.cloud.google.com](https://console.cloud.google.com)

### B2. VM banao

| Setting | Value |
|---------|-------|
| Name | `fuzzy-backend` |
| Region | `asia-south1` (Mumbai) |
| Machine | `e2-micro` |
| OS | Ubuntu 22.04 LTS |
| Firewall | HTTP + HTTPS tick |

### B3. Firewall — port 5000

**VPC network → Firewall → Create rule**

- Name: `allow-fuzzy-api`
- Ingress, targets: All instances
- Source: `0.0.0.0/0`
- Protocol: `tcp:5000`

### B4. VM par SSH karo

```bash
gcloud compute ssh fuzzy-backend --zone=asia-south1-a
```

### B5. VM par GitHub SSH key add karo

VM ke andar:

```bash
ssh-keygen -t ed25519 -C "gcp-fuzzy-vm" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
```

Output copy karo → GitHub → **Repo → Settings → Deploy keys → Add deploy key**  
Title: `gcp-fuzzy-vm`, key paste, **read-only** tick (write ki zaroorat nahi).

VM par test:
```bash
ssh -T git@github.com
```

### B6. Ek command se poora setup (clone + venv + systemd auto-start)

```bash
export GITHUB_REPO="git@github.com:YOUR_GITHUB_USERNAME/fuzzy.git"
git clone "$GITHUB_REPO" ~/fuzzy
cd ~/fuzzy/fuzzy_agent_backend/deploy
chmod +x setup.sh update.sh
export GITHUB_REPO="git@github.com:YOUR_GITHUB_USERNAME/fuzzy.git"
bash setup.sh
```

`setup.sh` yeh karta hai:
- GitHub se repo clone/pull
- Python venv + `pip install`
- **systemd service** install — VM boot par backend khud start
- Crash par bhi auto-restart (`Restart=always`)

### B7. Verify

```bash
# Service chal rahi hai?
sudo systemctl status fuzzy-api

# Health check
curl http://localhost:5000/api/health
# {"status":"ok"}

# Bahar se (apne PC se) — VM ka External IP use karo
curl http://YOUR_VM_EXTERNAL_IP:5000/api/health
```

**Ab `python app.py` manually chalane ki zaroorat nahi.**  
Service hamesha background mein chalegi.

---

## Part C — Code update (jab bhi GitHub par push karo)

**Apne PC par:**
```powershell
cd c:\fuzzy
git add .
git commit -m "your changes"
git push
```

**GCP VM par (SSH):**
```bash
cd ~/fuzzy/fuzzy_agent_backend/deploy
bash update.sh
```

Bas — pull, dependencies update, service restart. Manual backend run nahi.

---

## Part D — Flutter app (already configured)

File: `fuzzy_agent_flutter/fuzzy_app_agent/lib/services/api_service.dart`

```dart
static const String baseUrl = "http://35.234.218.138:5000";
```

APK build:
```powershell
cd c:\fuzzy\fuzzy_agent_flutter\fuzzy_app_agent
flutter pub get
flutter build apk --release
```

APK path: `build/app/outputs/flutter-apk/app-release.apk`

---

## Part E — Ollama GCP par (auto-start, manually run nahi)

Ollama sirf **natural narration** ke liye hai — fuzzy math Python mein hoti hai.  
Bina Ollama ke bhi app chalega (fixed text fallback).

### E1. VM par SSH

```bash
gcloud compute ssh instance-20260710-132743 --zone=asia-south1-a
```

### E2. Ollama install + auto-start (ek baar)

```bash
cd ~/fuzzy/fuzzy_agent_backend/deploy
chmod +x install_ollama.sh
bash install_ollama.sh
```

Yeh script:
- Ollama install karta hai
- `systemctl enable ollama` — **boot par auto-start**
- `phi3` model pull karta hai (e2-micro 1GB RAM ke liye safe; `llama3.2` se chhota)

Agar model badalna ho:
```bash
export OLLAMA_MODEL=llama3.2
bash install_ollama.sh
```

### E3. Backend ko Ollama se connect karo

`setup.sh` already yeh env vars set karta hai:
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3
```

Agar backend pehle se chal raha hai, restart karo:
```bash
sudo systemctl restart fuzzy-api
```

### E4. Verify Ollama

```bash
sudo systemctl status ollama
curl http://localhost:11434/api/tags
ollama run phi3 "Hello"
```

### Ollama commands

| Kaam | Command |
|------|---------|
| Status | `sudo systemctl status ollama` |
| Restart | `sudo systemctl restart ollama` |
| Logs | `sudo journalctl -u ollama -f` |
| Models list | `ollama list` |
| Naya model | `ollama pull phi3` |

**Note:** Ollama port 11434 bahar expose karne ki zaroorat **nahi** — sirf backend localhost se use karta hai.

---

## Useful commands (GCP VM par)

| Kaam | Command |
|------|---------|
| Status dekho | `sudo systemctl status fuzzy-api` |
| Restart | `sudo systemctl restart fuzzy-api` |
| Stop | `sudo systemctl stop fuzzy-api` |
| Start | `sudo systemctl start fuzzy-api` |
| Live logs | `sudo journalctl -u fuzzy-api -f` |
| Boot par auto? | `sudo systemctl is-enabled fuzzy-api` → `enabled` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `git@github.com: Permission denied` | VM par deploy key add kiya? `ssh -T git@github.com` test karo |
| Backend band ho jata hai | `sudo systemctl status fuzzy-api` — logs mein error dekho |
| VM restart ke baad down | `sudo systemctl enable fuzzy-api` dubara chalao |
| Port 5000 bahar se nahi khulta | GCP firewall rule `allow-fuzzy-api` tcp:5000 check karo |
| Flutter "Could not reach backend" | Phone par internet on? IP `35.234.218.138:5000` test: browser mein `http://35.234.218.138:5000/api/health` |
| Ollama slow / crash | e2-micro par `phi3` use karo, `llama3.2` se avoid karo (RAM kam) |
| Ollama optional | Bina Ollama ke bhi sab kaam karega — narration fixed text se aayegi |
| Code update ke baad purana behavior | VM par `bash update.sh` chalao |

---

## Quick checklist

- [ ] GitHub repo bana + SSH key + `git push`
- [ ] GCP VM + firewall port 5000
- [ ] VM par GitHub deploy key
- [ ] `bash setup.sh` — systemd enabled
- [ ] `curl http://35.234.218.138:5000/api/health` → ok
- [ ] Flutter APK build + phone par install
- [ ] (Optional) `bash install_ollama.sh` — narration ke liye

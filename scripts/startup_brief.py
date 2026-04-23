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
from email.utils import parsedate_to_datetime
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
# Exchange settings now come exclusively from Neon app_settings; do not decrypt legacy exchange.env.
GMAIL_ICAL_ENV = decrypt_env_if_needed(GMAIL_ICAL_ENV, _decrypt_dir)

load_env(GMAIL_IMAP_ENV)
load_env(EXCHANGE_ENV)
load_env(GMAIL_ICAL_ENV)
# Prefer the verified local Gmail overrides over any values that may come from decrypted envs.
for k in ('GMAIL1_EMAIL', 'GMAIL1_APP_PASSWORD', 'GMAIL2_EMAIL', 'GMAIL2_APP_PASSWORD', 'GMAIL1_ICAL_URL', 'GMAIL2_ICAL_URL'):
    if os.getenv(f'STARTUP_BRIEF_{k}'):
        os.environ[k] = os.getenv(f'STARTUP_BRIEF_{k}')




def db_query_app_settings():
    key_file = Path(os.getenv('NEON_KEY_FILE', str(DEFAULT_NEON_KEY_FILE)))
    if not key_file.exists():
        alt = Path('/home/george/.openclaw/workspace/secrets/Neon_Key.txt')
        if alt.exists():
            key_file = alt
        else:
            raise RuntimeError(f'Neon key file not found: {key_file}')
    raw = key_file.read_text().strip()
    if raw.startswith('psql '):
        raw = raw[5:].strip().strip("'\"")
    sql = "select key, value from app_settings order by key"
    result = subprocess.run(['psql', raw, '-At', '-F', '	', '-c', sql], capture_output=True, text=True, check=True)
    rows = []
    for line in result.stdout.splitlines():
        if '	' not in line:
            continue
        k, v = line.split('	', 1)
        rows.append((k, v))
    return rows

def load_db_settings():
    key_file = Path(os.getenv('NEON_KEY_FILE', str(DEFAULT_NEON_KEY_FILE)))
    if not key_file.exists():
        alt = Path('/home/george/.openclaw/workspace/secrets/Neon_Key.txt')
        if alt.exists():
            key_file = alt
        else:
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
for k in ('gmail1_ical_url', 'gmail2_ical_url', 'exchange_tenant_id', 'exchange_client_id', 'exchange_client_secret', 'exchange_mailbox_email'):
    env_key = k.upper()
    if _db_settings.get(k):
        os.environ[env_key] = _db_settings[k]
# Back-compat aliases used by this script.
if os.getenv('EXCHANGE_TENANT_ID'):
    os.environ['TENANT_ID'] = os.environ['EXCHANGE_TENANT_ID']
if os.getenv('EXCHANGE_CLIENT_ID'):
    os.environ['CLIENT_ID'] = os.environ['EXCHANGE_CLIENT_ID']
if os.getenv('EXCHANGE_CLIENT_SECRET'):
    os.environ['CLIENT_SECRET'] = os.environ['EXCHANGE_CLIENT_SECRET']
if os.getenv('EXCHANGE_MAILBOX_EMAIL'):
    os.environ['MAILBOX_EMAIL'] = os.environ['EXCHANGE_MAILBOX_EMAIL']

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


def gmail_unread(addr, pw, label='INBOX', limit=3, debug=False, max_age_hours=None):
    m = imaplib.IMAP4_SSL('imap.gmail.com', timeout=20)
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
    now_utc = datetime.now(timezone.utc)
    for msg_id in ids[::-1]:
        if len(msgs) >= limit:
            break
        typ, msg_data = m.fetch(msg_id, '(RFC822)')
        if typ!='OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        dt = None
        try:
            dt = parsedate_to_datetime(msg.get('Date'))
            if dt and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except Exception:
            dt = None
        if max_age_hours is not None and dt:
            age_hours = (now_utc - dt.astimezone(timezone.utc)).total_seconds() / 3600.0
            if age_hours > max_age_hours:
                continue
        elif dt and (now_utc - dt.astimezone(timezone.utc)).days > 7:
            continue
        msgs.append({
            'from': decode(msg.get('From')),
            'subject': decode(msg.get('Subject')),
            'date': dt.isoformat() if dt else msg.get('Date')
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
    if not TENANT or not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError('Exchange env missing TENANT_ID, CLIENT_ID, or CLIENT_SECRET')
    body = urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }).encode()
    req = urllib.request.Request(f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token", data=body)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())['access_token']


def _graph_json(url, token):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}', 'Accept':'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore') if hasattr(e, 'read') else ''
        raise RuntimeError(f'HTTP {e.code} {e.reason} {body[:500]} url={url}')


def graph_mailbox_candidates(token, mailbox):
    candidates = []
    if mailbox:
        candidates.append(mailbox)
    return candidates


def exchange_unread(token, mailbox, limit=10):
    params = urllib.parse.urlencode({
        '$top': limit,
        '$filter': 'isRead eq false'
    })
    candidates = graph_mailbox_candidates(token, mailbox)
    last_err = None
    for candidate in candidates:
        path = '/me' if candidate == 'me' else f'/users/{urllib.parse.quote(candidate)}'
        url = f"https://graph.microsoft.com/v1.0{path}/mailFolders/Inbox/messages?{params}"
        try:
            data = _graph_json(url, token)
            return [
                {
                    'from': m.get('from',{}).get('emailAddress',{}).get('address'),
                    'subject': m.get('subject'),
                    'date': m.get('receivedDateTime')
                } for m in data.get('value',[])
            ]
        except Exception as e:
            last_err = e
            if '404' not in str(e):
                raise
    raise last_err or RuntimeError('Exchange unread lookup failed')


def exchange_events(token, mailbox, hours=24, limit=10):
    now = datetime.now(timezone.utc)
    end = now + timedelta(hours=hours)
    params = urllib.parse.urlencode({
        'startDateTime': now.isoformat(),
        'endDateTime': end.isoformat(),
        '$top': limit,
        '$orderby': 'start/dateTime'
    })
    candidates = graph_mailbox_candidates(token, mailbox)
    last_err = None
    for candidate in candidates:
        path = '/me' if candidate == 'me' else f'/users/{urllib.parse.quote(candidate)}'
        url = f"https://graph.microsoft.com/v1.0{path}/calendarView?{params}"
        try:
            data = _graph_json(url, token)
            events=[]
            for e in data.get('value', []):
                events.append({
                    'subject': e.get('subject'),
                    'start': e.get('start',{}).get('dateTime'),
                    'end': e.get('end',{}).get('dateTime')
                })
            return events
        except Exception as e:
            last_err = e
            if '404' not in str(e):
                raise
    raise last_err or RuntimeError('Exchange events lookup failed')

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
summary = { 'ts': datetime.now(timezone.utc).isoformat(), 'gmail': {}, 'exchange': {}, 'gmail_cal': {}, 'errors': [], 'health': {}, 'debug': {} }

DEBUG_GMAIL = os.getenv('DEBUG_GMAIL_IMAP') == '1'
for addr,pw in gmail_accounts:
    try:
        summary['gmail'][addr] = with_timeout(15, gmail_unread, addr, pw, debug=DEBUG_GMAIL, label='INBOX', limit=3, max_age_hours=24 if addr == 'georgebroadbent67@gmail.com' else None)
    except Exception as e:
        summary['gmail'][addr] = {"error": str(e)}
        summary['errors'].append({"gmail": addr, "error": str(e)})

MAILBOX = os.getenv('MAILBOX_EMAIL')
summary['debug']['tenant_id'] = os.getenv('TENANT_ID')
summary['debug']['mailbox_email'] = MAILBOX
summary['debug']['db_app_settings_keys'] = sorted(_db_settings.keys())
if not MAILBOX:
    summary['exchange']['error'] = 'MAILBOX_EMAIL is not set'
else:
    try:
        token = with_timeout(20, graph_token)
        summary['debug']['graph_candidates'] = graph_mailbox_candidates(token, MAILBOX)
        summary['debug']['gmail_calendar_sources'] = {
            'gmail1': os.getenv('GMAIL1_ICAL_URL') is not None,
            'gmail2': os.getenv('GMAIL2_ICAL_URL') is not None,
        }
        summary['debug']['gmail1_ical_url'] = os.getenv('GMAIL1_ICAL_URL')[:40] if os.getenv('GMAIL1_ICAL_URL') else None
        summary['debug']['gmail2_ical_url'] = os.getenv('GMAIL2_ICAL_URL')[:40] if os.getenv('GMAIL2_ICAL_URL') else None
        summary['exchange']['unread'] = with_timeout(20, exchange_unread, token, MAILBOX)
        summary['exchange']['events_next_24h'] = with_timeout(20, exchange_events, token, MAILBOX)
    except Exception as e:
        summary['exchange']['error'] = str(e)
        summary['errors'].append({"exchange": MAILBOX, "error": str(e)})

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
        shown = 0
        for item in items:
            lines.append(f"- {addr}: {item.get('from','?')} — {item.get('subject','?')}")
            shown += 1
            if shown >= 10:
                break

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
        from zoneinfo import ZoneInfo
        london = ZoneInfo('Europe/London')
        lines.append(f"- events next 24h: {len(events)}")
        for item in events[:5]:
            s = item.get('start','?')
            try:
                dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
                s = dt.astimezone(london).strftime('%Y-%m-%d %H:%M %Z')
            except Exception:
                pass
            lines.append(f"  - {s} — {item.get('subject','?')}")
    dbg = summary.get('debug', {})
    if dbg:
        lines.append('')
        lines.append('Exchange debug:')
        for k in ('tenant_id', 'mailbox_email', 'graph_me_mailbox'):
            if k in dbg:
                lines.append(f"- {k}: {dbg.get(k)}")

    lines.append('')
    lines.append('Gmail calendars:')
    for key, items in gmail_cal.items():
        lines.append(f"- {key}: {len(items)} upcoming")
        for item in items[:10]:
            lines.append(f"  - {item.get('start','?')} — {item.get('summary','?')}")
    return '\n'.join(lines)


print(human_summary(summary))

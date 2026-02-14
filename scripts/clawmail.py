#!/usr/bin/env python3
"""
Clawdine Email Helper - AgentMail CLI
Usage:
  email.py inbox          - List recent messages
  email.py read <id>      - Read a specific message
  email.py send <to> <subject> <body>  - Send an email
  email.py unread         - List unread messages
"""

import sys
import os

# API key from secure location
API_KEY_FILE = os.path.expanduser("~/.openclaw/workspace/.credentials/agentmail-api-key")
INBOX_ID = "clawdine@agentmail.to"

def get_client():
    from agentmail import AgentMail
    with open(API_KEY_FILE) as f:
        api_key = f.read().strip()
    return AgentMail(api_key=api_key)

def list_inbox(limit=10):
    client = get_client()
    messages = client.inboxes.messages.list(inbox_id=INBOX_ID, limit=limit)
    print(f"📧 Inbox: {INBOX_ID} ({messages.count} total)\n")
    for msg in messages.messages:
        status = "📬" if not getattr(msg, 'read', True) else "📭"
        subject = msg.subject or "(no subject)"
        from_addr = getattr(msg.from_, 'email', str(msg.from_)) if msg.from_ else "unknown"
        print(f"{status} {msg.created_at.strftime('%m/%d %H:%M')} | {from_addr[:30]:30} | {subject[:40]}")
        print(f"   ID: {msg.message_id}")

def read_message(message_id):
    client = get_client()
    msg = client.inboxes.messages.get(inbox_id=INBOX_ID, message_id=message_id)
    print(f"From: {msg.from_}")
    print(f"To: {msg.to}")
    print(f"Subject: {msg.subject}")
    print(f"Date: {msg.created_at}")
    print(f"\n{'='*60}\n")
    print(msg.text or msg.html or "(no body)")

def send_email(to, subject, body):
    client = get_client()
    result = client.inboxes.messages.send(
        inbox_id=INBOX_ID,
        to=[to],
        subject=subject,
        text=body
    )
    print(f"✅ Sent to {to}")
    print(f"Message ID: {result.message_id}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "inbox":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        list_inbox(limit)
    elif cmd == "read" and len(sys.argv) > 2:
        read_message(sys.argv[2])
    elif cmd == "send" and len(sys.argv) > 4:
        send_email(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    elif cmd == "unread":
        list_inbox(limit=20)  # TODO: filter unread only
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()

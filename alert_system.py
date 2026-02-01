import requests
from datetime import datetime

# ==========================================
# 1. PASTE YOUR COPIED DISCORD WEBHOOK URL BELOW
#    It must start with "https://discord.com/api/webhooks/..."
# ==========================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1467549446064570378/FmRIZdiIwLxNJI-GMQWf3Ti-Bz7WHmMi1RkSvGzCLkcpO1EwnhKoWWtD7zCyueCscBfc"  # <--- DELETE THIS & PASTE YOUR URL

def alert_security_team(user_input, reason, user_id="demo_user"):
    """
    Sends a formatted alert to Discord when a threat is detected.
    """
    if "https://" not in WEBHOOK_URL:
        print("❌ Error: Webhook URL not set in alert_system.py")
        return

    print(f"🚨 Sending Alert: {reason}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Logic: If it's a "User Override" (Redacted), use Orange. If Blocked, use Red.
    if "Override" in reason or "Redacted" in reason:
        color = 0xFFA500 # Orange (Warning)
        title = "⚠️ Security Warning: User Override"
        desc = "User authorized processing of redacted content."
    else:
        color = 0xFF0000 # Red (Danger)
        title = "🚨 Security Alert: Threat Blocked"
        desc = "A malicious file or image was intercepted."

    # Build the Discord Embed Card
    embed = {
        "title": title,
        "description": desc,
        "color": color,
        "fields": [
            {"name": "👤 User ID", "value": str(user_id), "inline": True},
            {"name": "⏰ Time", "value": timestamp, "inline": True},
            {"name": "🛡️ Detection Reason", "value": reason, "inline": False},
            {"name": "📄 Content Snippet", "value": f"```{str(user_input)[:200]}...```", "inline": False}
        ],
        "footer": {"text": "Verity Gateway • Security Ops"}
    }
    
    data = {"embeds": [embed]}
    
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=3)
        if response.status_code == 204:
            print("✅ Alert sent to Discord!")
        else:
            print(f"⚠️ Discord rejected the alert (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Error sending alert: {e}")

# --- TEST BLOCK ---
# Run this file directly (python alert_system.py) to test the connection
if __name__ == "__main__":
    alert_security_team("CONFIDENTIAL_PASSWORD_123", "Manual Test: Blocked Password", "Admin_User")


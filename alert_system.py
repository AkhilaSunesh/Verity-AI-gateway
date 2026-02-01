import requests
from datetime import datetime

# REPLACE WITH YOUR ACTUAL WEBHOOK URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1467549446064570378/FmRIZdiIwLxNJI-GMQWf3Ti-Bz7WHmMi1RkSvGzCLkcpO1EwnhKoWWtD7zCyueCscBfc"

def alert_security_team(user_input, reason, user_id="USER-101"):
    if "https://" not in WEBHOOK_URL: return
    
    # Generate timestamp in the format shown in your screenshot
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine alert level based on the reason
    is_blocked = "Override" not in reason
    color = 0xFF0000 if is_blocked else 0xFFA500  # Red for Blocked, Orange for Override
    title = "🚨 Security Alert: Threat Blocked" if is_blocked else "⚠️ Security Warning: User Override"
    desc = "A malicious file or image was intercepted." if is_blocked else "User authorized processing of flagged content."

    embed = {
        "title": title,
        "description": desc,
        "color": color,
        "fields": [
            {"name": "👤 User ID", "value": str(user_id), "inline": True},
            {"name": "⏰ Time", "value": timestamp, "inline": True}, # Reflects precise time
            {"name": "🛡️ Detection Reason", "value": reason, "inline": False},
            {"name": "📄 Content Snippet", "value": f"```{str(user_input)[:200]}```", "inline": False}
        ],
        "footer": {"text": "Verity Gateway • Security Ops"}
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed]}, timeout=3)
    except Exception as e:
        print(f"Alert failed: {e}")

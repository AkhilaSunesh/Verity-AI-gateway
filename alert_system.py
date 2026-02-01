import requests
from datetime import datetime

# ==========================================
# PASTE YOUR DISCORD WEBHOOK URL BELOW
# It should look like: "https://discord.com/api/webhooks/..."
# ==========================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1467549446064570378/FmRIZdiIwLxNJI-GMQWf3Ti-Bz7WHmMi1RkSvGzCLkcpO1EwnhKoWWtD7zCyueCscBfc" 

def alert_security_team(user_input, reason, user_id="demo_user"):
    """
    Sends a rich formatted alert to Discord when a threat is detected.
    """
    print(f"🚨 Sending Alert: {reason}") # This prints to your screen
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # This 'embed' structure makes it look professional in Discord
    embed = {
        "title": "🚨 AI Gateway Security Alert",
        "description": "A threat was intercepted and blocked.",
        "color": 0xFF0000, # Red color for danger
        "fields": [
            {"name": "User", "value": user_id, "inline": True},
            {"name": "Time", "value": timestamp, "inline": True},
            {"name": "Detection Reason", "value": reason, "inline": False},
            {"name": "Blocked Content", "value": f"```{user_input[:200]}...```", "inline": False}
        ],
        "footer": {"text": "Sandboxed AI Gateway • Security Team"}
    }
    
    data = {"embeds": [embed]}
    
    try:
        # This acts like hitting "Send"
        response = requests.post(WEBHOOK_URL, json=data, timeout=3)
        
        if response.status_code == 204:
            print("✅ Alert sent successfully! Check Discord.")
        else:
            print(f"⚠️ Failed to send alert. Error code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending alert: {e}")

# --- TEST BLOCK (This runs when you press Play) ---
if __name__ == "__main__":
    # We are simulating a fake hacker to see if it works
    alert_security_team(
        user_input="I need to bypass the mainframe using the confidential passwords.", 
        reason="Confidential Keyword Detected", 
        user_id="Hacker_X"
    )
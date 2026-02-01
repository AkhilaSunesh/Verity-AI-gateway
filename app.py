import streamlit as st
import time
import io
import ollama
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- IMPORTS ---
try:
    from pypdf import PdfReader
except ImportError:
    st.error("⚠️ pypdf missing. Run: pip install pypdf")
    st.stop()

try:
    from security_text import sanitize_text
except ImportError:
    st.error("⚠️ security_text.py missing.")
    st.stop()

try:
    from security_image import analyze_image
except ImportError:
    analyze_image = lambda x: (True, "Safe")

try:
    from alert_system import alert_security_team
except ImportError:
    alert_security_team = lambda p, r, u: None

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sandboxed AI Gateway", page_icon="🛡️", layout="wide")

# --- SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "logs" not in st.session_state: st.session_state.logs = []
if "stats" not in st.session_state: st.session_state.stats = {"safe": 0, "redacted": 0, "blocked": 0}
if "active_prompt" not in st.session_state: st.session_state.active_prompt = None
if "pending_image_event" not in st.session_state: st.session_state.pending_image_event = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Security Controls")
    c1, c2, c3 = st.columns(3)
    c1.metric("Safe", st.session_state.stats["safe"])
    c2.metric("Redacted", st.session_state.stats["redacted"])
    c3.metric("Blocked", st.session_state.stats["blocked"])
    
    st.divider()
    st.subheader("🖼️ Image Scan")
    uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_image:
        # Check image security
        is_safe, reason = analyze_image(uploaded_image)
        if not is_safe:
            # Store event for the main loop to handle
            st.session_state.pending_image_event = {"name": uploaded_image.name, "reason": reason, "file": uploaded_image}
        else:
            st.success("✅ Image Cleared")

    st.divider()
    st.caption("Activity Log")
    log_text = "\n".join(reversed(st.session_state.logs))
    st.text_area("Logs", value=log_text, height=150, disabled=True)

# --- MAIN PAGE ---
st.title("🛡️ Sandboxed AI Gateway")

# 1. HANDLE SENSITIVE IMAGES (The Soft Block)
if st.session_state.pending_image_event:
    event = st.session_state.pending_image_event
    
    st.warning(f"🛑 **SENSITIVE IMAGE DETECTED**")
    st.info(f"Reason: {event['reason']}")
    
    # Show a "Redacted" visual instead of the real image
    st.image("https://via.placeholder.com/400x200?text=REDACTED+FOR+SECURITY", width=400)
    
    col1, col2 = st.columns(2)
    if col1.button("⚠️ Proceed & Report to SOC"):
        # Log and Alert
        st.session_state.stats["blocked"] += 1
        st.session_state.logs.append(f"[IMG OVERRIDE] {event['reason']}")
        alert_security_team(f"Image: {event['name']}", f"User Override: {event['reason']}", "USER-101")
        
        # Add to chat as an authorized event
        st.session_state.messages.append({"role": "user", "content": f"Shared Image: {event['name']} (Override Authorized)"})
        st.session_state.messages.append({"role": "assistant", "content": "🚨 This image was flagged for sensitive data but authorized by the user for processing."})
        
        st.session_state.pending_image_event = None
        st.rerun()
        
    if col2.button("Discard Image"):
        st.session_state.pending_image_event = None
        st.rerun()

# 2. CHAT INPUT
if chat_input := st.chat_input("Enter prompt..."):
    st.session_state.active_prompt = chat_input
    st.session_state.messages.append({"role": "user", "content": chat_input})

# 3. PROCESSING TEXT PROMPTS
if st.session_state.active_prompt:
    prompt = st.session_state.active_prompt
    safe_text = sanitize_text(prompt)
    
    if safe_text != prompt:
        st.error("🛑 **SECURITY HOLD: Sensitive Data in Prompt**")
        st.code(safe_text, language="text")
        if st.button("Confirm Override"):
            alert_security_team(prompt, "Text Override", "USER-101")
            # Logic to call LLM would go here...
            st.session_state.active_prompt = None
            st.rerun()
    else:
        # Standard Safe Processing
        with st.chat_message("assistant"):
            st.write("Processing safe query...")
        st.session_state.active_prompt = None

# 4. HISTORY
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

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

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Sandboxed AI Gateway", page_icon="🛡️", layout="wide")

# --- 2. HELPERS ---
def generate_pdf_report(user_text, ai_response, user_id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "SECURE AI TRANSCRIPT")
    c.setFont("Helvetica", 10)
    c.drawString(50, 735, f"User: {user_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(50, 725, 550, 725)
    text_obj = c.beginText(50, 700)
    text_obj.setFont("Courier", 10)
    display_prompt = user_text[:500] + "..." if len(user_text) > 500 else user_text
    content = f"INPUT:\n{display_prompt}\n\nRESULT:\n{ai_response}"
    for line in content.split('\n'):
        while len(line) > 80:
            text_obj.textLine(line[:80])
            line = line[80:]
        text_obj.textLine(line)
    c.drawText(text_obj)
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "logs" not in st.session_state: st.session_state.logs = []
if "stats" not in st.session_state: st.session_state.stats = {"safe": 0, "redacted": 0, "blocked": 0}
if "active_prompt" not in st.session_state: st.session_state.active_prompt = None
if "pending_event" not in st.session_state: st.session_state.pending_event = None
if "last_file_id" not in st.session_state: st.session_state.last_file_id = None

# --- 4. SIDEBAR & SCANNING ---
with st.sidebar:
    st.header("⚙️ Security Controls")
    c1, c2, c3 = st.columns(3)
    c1.metric("Safe", st.session_state.stats["safe"])
    c2.metric("Redacted", st.session_state.stats["redacted"])
    c3.metric("Blocked", st.session_state.stats["blocked"])
    
    st.divider()
    
    # A. DOCUMENT UPLOAD
    uploaded_doc = st.file_uploader("📂 Document Scan", type=["pdf", "txt", "py", "md"])
    if uploaded_doc and st.session_state.last_file_id != uploaded_doc.name:
        text_content = ""
        if uploaded_doc.type == "application/pdf":
            reader = PdfReader(uploaded_doc)
            for page in reader.pages:
                text_content += (page.extract_text() or "") + "\n"
        else:
            text_content = uploaded_doc.read().decode("utf-8")
        
        # Immediate Text Scan
        safe_ver = sanitize_text(text_content)
        if safe_ver != text_content:
            st.session_state.pending_event = {
                "type": "doc", "name": uploaded_doc.name, 
                "raw": text_content, "safe": safe_ver, "reason": "Sensitive PII detected in text"
            }
        else:
            st.session_state.active_prompt = f"Analyze: {text_content}"
        st.session_state.last_file_id = uploaded_doc.name

    # B. IMAGE UPLOAD
    uploaded_image = st.file_uploader("🖼️ Image Scan", type=["png", "jpg", "jpeg"])
    if uploaded_image and st.session_state.last_file_id != uploaded_image.name:
        is_safe, img_reason = analyze_image(uploaded_image)
        if not is_safe:
            st.session_state.pending_event = {
                "type": "image", "name": uploaded_image.name, "reason": img_reason
            }
        else:
            st.success("✅ Image Safe")
        st.session_state.last_file_id = uploaded_image.name

    st.divider()
    log_text = "\n".join(reversed(st.session_state.logs))
    st.text_area("Logs", value=log_text, height=150, disabled=True)

# --- 5. MAIN PAGE ---
st.title("🛡️ Sandboxed AI Gateway")

# UI Logic: If something is pending, show the REDACTED UI
if st.session_state.pending_event:
    event = st.session_state.pending_event
    st.warning(f"🛑 **SECURITY HOLD: {event['name']}**")
    st.info(f"Reason: {event['reason']}")
    
    if event['type'] == "image":
        st.image("https://via.placeholder.com/400x150?text=REDACTED+IMAGE", width=400)
    else:
        st.markdown("### Redacted Content Preview:")
        st.code(event['safe'][:1000], language="text")

    col1, col2 = st.columns(2)
    if col1.button("⚠️ Proceed & Report"):
        st.session_state.stats["redacted"] += 1
        st.session_state.logs.append(f"[OVERRIDE] {event['name']}")
        alert_security_team(event.get('raw', event['name']), event['reason'], "USER-101")
        
        # Add a special system message to the chat
        st.session_state.messages.append({"role": "assistant", "content": f"🚨 **Security Warning:** User authorized processing of flagged {event['type']}."})
        
        # Clear the block
        st.session_state.pending_event = None
        st.rerun()

    if col2.button("Discard File"):
        st.session_state.pending_event = None
        st.rerun()

# 6. CHAT INPUT
if chat_input := st.chat_input("Enter prompt..."):
    st.session_state.active_prompt = chat_input
    st.session_state.messages.append({"role": "user", "content": chat_input})

# 7. PROCESSING LOOP
if st.session_state.active_prompt:
    prompt = st.session_state.active_prompt
    safe_text = sanitize_text(prompt)
    
    if safe_text != prompt:
        # Re-use the pending_event logic for Chat too
        st.session_state.pending_event = {
            "type": "chat", "name": "Chat Prompt", "raw": prompt, "safe": safe_text, "reason": "PII in Chat"
        }
        st.session_state.active_prompt = None
        st.rerun()
    else:
        with st.chat_message("assistant"):
            response = ""
            stream = ollama.chat(model="qwen2.5:3b", messages=[{'role': 'user', 'content': prompt}], stream=True)
            placeholder = st.empty()
            for chunk in stream:
                response += chunk['message']['content']
                placeholder.markdown(response + "▌")
            placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.active_prompt = None

# 8. HISTORY
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

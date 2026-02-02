# 🛡️ Verity AI Gateway
> **Team Members:** Akhila Sunesh,Aleeta K Alex,Amrutha Ajish,Anjali Thomas
> 
> **Team Name:** AAA Battery

**Secure. Monitor. Control.**
*A multi-modal security layer protecting LLM interactions by detecting sensitive data in real-time.*

## 📖 Overview
**Verity AI Gateway** is a robust security intermediary designed to sit between users and Large Language Models (LLMs). It acts as a firewall for AI, automatically scanning text, documents, and images for Personally Identifiable Information (PII) and malicious content before it reaches the model.

If a threat is detected, the system intercepts the request, sanitizes the data, and instantly notifies security teams via Discord—ensuring that your AI adoption remains safe, compliant, and private.

## ✨ Key Features

* **🔒 Real-Time PII Redaction**
    * Automatically detects and redacts sensitive entities (names, phone numbers, emails, etc.) from chat prompts and uploaded documents using **Microsoft Presidio**.
* **🚨 Instant Discord Alerts**
    * Triggers live, rich-formatted security alerts to a dedicated Discord channel whenever a threat is blocked or a user attempts an override.
* **🖼️ Multi-Modal Scanning**
    * Scans uploaded images (JPG, PNG) and documents (PDF, TXT) for hidden risks using **EasyOCR** and custom vision logic.
* **🤖 Local LLM Integration**
    * Seamlessly connects to local models (via **Ollama**) to ensure data privacy, using `qwen2.5:3b` for intelligent responses.
* **📊 Live Security Dashboard**
    * A sidebar interface tracking real-time metrics: Safe Requests, Redacted Content, and Blocked Threats.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI Engine:** Ollama (Qwen 2.5)
* **Security & NLP:** Presidio Analyzer/Anonymizer, Spacy
* **Computer Vision:** EasyOCR, OpenCV, Pillow
* **Alerting:** Python Requests (Discord Webhooks)

## 🚀 Installation

### Prerequisites
* Python 3.8+
* [Ollama](https://ollama.com/) installed and running locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/AkhilaSunesh/Verity-AI-gateway.git](https://github.com/AkhilaSunesh/Verity-AI-gateway.git)
cd Verity-AI-gateway
```
## 🔮 Future Scope & Roadmap

### 1. Integration with Google Gemini API
**Current State:** The system uses a local LLM (Ollama) to ensure total data isolation during the proof-of-concept phase.
**Future Goal:** Integrate **Google Gemini API** to demonstrate the gateway's ability to act as a secure middleware for enterprise-grade public models.

**Proposed Architecture:**
1. **User Request** → **Verity Gateway** (Sanitization Layer)
2. **Verity Gateway** → **Gemini API** (Sends only clean, redacted JSON)
3. **Gemini API** → **Verity Gateway** (Returns intelligent response)
4. **Verity Gateway** → **User** (Delivers safe answer)

**Validation Metric:**
We will implement an audit log comparing the *Original User Prompt* vs. the *Payload Sent to Gemini* to mathematically prove that zero PII (Personally Identifiable Information) leaves the secure environment.

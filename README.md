# ✉️ Executive Mail AI — Professional Email Generator

A clean, modern, and executive-ready email writing assistant built with **Streamlit** and local **Ollama** (`tinyllama:latest`).

---

## ✨ Features

- **Executive UI**: Clean dual-pane workspace designed like a modern email client with sleek typography and subtle card styling.
- **Structured Email Specification**:
  - **Recipient**: Target individual or audience.
  - **Email Purpose**: Clear objective and intent.
  - **Tone Selector**: Professional & Direct, Formal & Executive, Polite & Diplomatic, Warm & Friendly, Persuasive, Apologetic, or Custom.
  - **Important Points**: Bulleted or line-separated key notes that guide the email content.
  - **Optional Sign-off & CTA**: Add custom sender name and specific Call-to-Action.
- **Live Token Streaming**: Real-time generation feedback via Ollama.
- **Email Client Preview & Actions**:
  - Prominent Subject Line display.
  - Formatted email body.
  - Word count & estimated reading time.
  - ✉️ **Open in Email App** (`mailto:` pre-filled launch button).
  - 📋 **One-Click Copy** to clipboard.
  - ✏️ **In-line Editing Mode** to tweak the text before sending.
  - ⚡ **One-Click Refinements**: *Make Shorter*, *More Formal*, *Add Warmth*.
  - 📜 **Version History**: Review and restore earlier drafts created during your session.
- **Quick Executive Templates**: 1-click presets for Meeting Follow-ups, Status Updates, Reschedules, Deadline Extensions, and Client Proposals.
- **100% Local & Private**: Runs entirely on your machine via Ollama with zero third-party API keys or external data transmission.

---

## 🚀 How to Run

### 1. Ensure Ollama is Running
Make sure Ollama is installed and running on your system:
```bash
ollama serve
```

Ensure the model is pulled:
```bash
ollama pull tinyllama:latest
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

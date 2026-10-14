import streamlit as st
import ollama
import urllib.parse
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Executive Mail AI | Professional Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN EXECUTIVE CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top banner card */
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }

    .hero-title {
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 6px;
        margin-bottom: 0;
        line-height: 1.5;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #22c55e;
        box-shadow: 0 0 8px #22c55e;
    }

    /* Section styling */
    .card-box {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 22px;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.03);
        margin-bottom: 18px;
    }

    /* Email Preview Container (Window Frame) */
    .email-window {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.08);
        overflow: hidden;
        margin-top: 4px;
    }

    .email-window-header {
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        padding: 14px 20px;
    }

    .email-meta-row {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        font-size: 13px;
    }

    .email-meta-label {
        color: #64748b;
        font-weight: 600;
        width: 70px;
        flex-shrink: 0;
    }

    .email-meta-value {
        color: #0f172a;
        font-weight: 500;
    }

    .subject-highlight {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
        background: #eff6ff;
        padding: 10px 14px;
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        margin-top: 4px;
    }

    .email-window-body {
        padding: 24px;
        color: #1e293b;
        font-size: 15px;
        line-height: 1.7;
        white-space: pre-wrap;
        background: #ffffff;
    }

    /* Stats chip */
    .meta-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }

    /* Empty state */
    .empty-state-box {
        text-align: center;
        padding: 60px 30px;
        background: #f8fafc;
        border-radius: 16px;
        border: 2px dashed #cbd5e1;
    }

    .empty-icon {
        font-size: 48px;
        margin-bottom: 14px;
        display: inline-block;
    }

    .empty-title {
        font-size: 18px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 8px;
    }

    .empty-desc {
        font-size: 13.5px;
        color: #64748b;
        max-width: 440px;
        margin: 0 auto 16px auto;
        line-height: 1.5;
    }

    /* Button styling adjustments */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    /* Primary button accent */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    }
</style>
""", unsafe_allow_html=True)


# --- TEMPLATE PRESETS ---
PRESETS = {
    "meeting_followup": {
        "title": "🤝 Meeting Follow-up",
        "recipient": "Sarah Jenkins (VP of Product)",
        "purpose": "Follow up on yesterday's product roadmap review and confirm action items",
        "tone": "Professional & Direct",
        "points": "- Thanked her for constructive feedback on the analytics UX\n- Confirmed engineering is updating dashboard wireframes\n- Revised prototype ready by Thursday 3:00 PM\n- Requested a 15-minute sync on Friday to review updates",
        "sender": "Alex Morgan | Senior Solutions Architect"
    },
    "project_update": {
        "title": "🚀 Project Status Update",
        "recipient": "Project Steering Committee & Stakeholders",
        "purpose": "Provide bi-weekly progress update on Core API Migration",
        "tone": "Formal & Executive",
        "points": "- Completed migration of user authentication service with zero downtime\n- Performance latency reduced by 32% under synthetic load testing\n- On schedule for staging deployment on October 24\n- No major blockers or budget deviations identified",
        "sender": "David Chen | Lead Project Manager"
    },
    "reschedule": {
        "title": "📅 Meeting Reschedule",
        "recipient": "Dr. Clara Evans (Research Director)",
        "purpose": "Request to reschedule our 1-on-1 strategy sync due to an urgent client priority",
        "tone": "Polite & Diplomatic",
        "points": "- Sincere apologies for the short notice\n- Unanticipated escalation meeting with high-priority enterprise client at 2:00 PM today\n- Proposed alternative times: Tomorrow (Thursday) at 11:00 AM or 3:30 PM\n- Happy to adjust to any slot convenient for her calendar",
        "sender": "Rachel Adams | Technical Account Manager"
    },
    "deadline_extension": {
        "title": "⏳ Deadline Extension",
        "recipient": "Marcus Vance (Department Lead)",
        "purpose": "Request a 48-hour extension on the Q3 Financial Audit Report",
        "tone": "Professional & Direct",
        "points": "- Encountered legacy database schema discrepancies during validation\n- Automated reconciliation script requires an extra 48 hours to guarantee 100% data integrity\n- Revised submission date: Friday at 2:00 PM\n- Rest of the project milestones remain unaffected",
        "sender": "Jordan Miller | Senior Financial Analyst"
    },
    "client_proposal": {
        "title": "💡 Client Proposal Outreach",
        "recipient": "Arthur Pendelton (VP of Operations, Global Logistics)",
        "purpose": "Introduce automated dispatch solution and offer an executive demo",
        "tone": "Persuasive & Enthusiastic",
        "points": "- Great connecting at the Logistics & Supply Chain Expo\n- Prepared custom simulation showing 24% reduction in fleet idle hours\n- Attached 2-page executive summary of proposed proof-of-concept\n- Invited to a 20-minute live demonstration next Tuesday or Wednesday",
        "sender": "Elena Rostova | Enterprise Account Executive"
    }
}

# --- INITIALIZE SESSION STATE ---
if "recipient_input" not in st.session_state:
    st.session_state.recipient_input = ""
if "purpose_input" not in st.session_state:
    st.session_state.purpose_input = ""
if "tone_input" not in st.session_state:
    st.session_state.tone_input = "Professional & Direct"
if "points_input" not in st.session_state:
    st.session_state.points_input = ""
if "sender_input" not in st.session_state:
    st.session_state.sender_input = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = ""
if "current_body" not in st.session_state:
    st.session_state.current_body = ""
if "email_history" not in st.session_state:
    st.session_state.email_history = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False


def apply_preset(preset_key):
    preset = PRESETS[preset_key]
    st.session_state.recipient_input = preset["recipient"]
    st.session_state.purpose_input = preset["purpose"]
    st.session_state.tone_input = preset["tone"]
    st.session_state.points_input = preset["points"]
    st.session_state.sender_input = preset["sender"]


def clear_inputs():
    st.session_state.recipient_input = ""
    st.session_state.purpose_input = ""
    st.session_state.tone_input = "Professional & Direct"
    st.session_state.points_input = ""
    st.session_state.sender_input = ""
    st.session_state.current_subject = ""
    st.session_state.current_body = ""
    st.session_state.edit_mode = False


def parse_email_response(text):
    """Cleanly extracts the subject line and email body from model output."""
    lines = text.strip().splitlines()
    subject = ""
    body_lines = []
    found_subject = False

    for line in lines:
        cleaned_line = line.strip()
        lower_line = cleaned_line.lower()

        # Check for Subject line prefix
        if not found_subject and (lower_line.startswith("subject:") or lower_line.startswith("**subject:**")):
            parts = cleaned_line.split(":", 1)
            if len(parts) > 1:
                subject = parts[1].strip().strip("*").strip()
                found_subject = True
                continue

        # Ignore lines repeating prompt metadata or headers like 'Recipient:'
        if not found_subject and any(lower_line.startswith(prefix) for prefix in ["recipient:", "purpose:", "tone:", "receiver:", "to:"]):
            continue

        if found_subject:
            # Stop if the model starts echoing prompt instructions at the end
            if any(lower_line.startswith(stop_phrase) for stop_phrase in ["requirements:", "inclduing:", "including:"]):
                break
            body_lines.append(line)
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    
    # Fallback subject if not explicitly parsed
    if not subject:
        # Check first line
        if lines and len(lines[0].strip()) < 80 and not lines[0].strip().endswith("."):
            subject = lines[0].strip().replace("Subject:", "").strip()
            body = "\n".join(lines[1:]).strip()
        else:
            subject = "Business Correspondence"

    return subject, body


# --- SIDEBAR: CONTROLS & STATUS ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")

    # Dynamic Ollama Model Detection
    available_models = ["tinyllama:latest"]
    ollama_online = False
    try:
        model_list_response = ollama.list()
        detected_names = [m.model for m in model_list_response.models]
        if detected_names:
            available_models = detected_names
            ollama_online = True
    except Exception:
        ollama_online = False

    # Status Pill
    if ollama_online:
        st.markdown("""
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px 14px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: #16a34a; box-shadow: 0 0 6px #16a34a;"></div>
            <span style="font-size: 13px; font-weight: 600; color: #166534;">Ollama Service Active</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 10px 14px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: #dc2626;"></div>
            <span style="font-size: 13px; font-weight: 600; color: #991b1b;">Ollama Offline / Unreachable</span>
        </div>
        """, unsafe_allow_html=True)

    default_index = 0
    if "tinyllama:latest" in available_models:
        default_index = available_models.index("tinyllama:latest")

    selected_model = st.selectbox(
        "AI Model",
        options=available_models,
        index=default_index,
        help="Select any local model running on your Ollama server."
    )

    email_length = st.select_slider(
        "Email Length Target",
        options=["Concise & Crisp", "Standard / Balanced", "Detailed & In-depth"],
        value="Standard / Balanced"
    )

    st.markdown("---")
    st.markdown("### 📋 Quick Templates")
    st.caption("Click to load realistic pre-structured executive scenarios:")

    for p_key, p_val in PRESETS.items():
        if st.button(p_val["title"], key=f"btn_preset_{p_key}", use_container_width=True):
            apply_preset(p_key)
            st.rerun()

    st.markdown("---")
    if st.button("🧹 Clear All Fields", use_container_width=True):
        clear_inputs()
        st.rerun()

    # Etiquette & requirements badge
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 12px; color: #64748b; line-height: 1.6;">
        <strong style="color: #334155;">🔒 100% Local & Private</strong><br>
        All email generations are computed locally on your machine via Ollama. No data leaves your network.
    </div>
    """, unsafe_allow_html=True)


# --- MAIN HEADER HERO ---
st.markdown("""
<div class="hero-container">
    <div>
        <h1 class="hero-title">
            <span>✉️</span> Executive Mail AI
        </h1>
        <p class="hero-subtitle">
            Draft polished, professional, context-aware business correspondence with local Ollama intelligence.
        </p>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span class="badge-pill">
            <span class="pulse-dot"></span> Local AI Ready
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# --- MAIN 2-COLUMN WORKSPACE ---
col_form, col_preview = st.columns([5, 7], gap="large")

# ==========================================
# LEFT COLUMN: INPUT FORM
# ==========================================
with col_form:
    st.markdown("### 📝 Email Specifications")
    st.caption("Provide key context below. The AI will format, refine, and structure your draft.")

    with st.container():
        # Recipient Input
        recipient_val = st.text_input(
            "👤 Recipient",
            value=st.session_state.recipient_input,
            placeholder="e.g., Sarah Jenkins (VP of Product), Hiring Manager, Team",
            key="input_recipient_field",
            help="Name and/or title of the person or team receiving this email."
        )
        st.session_state.recipient_input = recipient_val

        # Purpose Input
        purpose_val = st.text_input(
            "🎯 Purpose of Email",
            value=st.session_state.purpose_input,
            placeholder="e.g., Follow up on yesterday's roadmap review & confirm next steps",
            key="input_purpose_field",
            help="The primary objective or reason for sending this message."
        )
        st.session_state.purpose_input = purpose_val

        # Tone Selector
        tone_options = [
            "Professional & Direct",
            "Formal & Executive",
            "Polite & Diplomatic",
            "Warm & Friendly",
            "Persuasive & Enthusiastic",
            "Apologetic & Reassuring",
            "Urgent & Action-Oriented",
            "Custom Tone..."
        ]

        current_tone = st.session_state.tone_input
        if current_tone not in tone_options:
            selected_tone_option = "Custom Tone..."
            custom_tone_val = current_tone
        else:
            selected_tone_option = current_tone
            custom_tone_val = ""

        tone_choice = st.selectbox(
            "🎭 Desired Tone",
            options=tone_options,
            index=tone_options.index(selected_tone_option) if selected_tone_option in tone_options else 0,
            key="input_tone_select"
        )

        if tone_choice == "Custom Tone...":
            custom_tone = st.text_input(
                "Specify Custom Tone",
                value=custom_tone_val,
                placeholder="e.g., Firm but encouraging, inquisitive and cautious"
            )
            st.session_state.tone_input = custom_tone if custom_tone else "Professional & Direct"
        else:
            st.session_state.tone_input = tone_choice

        # Key Points Text Area
        points_val = st.text_area(
            "📌 Important Points / Key Notes",
            value=st.session_state.points_input,
            placeholder="Enter the key points to cover (bullet points or sentences):\n• Thanked client for feedback\n• Changes will be deployed by Thursday 3 PM\n• Need approval before Friday release",
            height=160,
            key="input_points_field",
            help="Specific details, data points, dates, or requests to include in the email body."
        )
        st.session_state.points_input = points_val

        # Optional Advanced Settings
        with st.expander("⚙️ Optional Sign-off & Sender Details", expanded=False):
            sender_val = st.text_input(
                "Your Name / Sign-off Title",
                value=st.session_state.sender_input,
                placeholder="e.g., Alex Morgan | Senior Solutions Architect",
                key="input_sender_field",
                help="Appended cleanly at the end of the email closing."
            )
            st.session_state.sender_input = sender_val

            cta_val = st.text_input(
                "Specific Call to Action (Optional)",
                placeholder="e.g., Reply with preferred time slot by Wednesday 5 PM",
                key="input_cta_field"
            )

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        generate_clicked = st.button(
            "✨ Generate Professional Email",
            type="primary",
            use_container_width=True
        )


# ==========================================
# RIGHT COLUMN: EMAIL PREVIEW & ACTIONS
# ==========================================
with col_preview:
    st.markdown("### 📬 Generated Email Preview")
    st.caption("Review your draft, edit on the fly, copy with 1 click, or launch your email app.")

    # GENERATE TRIGGER
    if generate_clicked:
        # Validation
        if not st.session_state.recipient_input.strip() or not st.session_state.purpose_input.strip():
            st.warning("⚠️ Please provide at least a **Recipient** and **Purpose** to generate an email.")
        else:
            # Construct Length Guideline
            length_notes = {
                "Concise & Crisp": "Keep it very concise and punchy (under 100-120 words). Avoid filler.",
                "Standard / Balanced": "Keep it balanced and professional (around 150-200 words).",
                "Detailed & In-depth": "Provide comprehensive context with thorough explanations (250+ words)."
            }.get(email_length, "Balanced and concise.")

            # Build Prompt following user's original specification + refined instructions
            sender_instruction = f"- Conclude with this sign-off name: {st.session_state.sender_input}" if st.session_state.sender_input.strip() else "- Include a clear closing."
            cta_instruction = f"- Clear Call to Action: {cta_val}" if cta_val.strip() else ""

            prompt_content = f"""Write a professional email.

Recipient:
{st.session_state.recipient_input}

Purpose:
{st.session_state.purpose_input}

Tone:
{st.session_state.tone_input}

Important points:
{st.session_state.points_input if st.session_state.points_input.strip() else 'Draft a relevant message matching the purpose.'}

Requirements:
- Write a clear, engaging subject line starting with 'Subject: ' on the first line.
- Keep sentences reasonably short.
- Be polite and professional.
- Do not invent information.
- Length guideline: {length_notes}
{sender_instruction}
{cta_instruction}

Output ONLY the ready-to-send email. Do not repeat the prompt, requirements, or labels.
"""

            # Display streaming container
            with st.spinner("Drafting your executive email..."):
                try:
                    response_stream = ollama.chat(
                        model=selected_model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a professional email writing assistant. You produce clean, polished, ready-to-send executive emails without meta-commentary.",
                            },
                            {"role": "user", "content": prompt_content},
                        ],
                        stream=True
                    )

                    # Stream tokens directly
                    preview_placeholder = st.empty()
                    accumulated_text = ""

                    for chunk in response_stream:
                        delta = chunk.get("message", {}).get("content", "")
                        accumulated_text += delta
                        preview_placeholder.markdown(
                            f"<div style='background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; font-family: monospace; font-size: 13.5px; white-space: pre-wrap; color: #334155;'>{accumulated_text}▌</div>",
                            unsafe_allow_html=True
                        )

                    preview_placeholder.empty()

                    # Parse output into Subject and Body
                    subject, body = parse_email_response(accumulated_text)
                    st.session_state.current_subject = subject
                    st.session_state.current_body = body

                    # Save to History
                    st.session_state.email_history.insert(0, {
                        "timestamp": datetime.now().strftime("%I:%M %p"),
                        "subject": subject,
                        "body": body,
                        "recipient": st.session_state.recipient_input,
                        "tone": st.session_state.tone_input
                    })

                    st.toast("✅ Email generated successfully!", icon="✨")

                except Exception as ex:
                    st.error(f"❌ Failed to communicate with Ollama: {ex}")
                    st.info("💡 Ensure Ollama is running (`ollama serve`) and the model is downloaded (`ollama pull tinyllama:latest`).")

    # DISPLAY DRAFT OR EMPTY STATE
    if st.session_state.current_body:
        # Calculate statistics
        full_email_text = f"Subject: {st.session_state.current_subject}\n\n{st.session_state.current_body}"
        word_count = len(full_email_text.split())
        char_count = len(full_email_text)
        reading_time_mins = max(1, round(word_count / 180, 1))

        # Email Card Header & Metadata
        st.markdown(f"""
        <div class="email-window">
            <div class="email-window-header">
                <div class="email-meta-row">
                    <span class="email-meta-label">To:</span>
                    <span class="email-meta-value">{st.session_state.recipient_input or 'Recipient'}</span>
                </div>
                <div class="email-meta-row" style="margin-bottom: 12px;">
                    <span class="email-meta-label">Tone:</span>
                    <span class="meta-chip">{st.session_state.tone_input}</span>
                    <span class="meta-chip" style="margin-left: 8px;">📊 {word_count} words</span>
                    <span class="meta-chip" style="margin-left: 8px;">⏱️ ~{reading_time_mins} min read</span>
                </div>
                <div class="subject-highlight">
                    <span style="color: #64748b; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 2px;">Subject</span>
                    {st.session_state.current_subject}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Toggle between Preview mode and Direct Edit mode
        edit_col1, edit_col2 = st.columns([8, 4])
        with edit_col2:
            toggle_edit = st.toggle("✏️ Edit Draft Directly", value=st.session_state.edit_mode)
            st.session_state.edit_mode = toggle_edit

        if st.session_state.edit_mode:
            st.caption("You can directly edit the subject and email body below:")
            edited_subj = st.text_input("Edit Subject", value=st.session_state.current_subject)
            edited_body = st.text_area("Edit Body", value=st.session_state.current_body, height=320)
            st.session_state.current_subject = edited_subj
            st.session_state.current_body = edited_body
        else:
            st.markdown(f"""
            <div class="email-window" style="border-top: none; margin-top: -6px; border-top-left-radius: 0; border-top-right-radius: 0;">
                <div class="email-window-body">{st.session_state.current_body}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        # ACTION TOOLBAR
        btn_col1, btn_col2 = st.columns([1, 1], gap="small")

        with btn_col1:
            # Mailto URL encoding
            encoded_subject = urllib.parse.quote(st.session_state.current_subject)
            encoded_body = urllib.parse.quote(st.session_state.current_body)
            mailto_url = f"mailto:?subject={encoded_subject}&body={encoded_body}"
            st.link_button("✉️ Open in Email App", mailto_url, use_container_width=True)

        with btn_col2:
            if st.button("🔄 Regenerate Variety", use_container_width=True):
                # Trigger regeneration
                st.session_state.edit_mode = False
                st.rerun()

        # Quick Refinement Buttons
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<span style='font-size: 13px; font-weight: 600; color: #64748b;'>⚡ One-Click Refinements:</span>", unsafe_allow_html=True)
        ref_col1, ref_col2, ref_col3 = st.columns(3)

        with ref_col1:
            if st.button("✂️ Make Shorter", use_container_width=True):
                with st.spinner("Condensing draft..."):
                    refine_prompt = f"Rewrite the following email to be significantly shorter and more concise (under 80-100 words), keeping only essential points and a clear subject line:\n\nSubject: {st.session_state.current_subject}\n\n{st.session_state.current_body}"
                    try:
                        res = ollama.chat(
                            model=selected_model,
                            messages=[
                                {"role": "system", "content": "You are an executive email editor. Output ONLY the condensed email starting with Subject: ."},
                                {"role": "user", "content": refine_prompt}
                            ]
                        )
                        s, b = parse_email_response(res["message"]["content"])
                        st.session_state.current_subject = s
                        st.session_state.current_body = b
                        st.session_state.email_history.insert(0, {
                            "timestamp": datetime.now().strftime("%I:%M %p"),
                            "subject": s,
                            "body": b,
                            "recipient": st.session_state.recipient_input,
                            "tone": "Shorter & Condensed"
                        })
                        st.rerun()
                    except Exception as err:
                        st.error(f"Refinement error: {err}")

        with ref_col2:
            if st.button("👔 More Formal", use_container_width=True):
                with st.spinner("Elevating tone..."):
                    refine_prompt = f"Rewrite the following email to have a highly formal, polished, executive tone while preserving all information:\n\nSubject: {st.session_state.current_subject}\n\n{st.session_state.current_body}"
                    try:
                        res = ollama.chat(
                            model=selected_model,
                            messages=[
                                {"role": "system", "content": "You are an executive email editor. Output ONLY the refined email starting with Subject: ."},
                                {"role": "user", "content": refine_prompt}
                            ]
                        )
                        s, b = parse_email_response(res["message"]["content"])
                        st.session_state.current_subject = s
                        st.session_state.current_body = b
                        st.session_state.email_history.insert(0, {
                            "timestamp": datetime.now().strftime("%I:%M %p"),
                            "subject": s,
                            "body": b,
                            "recipient": st.session_state.recipient_input,
                            "tone": "Formal & Executive"
                        })
                        st.rerun()
                    except Exception as err:
                        st.error(f"Refinement error: {err}")

        with ref_col3:
            if st.button("🌟 Add Warmth", use_container_width=True):
                with st.spinner("Adding warm tone..."):
                    refine_prompt = f"Rewrite the following email to be warm, friendly, appreciative, and collaborative while staying professional:\n\nSubject: {st.session_state.current_subject}\n\n{st.session_state.current_body}"
                    try:
                        res = ollama.chat(
                            model=selected_model,
                            messages=[
                                {"role": "system", "content": "You are an executive email editor. Output ONLY the warm email starting with Subject: ."},
                                {"role": "user", "content": refine_prompt}
                            ]
                        )
                        s, b = parse_email_response(res["message"]["content"])
                        st.session_state.current_subject = s
                        st.session_state.current_body = b
                        st.session_state.email_history.insert(0, {
                            "timestamp": datetime.now().strftime("%I:%M %p"),
                            "subject": s,
                            "body": b,
                            "recipient": st.session_state.recipient_input,
                            "tone": "Warm & Friendly"
                        })
                        st.rerun()
                    except Exception as err:
                        st.error(f"Refinement error: {err}")

        # Quick Copy Card
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        with st.expander("📋 View Raw / One-Click Copy", expanded=False):
            st.caption("Click the copy icon on the top right of the code block:")
            st.code(full_email_text, language="markdown")

    else:
        # Clean Empty State
        st.markdown("""
        <div class="empty-state-box">
            <span class="empty-icon">✉️</span>
            <div class="empty-title">Ready to Draft Your Email</div>
            <div class="empty-desc">
                Fill in the recipient, purpose, and key points on the left — or select a <b>Quick Template</b> from the sidebar — then click <b>Generate Professional Email</b>.
            </div>
            <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-top: 12px;">
                <span class="meta-chip">🔒 100% Private Local AI</span>
                <span class="meta-chip">⚡ Instant Streaming</span>
                <span class="meta-chip">🎯 Clear Subject Lines</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# REVISION HISTORY (BOTTOM DRAWER)
# ==========================================
if len(st.session_state.email_history) > 1:
    st.markdown("---")
    with st.expander(f"📜 Draft Revision History ({len(st.session_state.email_history)} versions saved in this session)", expanded=False):
        for idx, item in enumerate(st.session_state.email_history):
            st.markdown(f"**Version {len(st.session_state.email_history) - idx}** — `{item['timestamp']}` | Tone: *{item['tone']}* | Recipient: *{item['recipient']}*")
            st.markdown(f"**Subject:** {item['subject']}")
            st.text(item["body"][:200] + ("..." if len(item["body"]) > 200 else ""))
            col_restore, _ = st.columns([2, 10])
            with col_restore:
                if st.button(f"Restore Version {len(st.session_state.email_history) - idx}", key=f"restore_{idx}"):
                    st.session_state.current_subject = item["subject"]
                    st.session_state.current_body = item["body"]
                    st.rerun()
            st.markdown("---")

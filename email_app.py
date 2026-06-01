import streamlit as st
import anthropic

# Page setup
st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="centered"
)

# ===== MOBILE FRIENDLY STYLE =====
st.markdown("""
    <style>
        .block-container {
            padding: 1rem 1rem;
            max-width: 800px;
        }
        .stTextInput input {
            font-size: 16px;
        }
        .stSelectbox select {
            font-size: 16px;
        }
        .stButton button {
            font-size: 18px;
            padding: 12px;
        }
        @media (max-width: 600px) {
            h1 {
                font-size: 24px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ===== SESSION STATE =====
if "email_history" not in st.session_state:
    st.session_state.email_history = []

# ===== HEADER =====
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0'>
        <h1>📧 AI Email Assistant</h1>
        <p style='color: gray; font-size: 14px;'>Built by <b>Ahmed Abdullahi</b> — AI Specialist</p>
        <p style='color: gray; font-size: 13px;'>Generate professional emails in seconds using AI</p>
    </div>
""", unsafe_allow_html=True)

# ===== MODE SELECTOR =====
mode = st.radio("What do you want to do?",
                ["✍️ Write a new email", "↩️ Reply to an email"],
                horizontal=True)

st.markdown("---")

# ===== INPUTS =====
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("🎨 Tone", [
        "Professional", "Friendly", "Formal",
        "Apologetic", "Persuasive", "Grateful"
    ])
with col2:
    language = st.selectbox("🌍 Language", [
        "English", "Arabic", "French", "Spanish", "Dutch"
    ])

email_type = st.selectbox("📌 Email Type", [
    "Job Application", "Follow Up", "Thank You",
    "Complaint", "Request", "Introduction",
    "Meeting Request", "Resignation"
])

recipient = st.text_input("👤 Recipient (e.g. Hiring Manager, Client)")
your_name = st.text_input("✍️ Your Name")
your_job = st.text_input("💼 Your Job Title")
your_company = st.text_input("🏢 Your Company (optional)")

# ===== REPLY MODE =====
original_email = ""
if mode == "↩️ Reply to an email":
    original_email = st.text_area(
        "📩 Paste the email you want to reply to",
        height=150,
        placeholder="Paste the original email here..."
    )

# ===== GENERATE BUTTON =====
if st.button("🚀 Generate Email", use_container_width=True):
    if not recipient or not your_name:
        st.warning("⚠️ Please fill in at least the recipient and your name!")
    elif mode == "↩️ Reply to an email" and not original_email:
        st.warning("⚠️ Please paste the original email to reply to!")
    else:
        if mode == "↩️ Reply to an email":
            prompt = f"""Write a {tone} reply to this email in {language}.
Original email: {original_email}
Sign off with name: {your_name}, job title: {your_job}, company: {your_company}.
Do not use ANY placeholders. Do not use markdown formatting."""
        else:
            prompt = f"""Write a {tone} {email_type} email to {recipient} in {language}.
Sign off with name: {your_name}, job title: {your_job}, company: {your_company}.
Do not use ANY placeholders. Do not use markdown formatting."""

        with st.spinner("✍️ Writing your email..."):
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

        email_text = message.content[0].text

        with st.spinner("💡 Generating subject line..."):
            subject_message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=100,
                messages=[{"role": "user", "content": f"Generate one short professional email subject line for this email. Reply with ONLY the subject line, nothing else:\n\n{email_text}"}]
            )
        subject_line = subject_message.content[0].text.strip()

        st.success("✅ Email ready!")

        # Subject line
        st.markdown("**💡 Suggested Subject Line:**")
        st.info(subject_line)

        # Email text area
        st.text_area("📨 Your Email", email_text,
                     height=400, key="email_output")

        # Copy to clipboard using Streamlit button
        if st.button("📋 Copy to Clipboard", key="copy_btn"):
            st.write(
                "✅ Use Command+A then Command+C inside the email box above to copy!")

        # Download button
        st.download_button(
            label="💾 Download Email",
            data=email_text,
            file_name="my_email.txt",
            mime="text/plain",
            use_container_width=True
        )

        # Save to history
        st.session_state.email_history.append({
            "type": email_type if mode == "✍️ Write a new email" else "Reply",
            "language": language,
            "subject": subject_line,
            "email": email_text
        })

# ===== EMAIL HISTORY =====
if st.session_state.email_history:
    st.markdown("---")
    st.markdown("### 📋 Email History")
    for i, item in enumerate(reversed(st.session_state.email_history)):
        with st.expander(f"📧 Email {len(st.session_state.email_history) - i} — {item['type']} — {item['language']}"):
            st.markdown(f"**Subject:** {item['subject']}")
            st.text(item["email"])

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 13px; padding: 10px 0'>
        <p>Built by <b>Ahmed Abdullahi</b> — AI Specialist</p>
        <p>📧 Contact: qardhaas2021@gmail.com</p>
        <p style='font-size: 11px;'>Powered by Claude AI</p>
    </div>
""", unsafe_allow_html=True)

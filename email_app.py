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

# ===== BRANDING HEADER =====
st.markdown("""
    <div style='text-align: center; padding: 20px 0'>
        <h1>📧 AI Email Assistant</h1>
        <p style='font-size: 18px; color: gray;'>Built by <b>Ahmed Abdullahi</b> — AI Specialist</p>
        <p style='font-size: 14px; color: gray;'>Generate professional emails in seconds using AI</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== SESSION STATE =====
if "email_history" not in st.session_state:
    st.session_state.email_history = []

# Two columns for personal info
col1, col2 = st.columns(2)

with col1:
    your_name = st.text_input("👤 Your name")
    your_company = st.text_input("🏢 Your company")

with col2:
    your_job = st.text_input("💼 Your job title")
    recipient = st.text_input("📩 Send to")

st.markdown("### ✍️ Email details")

email_type = st.selectbox(
    "Email type",
    ["Meeting request", "Job application",
        "Follow up", "Thank you", "Apology", "Other"]
)
language = st.selectbox(
    "🌍 Language", ["English", "Arabic", "French", "Spanish", "Dutch"])
tone = st.selectbox("Tone", ["Professional", "Friendly", "Formal"])

st.markdown("---")

if st.button("✨ Generate Email", type="primary", use_container_width=True):
    if not your_name or not recipient:
        st.error("⚠️ Please fill in your name and recipient!")
    else:
        prompt = f"Write a {tone} {email_type} email to {recipient} in {language}. Sign off with the name: {your_name}, job title: {your_job}, company: {your_company}. IMPORTANT: Do not use ANY placeholders like [Name] or [Date]. Write in a general way without placeholders. Do not use markdown formatting."
        with st.spinner("✍️ Writing your email..."):
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
        st.success("✅ Email ready!")
        email_text = message.content[0].text
        st.text_area("📨 Your Email", email_text, height=400)
        st.download_button(
            label="💾 Download Email",
            data=email_text,
            file_name="my_email.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.session_state.email_history.append({
            "type": email_type,
            "language": language,
            "email": email_text
        })

# ===== EMAIL HISTORY =====
if st.session_state.email_history:
    st.markdown("---")
    st.markdown("### 📋 Email History")
    for i, item in enumerate(reversed(st.session_state.email_history)):
        with st.expander(f"📧 Email {len(st.session_state.email_history) - i} — {item['type']} — {item['language']}"):
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

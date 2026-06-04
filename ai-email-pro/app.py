import streamlit as st
from supabase import create_client, Client
import anthropic
import stripe

st.set_page_config(page_title="AI Email Pro",
                   page_icon="✉️", layout="centered")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
STRIPE_SECRET_KEY = st.secrets["STRIPE_SECRET_KEY"]
STRIPE_PRO_PRICE_ID = st.secrets["STRIPE_PRO_PRICE_ID"]
STRIPE_BUSINESS_PRICE_ID = st.secrets["STRIPE_BUSINESS_PRICE_ID"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
stripe.api_key = STRIPE_SECRET_KEY

if "user" not in st.session_state:
    st.session_state.user = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "email_count" not in st.session_state:
    st.session_state.email_count = 0
if "plan" not in st.session_state:
    st.session_state.plan = "free"


def generate_reply(email_text):
    message = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "You are a professional email assistant. Write a polite, clear, professional reply to this email:\n\n" +
                   email_text + "\n\nWrite only the reply body."}]
    )
    return message.content[0].text.strip()


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url="http://localhost:8502/?payment=success",
        cancel_url="http://localhost:8502/?payment=cancel",
    )
    return session.url


def show_auth():
    st.title("✉️ AI Email Pro")
    st.caption("Write professional email replies in seconds.")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()
    st.divider()
    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")
    if st.session_state.auth_mode == "login":
        if st.button("Log In Now", type="primary", use_container_width=True):
            try:
                result = supabase.auth.sign_in_with_password(
                    {"email": email, "password": password})
                st.session_state.user = result.user
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")
    else:
        if st.button("Create Account", type="primary", use_container_width=True):
            try:
                result = supabase.auth.sign_up(
                    {"email": email, "password": password})
                st.session_state.user = result.user
                st.rerun()
            except Exception as e:
                st.error(f"Signup failed: {e}")


def show_app():
    params = st.query_params
    if params.get("payment") == "success":
        st.session_state.plan = "pro"
        st.success("Payment successful! You are now on the Pro plan!")
        st.query_params.clear()
    st.title("✉️ AI Email Pro")
    st.caption("Logged in as: " + st.session_state.user.email)
    if st.session_state.plan == "free":
        st.info("Free Plan - " + str(st.session_state.email_count) +
                "/3 emails used this session")
    elif st.session_state.plan == "pro":
        st.success("Pro Plan - Unlimited emails!")
    elif st.session_state.plan == "business":
        st.success("Business Plan - Priority access!")
    st.divider()
    if st.session_state.plan == "free":
        st.subheader("Upgrade Your Plan")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Pro Plan")
            st.markdown("**9 euro/month**")
            st.markdown("Unlimited email replies")
            st.markdown("All languages")
            st.markdown("Priority support")
            if st.button("Upgrade to Pro", use_container_width=True, type="primary"):
                try:
                    url = create_checkout_session(STRIPE_PRO_PRICE_ID)
                    st.markdown("[Click here to pay](" + url + ")")
                except Exception as e:
                    st.error(f"Error: {e}")
        with col2:
            st.markdown("### Business Plan")
            st.markdown("**29 euro/month**")
            st.markdown("Everything in Pro")
            st.markdown("Custom tone and style")
            st.markdown("Dedicated support")
            if st.button("Upgrade to Business", use_container_width=True):
                try:
                    url = create_checkout_session(STRIPE_BUSINESS_PRICE_ID)
                    st.markdown("[Click here to pay](" + url + ")")
                except Exception as e:
                    st.error(f"Error: {e}")
        st.divider()
    st.subheader("Generate Email Reply")
    email_input = st.text_area("Paste the email you received:", height=200)
    if st.button("Generate Reply", type="primary", use_container_width=True):
        if st.session_state.plan == "free" and st.session_state.email_count >= 3:
            st.warning(
                "You have used all 3 free emails. Please upgrade to continue!")
        elif not email_input.strip():
            st.warning("Please paste an email first.")
        else:
            with st.spinner("Writing your reply..."):
                try:
                    reply = generate_reply(email_input)
                    st.session_state.email_count += 1
                    st.divider()
                    st.subheader("Your Professional Reply:")
                    st.text_area("Reply:", value=reply, height=250)
                    st.success("Done! Copy your reply above.")
                    st.download_button(label="Download Reply", data=reply,
                                       file_name="email_reply.txt", mime="text/plain", use_container_width=True)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    st.divider()
    if st.button("Log Out", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.email_count = 0
        st.session_state.plan = "free"
        st.rerun()


if st.session_state.user is None:
    show_auth()
else:
    show_app()

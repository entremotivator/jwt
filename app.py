import streamlit as st
import jwt
import datetime

st.set_page_config(page_title="JWT Token Creator", layout="centered")

st.title("🔐 JWT Token Creator")

# Secret key input
secret = st.text_input("Secret Key", type="password")

# Algorithm selection
algorithm = st.selectbox("Algorithm", options=["HS256", "HS384", "HS512"])

# Payload fields
st.subheader("Payload")
username = st.text_input("Username")
email = st.text_input("Email")
is_admin = st.checkbox("Is Admin")
exp_minutes = st.number_input("Expiration (in minutes)", min_value=1, value=60)

# Generate button
if st.button("Generate JWT Token"):
    if not secret:
        st.error("Secret key is required.")
    else:
        try:
            payload = {
                "username": username,
                "email": email,
                "is_admin": is_admin,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)
            }
            token = jwt.encode(payload, secret, algorithm=algorithm)
            st.success("JWT Token Generated!")
            st.code(token, language="bash")
        except Exception as e:
            st.error(f"Error generating token: {e}")

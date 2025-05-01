import streamlit as st
import jwt
import datetime
import os

# Ensure the app directory exists
app_dir = "/home/ubuntu/vapi_jwt_app"
os.makedirs(app_dir, exist_ok=True)

# --- VAPI Configuration ---
# Use Streamlit secrets or environment variables for sensitive data in a real app
# For this example, we'll use input fields
st.title("Vapi AI JWT Token Generator")

st.header("Configuration")
org_id = st.text_input("Vapi Organization ID", "64cf641a-39f2-411f-9926-bf28e93d1fb3") # Example ID from user's code
secret_key = st.text_input("Vapi Secret Key", "ad6c5243-9548-4231-9d04-b99c1628cc62", type="password") # Example key from user's code
token_expiry_minutes = st.number_input("Token Expiry (minutes)", min_value=1, max_value=60, value=10)

def generate_jwt(org_id, secret, expiry_minutes):
    """Generates a JWT token for Vapi AI."""
    if not org_id or not secret:
        return "Error: Please provide both Organization ID and Secret Key."

    try:
        now = datetime.datetime.now(datetime.UTC)
        exp_time = now + datetime.timedelta(minutes=expiry_minutes)

        payload = {
            "orgId": org_id,
            "iat": int(now.timestamp()),
            "exp": int(exp_time.timestamp())
        }

        token = jwt.encode(payload, secret, algorithm='HS256')

        # PyJWT >= 2 returns str, older versions might return bytes
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token
    except jwt.exceptions.InvalidKeyError:
         return "Error: Invalid Secret Key format. Ensure it's a valid string."
    except Exception as e:
        # Catch potential errors during encoding
        return f"Error generating token: {str(e)}"

st.header("Generate Token")
if st.button("Generate VAPI Bearer Token"):
    if org_id and secret_key:
        token = generate_jwt(org_id, secret_key, token_expiry_minutes)
        st.subheader("Generated Token")
        if token.startswith("Error:"):
             st.error(token)
        else:
             st.text_area("Bearer Token (JWT):", token, height=150)
             st.success("Token generated successfully!")

        st.subheader("Payload Used")
        # Recreate payload for display purposes
        now_display = datetime.datetime.now(datetime.UTC)
        exp_display = now_display + datetime.timedelta(minutes=token_expiry_minutes)
        payload_display = {
            "orgId": org_id,
            "iat": int(now_display.timestamp()),
            "exp": int(exp_display.timestamp())
        }
        st.json(payload_display)
    else:
        st.warning("Please enter both Organization ID and Secret Key above.")

st.sidebar.header("About")
st.sidebar.info(
    "This app generates JWT Bearer tokens required for authenticating with the Vapi AI API. "
    "Enter your Vapi Organization ID and Secret Key, set the desired token expiry time, and click the button to generate the token."
)
st.sidebar.header("Important Notes")
st.sidebar.warning(
    "Keep your Secret Key confidential. Do not share it publicly. "
    "Consider using environment variables or Streamlit secrets for production deployment."
)



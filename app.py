import streamlit as st
import jwt
import datetime
import os

# --- VAPI Configuration ---
st.title("Vapi AI JWT Token Generator (Updated)")

st.header("Configuration")
org_id = st.text_input("Vapi Organization ID", "64cf641a-39f2-411f-9926-bf28e93d1fb3") # Example ID from user input
secret_key = st.text_input("Vapi Secret Key (for HS256)", "ad6c5243-9548-4231-9d04-b99c1628cc62", type="password") # Example key from user input
token_expiry_minutes = st.number_input("Token Expiry (minutes)", min_value=1, max_value=1440, value=60) # Default 1 hour
token_scope = st.selectbox("Token Scope", ["private", "public"], index=0) # Default to private

def generate_jwt_hs256(org_id, secret, expiry_minutes, scope):
    """Generates a JWT token for Vapi AI using HS256 and the new payload structure."""
    if not org_id or not secret:
        return "Error: Please provide both Organization ID and Secret Key."

    try:
        now = datetime.datetime.now(datetime.UTC)
        exp_time = now + datetime.timedelta(minutes=expiry_minutes)

        # Construct payload based on Vapi documentation
        payload = {
            "orgId": org_id,
            "token": {
                "tag": scope
            },
            # Standard JWT claims
            "iat": int(now.timestamp()),
            "exp": int(exp_time.timestamp())
        }

        # Generate token using HS256
        token = jwt.encode(payload, secret, algorithm=\'HS256\')

        # PyJWT >= 2 returns str, older versions might return bytes
        if isinstance(token, bytes):
            token = token.decode(\'utf-8\')
        return token, payload # Return token and payload used
    except jwt.exceptions.InvalidKeyError:
         return "Error: Invalid Secret Key format for HS256. Ensure it\'s a valid string.", None
    except Exception as e:
        # Catch potential errors during encoding
        return f"Error generating token: {str(e)}", None

st.header("Generate Token")
if st.button(f"Generate {token_scope.capitalize()} VAPI Token (HS256)"):
    if org_id and secret_key:
        result, payload_used = generate_jwt_hs256(org_id, secret_key, token_expiry_minutes, token_scope)

        st.subheader("Generated Token")
        if isinstance(result, str) and result.startswith("Error:"):
             st.error(result)
        elif result:
             st.text_area(f"Bearer Token (JWT - {token_scope.capitalize()} Scope):", result, height=150)
             st.success("Token generated successfully using HS256!")
             st.subheader("Payload Used")
             st.json(payload_used)
        else:
            st.error("An unexpected error occurred during token generation.")

    else:
        st.warning("Please enter both Organization ID and Secret Key above.")

st.sidebar.header("About")
st.sidebar.info(
    "This app generates JWT Bearer tokens for Vapi AI using the HS256 algorithm and the payload structure specified in the Vapi docs (including token scope). "
    "Enter your Vapi Organization ID and Secret Key, select scope/expiry, and generate."
)
st.sidebar.header("Important Notes")
st.sidebar.warning(
    "This version uses HS256 based on the provided secret key. If Vapi requires RS256, a proper PEM private key will be needed. "
    "Keep your Secret Key confidential."
)


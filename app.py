import streamlit as st
import jwt  # Make sure this is PyJWT, not your script name
import datetime

# Define a payload with dynamic iat/exp for better testing
payload = {
    "orgId": "64cf641a-39f2-411f-9926-bf28e93d1fb3",
    "iat": int(datetime.datetime.utcnow().timestamp()),
    "exp": int((datetime.datetime.utcnow() + datetime.timedelta(minutes=10)).timestamp())
}

# Set your secret key
secret = 'ad6c5243-9548-4231-9d04-b99c1628cc62'

def generate_jwt(payload, secret):
    try:
        token = jwt.encode(payload, secret, algorithm='HS256')
        # PyJWT>=2 returns a str, older versions return bytes
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token
    except Exception as e:
        return f"Error generating token: {str(e)}"

# Streamlit UI
st.sidebar.header('Payload and Secret Key')
st.sidebar.json(payload)
st.sidebar.write('Secret:', secret)

if st.button('Generate JWT'):
    token = generate_jwt(payload, secret)
    st.text_area('Generated JWT:', token, height=150)



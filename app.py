import streamlit as st
import jwt

# Define a payload with the provided orgId, iat, and exp
payload = {
    "orgId": "64cf641a-39f2-411f-9926-bf28e93d1fb3",
    "iat": 1746074705,
    "exp": 1746075305
}

# Set your secret key
secret = 'ad6c5243-9548-4231-9d04-b99c1628cc62'

def generate_jwt(payload, secret):
    # Generate the token
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

# Streamlit UI
st.sidebar.header('Payload and Secret Key')
st.sidebar.write('Payload:', payload)
st.sidebar.write('Secret:', secret)

if st.button('Generate JWT'):
    token = generate_jwt(payload, secret)
    st.text('Generated JWT:')
    st.text(token)



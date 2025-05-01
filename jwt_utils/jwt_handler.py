# jwt_utils/jwt_handler.py

import jwt
import datetime

# Function to encode a JWT token
def encode_jwt(payload: dict, secret: str, algorithm="HS256", exp_minutes=60):
    """
    Encode a dictionary payload to JWT token.

    :param payload: The payload data to encode
    :param secret: The secret key to sign the token
    :param algorithm: The encoding algorithm (default: HS256)
    :param exp_minutes: Token expiration in minutes (default: 60 minutes)
    :return: Encoded JWT token
    """
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)
    return jwt.encode(payload, secret, algorithm=algorithm)


# Function to decode a JWT token
def decode_jwt(token: str, secret: str, algorithms=["HS256"]):
    """
    Decode a JWT token.

    :param token: The JWT token to decode
    :param secret: The secret key used to decode the token
    :param algorithms: List of acceptable algorithms (default: HS256)
    :return: Decoded JWT payload or error message
    """
    try:
        decoded_payload = jwt.decode(token, secret, algorithms=algorithms)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}

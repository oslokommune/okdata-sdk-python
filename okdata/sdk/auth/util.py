from datetime import datetime

import jwt


def is_token_expired(token):
    return is_expired(get_expired_timestamp(token))


def is_expired(timestamp):
    expires_dt = datetime.utcfromtimestamp(timestamp)

    difference = expires_dt - datetime.utcnow()

    if difference.total_seconds() < 10:
        return True

    return False


def decode_token(token):
    return jwt.decode(token, options={"verify_signature": False})


def get_expired_timestamp(token):
    return decode_token(token)["exp"]

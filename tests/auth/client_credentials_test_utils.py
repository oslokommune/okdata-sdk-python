import jwt
from datetime import datetime
from dateutil import parser

utc_now = parser.parse("2019-11-01T10:00:30+00:00")
not_expired_time = parser.parse("2019-11-01T10:00:41+00:00")
expired_time = parser.parse("2019-11-01T10:00:39+00:00")

not_expired = {"exp": datetime.timestamp(not_expired_time)}

expired = {"exp": datetime.timestamp(expired_time)}

not_expired_token = jwt.encode(not_expired, "secret", algorithm="HS256")
expired_token = jwt.encode(expired, "secret", algorithm="HS256")

default_test_client_credentials = {
    "access_token": not_expired_token,
    "refresh_token": not_expired_token,
}

from_cache_not_expired = {"exp": not_expired_time, "source": "cache"}
from_cache_expired = {"exp": expired_time, "source": "cache"}

from_cache_not_expired_token = jwt.encode(
    from_cache_not_expired, "secret", algorithm="HS256"
)
from_cache_expired_token = jwt.encode(from_cache_expired, "secret", algorithm="HS256")

import jwt
from datetime import datetime
from dateutil import parser

utc_now = parser.parse("2019-11-01T10:00:30+00:00")
_not_expired_time = parser.parse("2019-11-01T10:00:41+00:00")
_expired_time = parser.parse("2019-11-01T10:00:39+00:00")

_not_expired = {"exp": datetime.timestamp(_not_expired_time)}
_expired = {"exp": datetime.timestamp(_expired_time)}

not_expired_token = jwt.encode(_not_expired, "secret", algorithm="HS256")
expired_token = jwt.encode(_expired, "secret", algorithm="HS256")

default_test_client_credentials = {
    "access_token": not_expired_token,
    "refresh_token": not_expired_token,
}

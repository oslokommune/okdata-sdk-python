# TODO: Use these simplified dataclasses once support for Python 3.6 is
# dropped. Meanwhile we'll use the "polyfill" classes defined below.
#
# from dataclasses import dataclass, field
#
# @dataclass
# class Client:
#     user_id: str
#     user_type: str = field(default="client", init=False)
#
#
# @dataclass
# class Team:
#     user_id: str
#     user_type: str = field(default="team", init=False)
#
#
# @dataclass
# class User:
#     user_id: str
#     user_type: str = field(default="user", init=False)


class Client:
    user_id: str
    user_type: str

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_type = "client"


class Team:
    user_id: str
    user_type: str

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_type = "team"


class User:
    user_id: str
    user_type: str

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_type = "user"


def asdict(obj):
    return obj.__dict__

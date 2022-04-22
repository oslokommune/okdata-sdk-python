from dataclasses import dataclass, field


@dataclass
class Client:
    user_id: str
    user_type: str = field(default="client", init=False)


@dataclass
class Team:
    user_id: str
    user_type: str = field(default="team", init=False)


@dataclass
class User:
    user_id: str
    user_type: str = field(default="user", init=False)

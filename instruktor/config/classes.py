from dataclasses import dataclass


@dataclass
class Endpoints:
    base_url: str
    login: str
    logout: str


@dataclass
class ApiCredentials:
    login: str
    password: str


@dataclass
class BotConfig:
    token: str

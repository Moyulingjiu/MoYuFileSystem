"""
与前端交互的object
"""

from datetime import datetime
from pydantic import BaseModel

__all__ = [
    "Result", "Login", "Register"
]


class Result(BaseModel):
    code: int
    msg: str
    data: object
    timestamp: datetime


class Login(BaseModel):
    username: str
    password: str
    remember: bool = False


class Register(BaseModel):
    username: str
    password: str
    nickname: str
    avatar: str

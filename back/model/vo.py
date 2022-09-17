"""
与前端交互的object
"""

from pydantic import BaseModel


__all__ = [
    "Login"
]


class Login(BaseModel):
    username: str
    password: str
    remember: bool = False

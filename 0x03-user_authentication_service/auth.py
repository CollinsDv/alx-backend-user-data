#!/usr/bin/env python3
"""password hashing
"""
import bcrypt
import hashlib
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hashed passwords of abitraty length
    Args:
        password: password to be hashed
    Returns:
        bytes sized irreversible hash value
    """
    return bcrypt.hashpw(
            hashlib.sha256(password.encode()).digest(),
            bcrypt.gensalt()
            )


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers user
        Args
            email: user email
            password: user credentials
        Returns:
            user object or raise valueerror
        """
        # check if user exists
        if self._db._session.query(User).filter_by(email=email).first():
            raise ValueError(f"User {email} already exists")

        hashed_pwd = _hash_password(password)

        return self._db.add_user(email, hashed_pwd)

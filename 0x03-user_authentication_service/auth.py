#!/usr/bin/env python3
"""password hashing
"""
import bcrypt
from db import DB
import uuid
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashed passwords of abitraty length
    Args:
        password: password to be hashed
    Returns:
        bytes sized irreversible hash value
    """
    return bcrypt.hashpw(
            password.encode(),
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
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_pwd = _hash_password(password)

        return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """validates a user
        Args:
            email: The user's email.
            password: The user's plaintext password.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        user = self._db.find_user_by(email=email)
        if user is None:
            return False

        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def _generate_uuid(self):
        """generates unique id
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """creates a session id
        Args:
            email: email id
        Returns:
            session id related to the user
        """
        user = self._db.find_user_by(email=email)

        if user:
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()

            return session

        return None

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
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
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
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            pass
        else:
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()

            return session_id

        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """returns a user based on a session_id
        Args:
            session_id: session id for obtaining user
        Returns:
            User object or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """updates user's session id to None
        Args:
            user_id: a user's identification number
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

	def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates Users password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_password = _hash_password(password).decode('utf-8')
            self._db.update_user(user.id, hashed_password=new_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError

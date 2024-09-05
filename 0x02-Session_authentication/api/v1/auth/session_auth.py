#!/usr/bin/env python3
"""session auth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from os import getenv


class SessionAuth(Auth):
    """the session class implementation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id
        Args:
            user_id
        Returns:
            uuid string
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a session id for a user id
        Args:
            session_id: session to retrieve a user sessionid
        Returns:
            user id associated with a session_id
        """
        if session_id is None and isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value
        """
        sess_id = self.session_cookie(request)  # get session id from cookie

        # get user id from session
        user_id = self.user_id_by_session_id.get(sess_id)

        return User.get(user_id)  # get the user from storage

    def destroy_session(self, request=None):
        """destroys a session
        """
        if request is None:
            return False

        session_id = request.cookies.get(getenv('SESSION_NAME'))
        if session_id is None:
            return False

        session_id_key = self.user_id_for_session_id(session_id)
        if session_id_key is None:
            return False

        del self.user_id_by_session_id[session_id_key]

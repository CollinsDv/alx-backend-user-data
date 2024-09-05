#!/usr/bin/env python3
"""session auth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
        user_id_by_session_id[session_id] = user_id

        return session_id

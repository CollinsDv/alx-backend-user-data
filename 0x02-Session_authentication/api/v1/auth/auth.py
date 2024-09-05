#!/usr/bin/env python3
"""auth class definition
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to implement authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication
        Args:
            path: path to examine
            excluded_paths: list of unauthorized links
        Returns
            Boolean if path is authorized or not
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize path to ensure it ends with a '/'
        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Args:
            request: Flask request object
        Returns:
            the authorization header contents or None
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """pass
        request: Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """returns cookie value from a request
        """
        # cookie = request.cookie  # get cookie name

        if request is None:
            return None

        return request.cookies.get('_my_session_id')

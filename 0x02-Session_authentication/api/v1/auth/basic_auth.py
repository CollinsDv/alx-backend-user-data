#!/usr/bin/env python3
"""basic_auth class implementation
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Auth implementation
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        for a Basic Authentication
        Args:
            authorization_header: the http authorization header tag
        Returns:
            value after Basic that contains the decoded string else None
        """
        if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decodes base64_authorization_header back to Base64 string
        Args:
            base64_authorization_header: base64 encoded string
        Returns:
            base64 decode string of base64_authorization_header else None
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None

        try:
            return base64.b64decode(
                    base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from
        the Base64 decoded value.
        Args:
            decoded_base64_authorization_header: string to extract user data
        Returns:
            A tuple of the user email and password or None tuple values
        """
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ':' not in decoded_base64_authorization_header:
            return (None, None)

        # split the list based on the colon and convert the list
        # to a tuple
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns user obj if user_email in storage
        """
        user = User()
        user.load_from_file()

        # handle no users in store and empty variables
        if user.count() == 0 or\
                user_email is None or not isinstance(user_email, str) or\
                user_pwd is None or not isinstance(user_pwd, str):
            return None

        # search user by email
        user_obj = user.search({'email': user_email})
        if len(user_obj) == 0:  # user email not found
            return None

        for user in user_obj:
            if user.is_valid_password(user_pwd):
                return user

        return None  # incorrect password

    def current_user(self,
                     request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request
        Args:
            request: Flask request object
        Returns:
            User instance if found, None otherwise
        """
        # Step 1: Get the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Step 2: Extract the Base64 part of the Authorization header
        base64_credentials = self.extract_base64_authorization_header(
                auth_header)
        if base64_credentials is None:
            return None

        # Step 3: Decode the Base64 string
        decoded_credentials = self.decode_base64_authorization_header(
                base64_credentials)
        if decoded_credentials is None:
            return None

        # Step 4: Extract email and password from the decoded string
        email, password = self.extract_user_credentials(
                decoded_credentials)
        if email is None or password is None:
            return None

        # Step 5: Retrieve the User object
        user = self.user_object_from_credentials(email, password)
        return user

#!/usr/bin/env python3
"""password hashing function
"""
import bcrypt
import base64
import hashlib


def _hash_password(password: str) -> bytes:
    """hashed passwords of abitraty length
    Args:
        password: password to be hashed
    Returns:
        bytes sized irreversible hash value
    """
    return bcrypt.hashpw(
            base64.b64encode(
                hashlib.sha256(password.encode()).digest()),
                bcrypt.gensalt()
            )

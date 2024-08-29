#!/usr/bin/env python3
"""module: encrypt_password
Implement a hash_password function that expects one string
argument name password and returns a salted, hashed password,
which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).
"""
import bcrypt
import base64
import hashlib


def hash_password(password: str) -> bytes:
    """
    returns a salted, hashed password, which is a byte string.
    Args:
        password (str) -> password
    Returns
        hashed password in bytes
    """
    return bcrypt.hashpw(
            base64.b64encode(hashlib.sha256(password.encode()).digest()),
            bcrypt.gensalt()
            )

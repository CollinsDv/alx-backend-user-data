#!/usr/bin/env python3
"""Basic flask app
"""
from flask import Flask, jsonify
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=["POST"])
def users(email: str, password: str):
    """registers users and uses auth proxy
    Args:
        email: user email
        password: user password
    """
    try:
        AUTH.register_user(email, password)
    catch ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({f"email": {email}, "message": "user created"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

#!/usr/bin/env python3
"""session auth view
"""

from flask import request, make_response, jsonify
from api.v1.views import app_views, User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sesh_auth():
    """Handles all routes for the Session authentication"""
    user_email = request.form.get('email')
    if user_email is None:
        return make_response(jsonify({'error': 'email missing'}), 400)

    user_pwd = request.form.get('password')
    if user_pwd is None:
        return make_response(jsonify({'error': 'password missing'}), 400)
    print(user_email)
    users = User.search({'email': user_email})
    print(users)
    if len(users) == 0:
        return make_response(jsonify(
            {'error': 'no user found with this email'}), 404)

    if not users[0].is_valid_password(user_pwd):
        return make_response(jsonify({'error': 'wrong password'}), 401)

    from api.v1.app import auth

    session_id = auth.create_session(users[0].id)

    res = make_response(jsonify(users[0].to_json()))

    # set cookie with environment variable SESSION_NAME
    # during app run
    res.set_cookie(getenv('SESSION_NAME'), session_id)

    return res


@app_views.route('auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """logout a deletes a session
    """
    from api.v1.app import auth
    auth.destroy_session(request)

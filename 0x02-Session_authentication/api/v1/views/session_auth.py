#!/usr/bin/env python3
"""session auth view
"""

from api.v1.views import app_views
from flask import request, make_response


@app_views.route('auth_session/login',
                 methods=['POST'], strict_slashes=False)
def sesh_auth():
    """handles all routes for the Session authentication
    """
    user_email = request.form.get('email')
    if user_email is None:
        return make_response({'error': 'email missing'}), 400

    user_pwd = request.form.get('password')
    if user_pwd is None:
        return make_response({'error': 'password missing'}), 400

    from api.v1.views import User
    user = User.search({'email': user_email})

    if len(user) == 0:
        return make_response(
                {'error': 'no user found with this email'}
                ), 400

    if user[0].is_valid_password(user_pwd) is False:
        return make_response(
                {'error': 'wrong password'}
                )

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    res = make_response(user.to_json())

    # set cookie with environment variable SESSION_NAME
    # during app run
    res.set_cookie(get_env('SESSION_NAME'), session_id)

    return res

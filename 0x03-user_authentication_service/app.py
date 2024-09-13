#!/usr/bin/env python3
"""Basic flask app
"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=["POST"])
def users():
    """registers users and uses auth proxy
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions():
    """creates sessions
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    sesh_id = AUTH.create_session(email)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', sesh_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """destroys a user's session id
    """
    sesh_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sesh_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', strict_slashes=False)
def profile():
    """gets a user profile
    """
    sesh_id = request.cookies.get('session_id')
    if sesh_id
        user = AUTH.get_user_from_session_id(sesh_id)

        if user:
            return jsonify({"email": user.email})

    return abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get a reset password token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Update a user password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

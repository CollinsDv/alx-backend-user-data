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
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

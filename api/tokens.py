from flask import jsonify
from api import app, db
from api.auth import basic_auth, token_auth

# Generate user tokens
@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

# Clients can send a DELETE request to the /tokens URL to invalidate the token.
@app.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204
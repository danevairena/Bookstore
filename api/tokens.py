from flask import jsonify
from api import app, db
from api.auth import basic_auth

# Generate user tokens
@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

# placeholders
def get_token():
    pass

def revoke_token():
    pass
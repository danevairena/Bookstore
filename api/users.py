from flask import jsonify
from api import app
from api.models import User

# Retrieve a single user, given by id
# The view function receives the id for the requested user as a dynamic argument in the URL.
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    # The advantage of get_or_404() over get() is that it removes the need to check the result of the query -
    # when the id does not exist, it aborts the request and returns a 404 error to the client.
    return jsonify(User.query.get_or_404(id).to_dict())

@app.route('/users', methods=['GET'])
def get_users():
    pass

@app.route('/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass

@app.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass

@app.route('/users', methods=['POST'])
def create_user():
    pass

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
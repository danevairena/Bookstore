from flask import jsonify, request, url_for, abort
from api import app, db
from api.models import User
from api.errors import bad_request
from api.auth import token_auth

# Retrieve a single user, given by id
# The view function receives the id for the requested user as a dynamic argument in the URL.
@app.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    # The advantage of get_or_404() over get() is that it removes the need to check the result of the query -
    # when the id does not exist, it aborts the request and returns a 404 error to the client.
    return jsonify(User.query.get_or_404(id).to_dict())

# Return the collection of all users.
@app.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    # The page and per_page arguments are then passed to the to_collection_query() method, along with the query, 
    # which in this case is simply User.query, the most generic query that returns all users.
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

# Endpoint that returns the followers
@app.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)

# Endpoint that returns the followed users
@app.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page, 'api.get_followed', id=id)
    return jsonify(data)

# The POST request to the /users route is going to be used to register new user accounts.
@app.route('/users', methods=['POST'])
def create_user():
    # Ensure that I always get a dictionary using the expression request.get_json() or {}
    data = request.get_json() or {}
    # Check if any of the fields are missing - the bad_request() helper function returns an error to the client.
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    # Check if username and email fields are not already used by another user and if any of those return a valid user - return an error back to the client.
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    # Create a user object and add it to the database
    user = User()
    # The new_user argument is set to True, so that it also accepts the password field which is normally not part of the user representation.
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    # The response that returned for this request is going to be the representation of the new user
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

# Endpoint to modify user
@app.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    # Ensure that I always get a dictionary using the expression request.get_json() or {}
    data = request.get_json() or {}
    # Validate that the username and email fields provided by the client
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    # Once the data has been validated, I can use the from_dict() method of the User model to 
    # import all the data provided by the client, and then commit the change to the database
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
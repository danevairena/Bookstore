from flask import app

# User API resource placeholders.

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

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
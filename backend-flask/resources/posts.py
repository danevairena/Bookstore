# contains logic for /Posts

# reqparse - request parser which makes sure that when we send a request, we pass the information we need with that request
from flask_restful import Resource, reqparse, abort


# Create new request parser object that will parse though the request that's being sent
# and make sure that it fits the guidelines we've defined below and has the correct information
# Validating the request - the request parser is looking for the exact arguments 
posts_put_args = reqparse.RequestParser()
# The help value is like an error message to the user
posts_put_args.add_argument("name", type=str, help="Name of the post is reqired", required=True, location='form')
posts_put_args.add_argument("description", type=str, help="Description of the product is reqired", required=True, location='form')
posts_put_args.add_argument("price", type=int, help="Book price is reqired", required=True, location='form')


# Empty dictionary for storing information
posts = {}

# Define a function to abort if post is not found
def abort_if_id_not_found(post_id):
    if post_id not in posts:
        abort(404,message="Post id is not valid ..")

# Define abort function if post already exist and send status code 409 for already exists
def abort_if_post_exists(post_id):
    if post_id in posts:
        abort(409,message="Post with that id already exists.")

class Post(Resource):

    # Get information about post
    def get(self, post_id):
        # Check if requested post exists
        abort_if_id_not_found(post_id)
        return posts[post_id]
    
    # Create post
    def put(self, post_id):
        abort_if_post_exists(post_id)
        # Get all of the arguments and if they are not there automatically send back error message
        args = posts_put_args.parse_args()
        posts[post_id] = args
        # Send response
        # 201 status code stands for created
        return posts[post_id], 201
    
    # Delete post
    def delete (self, post_id):
        # Check if post doesn't exist
        abort_if_id_not_found(post_id)
        # Delete and return 204 status code for successful deletion 
        del posts[post_id]
        return '', 204

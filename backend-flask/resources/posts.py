# contains logic for /Posts

# reqparse - request parser which makes sure that when we send a request, we pass the information we need with that request
from flask_restful import Resource, reqparse


# Create new request parser object that will parse though the request that's being sent
# and make sure that it fits the guidelines we've defined below and has the correct information
# Validating the request - the request parser is looking for the exact arguments 
posts_put_args = reqparse.RequestParser()
# The help value is like an error message to the user
posts_put_args.add_argument("name", type=str, help="Name of the post")
posts_put_args.add_argument("description", type=str, help="Description of the product")
posts_put_args.add_argument("price", type=int, help="Book price")


# Empty dictionary for storing information
posts = {}


class Post(Resource):
    # If we send get request to the URL, where resource is accessible
    # it should reeturn hello world
    # name is parameter from the request (string that the user has typed in)
    def get(self, post_id):
        return posts[post_id]
    
    def put(self, post_id):
        # Get all of the arguments and if they are not there automatically send back error message
        args = posts_put_args.parse_args()
        # Send response
        return {post_id: args}
# This file contains your app and routes


from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


# Enable Cross Origin Resource Sharing (CORS)
from flask_cors import CORS


# Import datetime module for showing date and time
import datetime

# Import resources files
from resources.foo import Foo
from resources.hello import HelloWorld
from resources.posts import Post


x = datetime.datetime.now()
 

# Initializing flask app
app = Flask(__name__.split('.')[0])

# Include an extra API(app) instance to indicate Flask that this is a REST API web app
api = Api(app)


# Change configuration settings - define what we want the location of our database to be
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db '
# Initialize database
db = SQLAlchemy(app)



# Initialize the Flask-Cors extension with default arguments to allow CORS for all domains on all routes
# Exposes all resources matching /api/* to CORS and allows the Content-Type header, which is necessary to POST JSON
# supports_credentials - To allow cookies or authenticated requests to be made cross origins
CORS(app, resources=r'/api/*', supports_credentials=True)


# Add resource to the API and make it accessible though what URL
# We can pass arguments or kind of parameters through the request URL
# Define parameter you want to be passed in <type:name> - when you want the user to type some string after helloworld
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Post, "/post/<int:post_id>")




# Route for seeing a data
@app.route('/data')
def get_time():
 
    # Returning an api for showing in  reactjs
    return {
        'Name':"Irenaaa",
        "Date":x,
        "programming":"python"
        }
 
     
# Running app
if __name__ == '__main__':
    app.run()
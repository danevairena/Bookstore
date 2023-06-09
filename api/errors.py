# Error responses

from flask import jsonify
# The HTTP_STATUS_CODES dictionary from Werkzeug (a core dependency of Flask) provides a short descriptive name for each HTTP status code.
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
        # The jsonify() function returns a Flask Response object with a default status code of 200, 
        # so after I create the response, I set the status code to the correct one for the error
    response = jsonify(payload)
    response.status_code = status_code
    return response

# The most common error that the API is going to return is going to be the code 400, which is the error for "bad request"
def bad_request(message):
    return error_response(400, message)

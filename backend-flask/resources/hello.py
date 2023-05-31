# contains logic for /HelloWorld

from flask_restful import Resource

names = {"irena":{"age":"25", "gender":"female"},
         "jordan":{"age":"35", "gender":"male"}}

class HelloWorld(Resource):
    # If we send get request to the URL, where resource is accessible
    # it should reeturn hello world
    # name is parameter from the request (string that the user has typed in)
    def get(self, name):
        return names[name]
    def post(self):
        return {"data":"posted"}
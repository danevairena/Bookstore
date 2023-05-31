import requests

BASE = "http://127.0.0.1:5000/"


# Rather than having all the information directly in the URL which anyone can see we can send information though data
# in the form of say JSON or some other format that will actually get sent alongside of my request
response = requests.put(BASE + "post/1", {"name":"Daniel"})
print(response.json())
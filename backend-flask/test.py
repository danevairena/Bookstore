import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name":"Daniel", "description":"kid", "price":"3"},
        {"name":"Irena", "description":"adult", "price":"25"},
        {"name":"Jordan", "description":"adult", "price":"35"}]

for i in range(len(data)):
    response = requests.put(BASE + "post/" + str(i), data[i])
    print(response.json())

# Rather than having all the information directly in the URL which anyone can see we can send information though data
# in the form of say JSON or some other format that will actually get sent alongside of my request
input()
response = requests.delete(BASE + "post/0") 
print(response)
input()
response = requests.get(BASE + "post/0")
print(response.json())
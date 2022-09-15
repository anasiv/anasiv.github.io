import requests

result = requests.get("http://google.com")
print (result.text)

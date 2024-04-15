import requests

url = "https://google-reverse-image-api.vercel.app/reverse"
data = {"imageUrl": "https://i.redd.it/w52vxsl1hyn91.png"}

response = requests.post(url, json=data)

if response.ok:
    print(response.json())
else:
    print(response.status_code)
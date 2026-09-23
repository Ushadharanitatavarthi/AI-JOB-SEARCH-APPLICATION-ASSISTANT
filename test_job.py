import requests

API_KEY = "sk-live-ZtRT0b0bBXMYHTW1xHK24rX1vqQ5dN2BrhccGawn"

url = "https://jobs.indianapi.in/jobs"

headers = {
    "x-api-key": API_KEY
}

params = {
    "limit": "5"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

print("Status:", response.status_code)
print(response.json())
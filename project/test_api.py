import requests

# Test the API endpoint
response = requests.get('http://127.0.0.1:5000/recommendations?mood=happy')
print("Status Code:", response.status_code)
print("Response JSON:")
print(response.json())
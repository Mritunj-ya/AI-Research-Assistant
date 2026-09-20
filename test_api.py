import requests
url="https://api.semanticscholar.org/graph/v1/paper/search"
params={
    "query":"Large Language Model",
    "limit": 5    
}
response=requests.get(url, params=params)
print("Status Code:",response.status_code)

data=response.json()
print(type(data))
print(data.keys())
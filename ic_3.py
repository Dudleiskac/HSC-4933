import requests

YEAR = 2020
DATASET = "dec/pl"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "40b77dbbe71e4360e403b2f033e0f91b22a3cf0f"

params = {
    "get": "NAME,P1_001N",
    "for": "state:*",
     "key": API_KEY,
}

response = requests.get(URL, params=params)
response.raise_for_status()
data = response.json()

header, rows = data[0], data[1:]
print(f"Got {len(data) -1} rows back.")
for row in rows:
    print(dict(zip(header, row)))


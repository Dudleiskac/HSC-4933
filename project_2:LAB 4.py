import requests

YEAR = 2022
DATASET = "acs/acsse"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "85a80fb8cd07b4dfeb96ec95cda88b1a01b48068"

state_fips = input("Enter state fips code(s) you would like data for: ")
variable_names = input("Enter variable names you want data for:")

params = {
    "get": f"NAME,{variable_names}",
    "for": f"state:{state_fips}",
    "key": API_KEY
}
response = requests.get(URL, params=params)
response.raise_for_status()
data = response.json()

header = data[0]
rows = data[1:]

print(f"Found {len(rows)}   Rows of Data.")
print(header)
for row in rows:
    print(row)

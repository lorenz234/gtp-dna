import requests
import yaml
import pandas as pd
import os

api_key = os.getenv('DUNE_KEY')
if not api_key:
    raise ValueError("API Key not set. Ensure DUNE_KEY is configured correctly.")

# define the header for DUNE Api
headers = {
    "X-DUNE-API-KEY": api_key
}

# create & save csv file
with open('economics_da/economics_mapping.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
table = [
    [
        L2, 
        layers.get('name'),
        settlement_layer, 
        f.get('from_address'), 
        f.get('to_address'), 
        f.get('method'), 
        f.get('namespace') if settlement_layer == 'celestia' else None
    ]
    for L2, layers in data.items()
    for settlement_layer, filters in layers.items() if isinstance(filters, list)
    for f in filters
]
df = pd.DataFrame(table, columns=['l2', 'name', 'settlement_layer', 'from_address', 'to_address', 'method', 'namespace'])
df.to_csv('economics_mapping.csv', index=False)

# clear the current table:
url = "https://api.dune.com/api/v1/table/growthepie/l2economics_mapping/clear"
response = requests.request("POST", url, headers=headers)

# upload the new data
url = "https://api.dune.com/api/v1/table/growthepie/l2economics_mapping/insert"
headers['Content-Type'] = "text/csv"
with open("./economics_mapping.csv", "rb") as data:
  response = requests.request("POST", url, data=data, headers=headers)
  print(response.json())

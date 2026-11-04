import json
import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

params = {
    "keywordSearch": "Apache",
    "resultsPerpage": 5,
}

response = requests.get(URL, params=params, timeout=30)
print(response.status_code)

data = response.json()
print(data["totalResults"])

first = data["vulnerabilities"][0]

print(json.dumps(first, indent=2, ensure_ascii=False)[:2000])

import json
from datetime import datetime, timedelta
import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DAYS = 30
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000"

now = datetime.now()
start = now - timedelta(days=DAYS)

params = {
    "keywordSearch": "Apache",
    "resultsPerPage": 20,
    "pubStartDate": start.strftime(DATE_FORMAT),
    "pubEndDate": now.strftime(DATE_FORMAT),
}

response = requests.get(URL, params=params, timeout=30)
print(response.status_code)

data = response.json()
print(data["totalResults"])

for item in data["vulnerabilities"]:
    cve_id = item["cve"]["id"]
    published = item["cve"]["published"][:10]
    description = item["cve"]["descriptions"][0]["value"][:60]
    print(f"{cve_id}  {published}  {description}")
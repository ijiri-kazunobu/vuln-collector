import csv
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

rows = []
for item in data["vulnerabilities"]:
    cve_id = item["cve"]["id"]
    published = item["cve"]["published"][:10]
    description = item["cve"]["descriptions"][0]["value"].replace("\n", " ")
    url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
    print(f"{cve_id}  {published}  {description[:60]}")
    rows.append([cve_id, published, description, url])

with open("result.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["CVE番号", "公開日", "説明", "URL"])
    writer.writerows(rows)

print(f"{len(rows)} 件を result.csv に保存しました")
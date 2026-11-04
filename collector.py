import requests

URL = "https://jvndb.jvn.jp/myjvn"

params = {
    "method": "getVulnOverviewList",
    "feed": "hnd",
    "keyword": "Apache",
}

response = requests.get(URL, params=params, timeout=10)
response.encoding = "utf-8"

print(response.status_code)
print(response.text[:1500])
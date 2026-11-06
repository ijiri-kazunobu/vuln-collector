import argparse
import csv
from datetime import datetime, timedelta

import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000"
MAX_DAYS = 120

def fetch_vulnerabilities(keyword, days, limit):
    now = datetime.now()
    start = now - timedelta(days=days)
    params = {
        "keywordSearch": keyword,
        "resultsPerPage": limit,
        "pubStartDate": start.strftime(DATE_FORMAT),
        "pubEndDate": now.strftime(DATE_FORMAT),
    }

    try:
        response = requests.get(URL, params=params, timeout=30)
    except requests.exceptions.RequestException:
        print("[エラー] NVDに接続できませんでした。インターネット接続を確認してください")
        return None

    if response.status_code != 200:
        print(f"[エラー] NVDからエラーが返されました (ステータスコード: {response.status_code}) ")
        return None

    data = response.json()
    print(f"「{keyword}」に関する脆弱性: 全 {data['totalResults']} 件 (直近 {days} 日) ")
    return data["vulnerabilities"]

def save_csv(vulnerabilities, output):
    rows = []
    for item in vulnerabilities:
        cve_id = item["cve"]["id"]
        published = item["cve"]["published"][:10]
        description = item["cve"]["descriptions"][0]["value"].replace("\n", " ")
        url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"

        metrics = item["cve"]["metrics"].get("cvssMetricV31")
        if metrics:
            score = metrics[0]["cvssData"]["baseScore"]
            severity = metrics[0]["cvssData"]["baseSeverity"]
        else:
            score = ""
            severity = "未評価"
        print(f"{cve_id}  {published} {severity}  {description[:50]}")
        rows.append([cve_id, published, severity, score, description, url])

    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["CVE番号", "公開日", "深刻度", "スコア", "説明", "URL"])
        writer.writerows(rows)

    print(f"{len(rows)} 件を {output} に保存しました")


parser = argparse.ArgumentParser(description="NVDから最新の脆弱性情報を収集してCSVに保存するツール")
parser.add_argument("--keyword", default="Apache", help="検索するキーワード（省略時: Apache）")
parser.add_argument("--days", type=int, default=30, help=f"何日前までさかのぼるか（1〜{MAX_DAYS}、省略時: 30）")
parser.add_argument("--limit", type=int, default=20, help="取得する最大件数 (省略時: 20)")
parser.add_argument("--output", default="result.csv", help="保存するCSVファイル名（省略時: result.csv）")
args = parser.parse_args()

if args.days < 1 or args.days > MAX_DAYS:
    print(f"[エラー] --days は 1～{MAX_DAYS} の範囲で指定してください")
else:
    vulnerabilities = fetch_vulnerabilities(args.keyword, args.days, args.limit)
    if vulnerabilities is not None:
        save_csv(vulnerabilities, args.output)
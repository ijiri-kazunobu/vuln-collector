# Vuln Collector

NVD（National Vulnerability Database）のAPIから、指定したキーワードに関する最新の脆弱性情報を自動で収集し、CSVファイルに保存するPythonツールです。

## 背景

セキュリティの現場では、自分たちが利用しているソフトウェアに新しい脆弱性が公開されていないかを日々確認する必要があります。この情報収集を自動化し、結果をExcelで扱える形にまとめるために作成しました。

当初は日本の脆弱性データベースであるMyJVN APIの利用を予定していましたが、開発時にサービスが一時停止していたため（ステータスコード503）、米国NISTが運営するNVDのAPIを利用する形に切り替えました。

## セットアップ

```
$ pip install -r requirements.txt
```

## 使い方

```
$ python collector.py
$ python collector.py --keyword WordPress --days 7 --output wordpress.csv
```

| 引数 | 説明 |
|---|---|
| `--keyword` | 検索するキーワード（省略時：Apache） |
| `--days` | 何日前までさかのぼるか。1〜120の範囲で指定（省略時：30） |
| `--output` | 保存するCSVファイル名（省略時：result.csv） |

## 実行例

```
$ python collector.py --keyword WordPress --days 7 --output wordpress.csv
「WordPress」に関する脆弱性: 全 248 件（直近 7 日）
CVE-2026-104368  2026-10-30  The Export and Import Users and Customers plugin for WordPre
CVE-2026-5461  2026-10-30  The Forminator Forms plugin for WordPress is vulnerable to L
CVE-2026-114422  2026-10-30  The Enable Media Replace WordPress plugin before 4.2.3 does
...
20 件を wordpress.csv に保存しました
```

範囲外の日数を指定した場合

```
$ python collector.py --days 200
[エラー] --days は 1〜120 の範囲で指定してください
```

インターネットに接続できない場合

```
$ python collector.py
[エラー] NVDに接続できませんでした。インターネット接続を確認してください
```

## 出力されるCSV

| 列 | 内容 |
|---|---|
| CVE番号 | 脆弱性の識別番号（例：CVE-2026-104368） |
| 公開日 | 脆弱性情報の公開日 |
| 説明 | 脆弱性の説明（全文） |
| URL | NVDの詳細ページへのリンク |

ExcelでそのままCSVを開いても日本語が文字化けしないよう、BOM付きUTF-8（`utf-8-sig`）で保存しています。

## 工夫した点

- **エラー処理**：外部APIを利用するツールは、相手のサービスの停止や通信障害の影響を受けます。開発中に実際にMyJVNの停止に遭遇した経験から、通信エラーは `try` / `except` で、APIからのエラー応答はステータスコードで判定し、異常終了せずに分かりやすいメッセージを表示するようにしました。
- **入力値の検証**：NVD APIの日付範囲の上限（120日）に合わせ、範囲外の日数が指定された場合は通信を行う前にエラーを表示します。
- **データの整形**：説明文に含まれる改行を取り除き、CSVの1行に収まるようにしました。画面には説明の冒頭のみ、CSVには全文を出力しています。
- **詳細ページへのリンク**：各脆弱性のNVD詳細ページのURLをCSVに含め、気になる脆弱性をすぐに確認できるようにしました。
- **処理の分割**：「データの取得」と「CSVへの保存」を別の関数に分けました。取得元を追加する場合も、保存の処理はそのまま使えます。

## 利用上の注意

- NVD APIはAPIキーなしで利用できますが、30秒あたり5リクエストまでという制限があります。本ツールは1回の実行につき1回のみアクセスします。
- 現在は1回の実行で最大20件を取得します。
- This product uses the NVD API but is not endorsed or certified by the NVD.

## 今後の改善

- **JVN（MyJVN API）への対応**：サービス再開後、日本語の脆弱性情報も取得できるようにし、片方のサービスが停止していても、もう片方から取得を続けられるようにしたいと考えています。
- **危険度（CVSS）の出力**：CVSSのスコアと深刻度をCSVに追加し、危険度の高いものから確認できるようにしたいと考えています。
- **全件取得**：ページ分けされた結果を、APIの利用制限を守りながらすべて取得できるようにしたいと考えています。
- **定期実行と通知**：タスクスケジューラや cron で毎日自動実行し、新しい脆弱性を通知できるようにしたいと考えています。

## 使用技術

- Python 3.12
- requests
- 標準ライブラリ（argparse、csv、datetime）
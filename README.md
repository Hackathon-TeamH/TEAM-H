# TEAM-H

### TEST WRITE

mal
you
mayuu
koudai
taga
yuki


# ディレクトリ構成
```
.
├── ChatApp              # アプリ用ディレクトリ
│   ├── __init__.py         #
│   ├── app.py              # ルーティング
│   ├── models.py           # DB操作
|   |── channnels.py        # マッチングHTML作成関数
|   |── relods.py           # メッセージ一覧HTML作成関数
|   |── renderProfile.py    # プロフィールHTML作成関数
|   |── translation.py      # 翻訳機能
│   ├── static              # 静的ファイル用ディレクトリ
│   ├── templates           # Template(HTML)用ディレクトリ
│   |── util                # DBコネクション
│   └── config              # Flaskのconfig
│
├── Docker
│   ├── Flask
│   │   └── Dockerfile      # Flask(Python)用Dockerファイル
│   └── MySQL
│       ├── Dockerfile      # MySQL用Dockerファイル
│       ├── init.sql        # MySQL初期設定ファイル
│       └── my.cnf
│
├── docker-compose.yml      # Docker-composeファイル
└── requirements.txt        # 使用モジュール記述ファイル

```

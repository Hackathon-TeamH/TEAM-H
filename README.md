# TEAM-H

### TEST WRITE

mal
you
mayuu
koudai
taga
yuki


## チェックリスト
https://sunrise-brownie-db8.notion.site/e00deb25fc73461c8da71faf855d9f04?pvs=4


## ディレクトリ構成
```
.
│── ChatApp              # アプリ用ディレクトリ
│   ├── config              # Flaskのconfi
│   ├── static              # 静的ファイル用ディレクトリ
│   ├── templates           # Template(HTML)用ディレクトリ
|   |── util                # DBコネクション
|   |── __init__.py         #
|   |── app.py              # ルーティング
│   ├── channels.py         # マッチングHTML作成関数
|   ├── Dockerfile          # Flask用Dockerファイル
│   ├── models.py           # DB操作
│   |── renderProfile.py    # プロフィールHTML作成関数
│   |── translation.py      # 翻訳機能
│   └── uwsgi.ini
│
│── MySQL
│   ├── Dockerfile          # MySQL用Dockerファイル
│   ├── init.sql            # DB作成
│   └── my.cnf              # MySQL初期設定ファイル
|
├── Nginx
│   ├── static              # Nginx用静的ファイル
|   ├── Dockerfile          # Nginx用Dockerファイル
|   └── nginx.conf          # Nginx用初期設定ファイル
│
├── docker-compose.yml      # Docker-composeファイル
├── .gitignore              # 使用モジュール記述ファイル
└── README.md

```

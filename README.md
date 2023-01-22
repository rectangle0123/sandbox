# Sandboxアプリケーション

## スタートアップ
ビルド時のGitキャッシュ対策を施していないので```--no-cache```オプションを付加する。
```sh
# イメージビルド
$ docker build ./ -t sandbox --no-cache

# コンテナ起動＆ログイン（初回）
$ docker run --name sandbox -it sandbox /bin/bash
```

## アプリケーション起動
```sh
$ python3 app/main.py
```

## ミドルウェア・言語・フレームワーク
ミドルウェア
- SQLite
- memcached

言語
- Python

フレームワーク
- SQLAlchemy: PythonのORマッピングフレームワーク

## ソースコード
|ファイル名|説明|
|--|--|
|database.py|データベース定義|
|main.py|メインプログラム|
|models.py|Model定義|
|setup.py|初期データ投入プログラム、Dockerコンテナ起動時に実行|
|utils.py|memcached共通部品|

## Model

# Appendix
## Dockerコマンド集
```sh
# イメージビルド
$ docker build ./ -t sandbox --no-cache

# コンテナ起動＆ログイン（初回）
$ docker run --name sandbox -it sandbox /bin/bash

# コンテナ停止
$ docker stop sandbox

# コンテナ起動＆ログイン
$ docker start -ai sandbox

# コンテナ削除
$ docker container rm sandbox

# イメージ削除
$ docker image rm sandbox
```

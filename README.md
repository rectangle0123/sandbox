# Sandboxアプリケーション

## アプリケーションについて
### スタートアップ
ビルド時のGitキャッシュ対策を施していないので```--no-cache```オプションを付加する。
```sh
# イメージビルド
$ docker build ./ -t sandbox --no-cache

# コンテナ起動＆ログイン（初回）
$ docker run --name sandbox -it sandbox /bin/bash
```

### アプリケーション起動
```sh
$ python3 app/main.py
```

### 初期データ
Dockerコンテナ起動時に下記のデータが投入される。

役職
|ID|名前|
|--|--|
|1|PM|
|2|PG|
|3|Tester|

従業員
|ID|名前|入社年月日|役職|
|--|--|--|--|
|1|Lorand|1990-12-31|PM|
|2|Andy|2000-1-1|PG, Tester|
|3|Andy%|2020-4-1|Tester|

### ミドルウェア・言語・フレームワーク
ミドルウェア
- SQLite
- memcached: Dockerコンテナ起動時にサービスとして起動

言語
- Python

フレームワーク
- SQLAlchemy: PythonのORマッピングフレームワーク

---

## ソースコードについて
### ファイル
|ファイル名|説明|
|--|--|
|database.py|データベース定義|
|main.py|メインプログラム|
|models.py|Model定義|
|setup.py|初期データ投入プログラム、Dockerコンテナ起動時に実行|
|utils.py|memcached共通部品|

### Model（テーブル定義）
![models](https://user-images.githubusercontent.com/77914234/213900662-e0526784-d771-454c-b2d7-890fb4a3d443.png)

多対多なので、ORマッピングを考えると少しやっかいだが、SQLAlchemyでは紐付けテーブルを作成してあげることで実現できそうだ。

SQLiteは日付型を持っていないようなので、入社年月日はUnixタイムスタンプで定義する。

### メインプログラム
#### CUIでの対話
Pythonの```input```で実現。入力値で処理を分岐する。

#### Ctrl+C対応
発生した例外をキャッチしてプログラムを終了させる。

#### 横断的処理の実装
検索処理で横断的に必要になる共通部分は、デコレータでラップしてコードをシンプル化している。

#### 検索処理
以下の手順で実装。

- バリデーション（未入力のみ）
- キャッシュからデータを取得
- データがあればデシリアライズしたオブジェクトを表示して終了
- DBからデータを取得
- データがあれば、結果をシリアライズしてキャッシュに登録（キーは「メソッド名-パラメータ」）
- 結果表示

動作確認をしやすいように、キャッシュの生存期間は3分としている。キャッシュからデータを取得できた場合「DEBUG: Found in memcached.」とメッセージを表示している。

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

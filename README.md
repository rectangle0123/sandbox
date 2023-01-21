# Dockerコマンド
```
# イメージビルド
$ docker build ./ -t sandbox
```

```
# コンテナ起動＆ログイン（初回）
$ docker run --name sandbox -it sandbox /bin/bash
```

```
# コンテナ停止
$ docker stop sandbox
```

```
# コンテナ起動
$ docker start -ai sandbox
```

```
# コンテナ削除
$ docker container rm sandbox
```

```
# イメージ削除
$ docker image rm sandbox
```

# 課題
- CASCADE削除がうまくいかない
- バリデーション
- 横断的処理の実装

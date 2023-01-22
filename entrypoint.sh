#!/bin/sh

# memcachedサービス起動
service memcached start

# 初期データ投入
python3 app/setup.py

exec "$@"

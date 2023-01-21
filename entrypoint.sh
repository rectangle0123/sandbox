#!/bin/sh

# memcachedサービス起動
service memcached start

exec "$@"

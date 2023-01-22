FROM python:3
USER root

# アプリケーションディレクトリ
ARG app_home="/opt/sandbox"

# デプロイ
WORKDIR ${app_home}
RUN git clone --depth 1 https://github.com/rectangle0123/sandbox.git .
# COPY app ${app_home}/app
# COPY entrypoint.sh ${app_home}/

# ロケールのインストールと設定
RUN apt update
RUN apt -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# Vimインストール
RUN apt install -y vim

# SQLiteインストール
RUN apt install -y sqlite3

# memcachedインストール
RUN apt install -y memcached libmemcached-tools

# Pythonパッケージインストール
RUN pip install --upgrade pip
RUN pip install python-dateutil
RUN pip install sqlalchemy
RUN pip install pymemcache

# memcached起動
RUN chmod 755 ${app_home}/entrypoint.sh
ENTRYPOINT ["/opt/sandbox/entrypoint.sh"]

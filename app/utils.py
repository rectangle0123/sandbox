import inspect
import pickle
from pymemcache.client.base import Client

class MemcachedUtils:
    """ Memcachedユーティリティ"""

    # memcachedクライアント
    client = Client('localhost')

    def get(self, key):
        """ 取得 """
        keystring = self.__gen_keystring(key)
        if keystring:
            result = self.client.get(keystring)
            return pickle.loads(result) if result else None
        else:
            return None

    def set(self, key, obj):
        """ 設定 """
        keystring = self.__gen_keystring(key)
        if keystring:
            self.client.set(keystring, pickle.dumps(obj), expire=180)

    def __gen_keystring(self, str):
        """ キー文字列を作成する """
        key = f'{inspect.stack()[2].function}-{str}'
        return key if len(key) <= 250 else None

# インスタンスを返す
memcached = MemcachedUtils()

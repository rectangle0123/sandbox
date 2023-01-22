import inspect
import pickle
from pymemcache.client.base import Client

class MemcachedUtils:
    """ Memcachedユーティリティ"""

    # memcachedクライアント
    client = Client('localhost')

    @staticmethod
    def get(key: str):
        """ 取得 """
        keystring = MemcachedUtils.__gen_keystring(key)
        if keystring:
            result = MemcachedUtils.client.get(keystring)
            return pickle.loads(result) if result else None
        else:
            return None

    @staticmethod
    def set(key: str, obj):
        """ 設定 """
        keystring = MemcachedUtils.__gen_keystring(key)
        if keystring:
            MemcachedUtils.client.set(keystring, pickle.dumps(obj), expire=180)

    @staticmethod
    def __gen_keystring(str: str):
        """ キー文字列を作成する """
        key = f'{inspect.stack()[2].function}-{str}'
        return key if len(key) <= 250 else None

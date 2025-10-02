import redis
import json
from tests import tests_config


class CacheManager:
    _redis_clients = {}

    for name, cfg in tests_config.items():
        _redis_clients[name] = redis.Redis(
            host=cfg["host"],
            port=cfg["port"],
            decode_responses=True
        )


    @classmethod
    def save_cache(cls, config: str, key: str, value):
        try:
            client = cls._redis_clients[config]
            
            client.set(key, json.dumps(value))
            
            print(f'[Status] Key "{key}" saved in cache with config "{config}"')
            
        except (redis.exceptions.RedisError, KeyError) as e:
            print(f'[Error] Failed to save key "{key}" in config "{config}"')
            print(e)


    @classmethod
    def check_cache(cls, config: str, key: str):
        try:
            client = cls._redis_clients[config]
            value = client.get(key)
            
            if value is None:
                return None
            
            return json.loads(value)
        
        except (redis.exceptions.RedisError, KeyError, json.JSONDecodeError) as e:
            print(f'[Error] Failed to get key "{key}" from config "{config}"')
            print(e)
            
            return None

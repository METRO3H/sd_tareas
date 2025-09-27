import redis
import json

redis_clients = {
  "gauss_lru_5mb_1min": redis.Redis(host="redis_1", port=6379, decode_responses=True)
}

def check_cache(config: str, key: str):
    try:
        redis_client = redis_clients[config]
        return redis_client.get(key)
    except redis.exceptions.RedisError as e:
        print("Error Redis GET:", e)
        return None

def save_cache(config: str, key: str, value, ttl: int = None):
    try:
        redis_client = redis_clients[config]
        
        value = json.dumps(value)
        
        redis_client.set(key, value, ex=ttl)
        print(f'[Status] Request with key "{key}" saved in cache')
        
    except redis.exceptions.RedisError as e:
        
        print(f'[Error] Request with key "{key}" not saved in cache')
        print("Error Redis SET:", e)

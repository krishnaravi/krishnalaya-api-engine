import redis
import json
from functools import wraps

r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

def set_cache(key: str, data: dict, expire: int = 300):
    r.setex(key, expire, json.dumps(data))

def get_cache(key: str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def delete_cache(key: str):
    r.delete(key)

def cache_response(expire: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached = get_cache(key)
            if cached:
                return {"success": True, "message": "cached", "data": cached}
            result = await func(*args, **kwargs)
            set_cache(key, result, expire)
            return result
        return wrapper
    return decorator

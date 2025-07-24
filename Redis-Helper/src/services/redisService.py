import redis # type: ignore

class RedisService:
    def __init__(self, redis_client):
        self.redis = redis_client

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)
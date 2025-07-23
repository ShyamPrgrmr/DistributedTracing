import sys
import os
import redis

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Virtual environment:", os.environ.get('VIRTUAL_ENV', 'None'))

redis_host = 'redis'
redis_port = 6379
redis_password = os.environ.get('REDIS_PASSWORD')

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

try:
    pong = r.ping()
    print("Connected to Redis:", pong)
except redis.exceptions.ConnectionError as e:
    print("Redis connection error:", e)
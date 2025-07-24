import sys
import os
import redis # type: ignore
import requests # type: ignore
import json
import mysql.connector  # type: ignore




mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
mysql_port = int(os.environ.get('MYSQL_PORT', 3306))
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_database = os.environ.get('MYSQL_DATABASE')

if not all([mysql_user, mysql_password, mysql_database]):
    print("Error: MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE environment variables must be set.")
    sys.exit(1)

try:
    mysql_conn = mysql.connector.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    print("Connected to MySQL:", mysql_conn.is_connected())
except mysql.connector.Error as err:
    print("MySQL connection error:", err)
    sys.exit(1)


redis_host = 'redis'
redis_port = 6379
redis_password = os.environ.get('REDIS_PASSWORD')

if not redis_password:
    print("Error: REDIS_PASSWORD environment variable is not set.")
    sys.exit(1)

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

try:
    pong = r.ping()
    print("Connected to Redis:", pong)
except redis.exceptions.ConnectionError as e:
    print("Redis connection error:", e)
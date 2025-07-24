
import os

mysql_config:dict = {
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE')
}

redis_config:dict = {
    'host': os.environ.get('REDIS_HOST'),
    'port': int(os.environ.get('REDIS_PORT', 6379)),
    'password': os.environ.get('REDIS_PASSWORD'),
    'decode_responses': True
}



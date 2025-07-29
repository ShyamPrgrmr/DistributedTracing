
import os

schedule_config: dict = {
    'intervalSecond': int(os.environ.get('SCHEDULE_INTERVAL', 10)),  # in seconds
}

table_name: str = os.environ.get('TABLE_NAME', 'application_partition_mapping')

postgresql_config: dict = {
    'port': int(os.environ.get('POSTGRES_PORT', 5432)),
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'user': os.environ.get('POSTGRES_USER', 'dt_user'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'password@123'),
    'dbname': os.environ.get('POSTGRES_DB', 'distributed_tracing')
}

redis_config:dict = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': int(os.environ.get('REDIS_PORT', 6379)),
    'password': os.environ.get('REDIS_PASSWORD', 'Redis@123'),
    'decode_responses': True
}



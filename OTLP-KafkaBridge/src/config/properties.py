import os

table_name: str = os.environ.get('TABLE_NAME', 'application_partition_mapping')
port: int = int(os.environ.get('PORT', '5000'))
host: str = os.environ.get('HOST', '0.0.0.0')

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
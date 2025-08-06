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


kafka_config: dict = {
    'bootstrap_servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'topic': os.environ.get('KAFKA_TOPIC', 'otlp-bridge-topic'),
    'group_id': os.environ.get('KAFKA_GROUP_ID', 'otlp-bridge-group'),
    'auto_offset_reset': os.environ.get('KAFKA_AUTO_OFFSET_RESET', 'earliest'),
    'enable_auto_commit': os.environ.get('KAFKA_ENABLE_AUTO_COMMIT', 'true').lower() == 'true',
    'value_deserializer': lambda x: x.decode('utf-8')
}

# Print the names of environment variables used in this file
env_vars = [
    'TABLE_NAME',
    'PORT',
    'HOST',
    'POSTGRES_PORT',
    'POSTGRES_HOST',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_DB',
    'REDIS_HOST',
    'REDIS_PORT',
    'REDIS_PASSWORD',
    'KAFKA_BOOTSTRAP_SERVERS',
    'KAFKA_TOPIC',
    'KAFKA_GROUP_ID',
    'KAFKA_AUTO_OFFSET_RESET',
    'KAFKA_ENABLE_AUTO_COMMIT'
]


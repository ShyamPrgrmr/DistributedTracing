import redis  # type: ignore
import psycopg2  # type: ignore
from config.properties import postgresql_config, redis_config, table_name
from config.logger import get_logger

logger = get_logger(__name__)


class DBService:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.redis_client = redis.Redis(**redis_config)
        self.postgres_conn = psycopg2.connect(
            **postgresql_config
        )

    def save_trace(self, trace_data: dict):
        pass
            
    def save_metric(self, metric_data: dict):
        pass

    def save_log(self, log_data: dict):
        pass

    def __check_redis_connectivity(self):
        try:
            return self.redis_client.ping()
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            return False
    
    def __check_postgres_connectivity(self):
        try:
            with self.postgres_conn.cursor() as cur:
                cur.execute("SELECT 1;")
                connection_status = cur.fetchone()
                return connection_status and connection_status[0] == 1
        except Exception as e:
            self.logger.error(f"Failed to connect to PostgreSQL: {e}")
            return False
    
    def check_connectivity(self):
        if self.__check_redis_connectivity():
            self.logger.info("Connected to Redis successfully.")
        else:
            self.logger.error("Failed to connect to Redis.")
            return False

        if self.__check_postgres_connectivity():
            self.logger.info("Connected to PostgreSQL successfully.")
            return True
        
    def close_connections(self):
        if self.redis_client:
            self.redis_client.close()
            self.logger.info("Redis connection closed.")
        if self.postgres_conn:
            self.postgres_conn.close()
            self.logger.info("PostgreSQL connection closed.")

    def get_from_redis(self, key: str):
        try:
            value = self.redis_client.get(key)
            
            if value is None:
                self.logger.warning(f"Key {key} not found in Redis.")
                return None

            # value = value.decode('utf-8')
            self.logger.info(f"Retrieved value for key {key} from Redis.")
            return value

        except Exception as e:
            self.logger.error(f"Failed to get data from Redis: {e}")
            return None

    def get_from_postgres(self, condition: str):
        try:
            query = f"SELECT * FROM {table_name} WHERE  {condition};"
            with self.postgres_conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
        except Exception as e:
            self.logger.error(f"Failed to execute query in PostgreSQL: {e}")
            return None
        
    def put_in_postgres(self, data: dict):
        try:
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            with self.postgres_conn.cursor() as cur:
                cur.execute(query, tuple(data.values()))
                self.postgres_conn.commit()
                self.logger.info("Data inserted into PostgreSQL successfully.")
        except Exception as e:
            self.logger.error(f"Failed to insert data into PostgreSQL: {e}")
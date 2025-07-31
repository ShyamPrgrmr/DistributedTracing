import redis # type: ignore
import psycopg2 # type: ignore

from config.properties import postgresql_config

from config.logger import get_logger
logger = get_logger(__name__)

class DBConnections:
    def __init__(self):
        self.postgres_client = psycopg2.connect(
            **postgresql_config
        )

    def check_redis_connectivity(self):
        try:
            return self.redis_client.ping()
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return False

    def check_postgres_connectivity(self):
        try:
            with self.postgres_client.cursor() as cur:
                cur.execute("SELECT 1;")
                connection_status = cur.fetchone()
                return connection_status and connection_status[0] == 1
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            return False
        
    def check_connectivity(self):

        if self.check_redis_connectivity():
            logger.info("Connected to Redis successfully.")
        else:
            logger.error("Failed to connect to Redis.")
            return False

        if self.check_postgres_connectivity():
            logger.info("Connected to PostgreSQL successfully.")
            return True  # Return the connection for later use
        else:
            logger.error("PostgreSQL connection test failed.")
            return False

    def close_connections(self):
        if self.redis_client:
            self.redis_client.close()
            logger.info("Redis connection closed.")
        if self.postgres_client:
            self.postgres_client.close()
            logger.info("PostgreSQL connection closed.")

    def putInRedis(self, key: str, value: str):
        try:
            self.redis_client.set(key, value)
            logger.info(f"Successfully put {key} in Redis.")
        except Exception as e:
            logger.error(f"Failed to put {key} in Redis: {e}")

    def getFromRedis(self, key: str):
        try:
            value = self.redis_client.get(key)
            if value is not None:
                logger.info(f"Successfully retrieved {key} from Redis.")
                return value
            else:
                logger.warning(f"{key} not found in Redis.")
                return None
        except Exception as e:
            logger.error(f"Failed to get {key} from Redis: {e}")
            return None
        
    def getFromPostgres(self, table: str, condition: str = None):
        try:
            with self.postgres_client.cursor() as cur:
                query = f"SELECT * FROM {table}"
                if condition:
                    query += f" WHERE {condition}"
                cur.execute(query)
                results = cur.fetchall()
                logger.info(f"Successfully retrieved data from {table} table in PostgreSQL.")
                return results
        except Exception as e:
            logger.error(f"Failed to get data from {table} table in PostgreSQL: {e}")
            return None
    
    def refreshRedisData(self, table: str):
        data = self.getFromPostgres(table)
        
        for item in data:
            key = item[1]
            value = item[2] 
            logger.info(f"Refreshing Redis with key: {key}, value: {value}")
            self.putInRedis(key, value)
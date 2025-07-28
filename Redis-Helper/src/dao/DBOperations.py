import redis # type: ignore
import psycopg2 # type: ignore

from config.properties import redis_config, postgresql_config


from config.logger import get_logger
logger = get_logger(__name__)

class DBConnections:
    def __init__(self):
        self.redis_client = redis.Redis(
            **redis_config,
            socket_connect_timeout=5,
            socket_timeout=5
        )
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


from dao.DBOperations import DBConnections
from config.logger import get_logger
from config.properties import table_name

logger = get_logger(__name__)

class DBService:
    def __init__(self, db_operations: DBConnections):
        self.db_operations = db_operations

    def check_connectivity(self):
        if self.db_operations.check_connectivity():
            logger.info("Database connections are healthy.")
            return True
        else:
            logger.error("Database connections are unhealthy.")
            return False

    #get
    def get_data(self, key: str):
        return self.db_operations.getFromPostgres(key)
    
    #Refresh Redis Cache
    def refresh_redis(self):
        try:
            self.db_operations.refreshRedisData(table_name)
            logger.info("Redis cache refreshed successfully.")
        except Exception as e:
            logger.error(f"Failed to refresh Redis cache: {e}")

    #Put new data in Redis
    def get_from_postgres_and_put_in_redis(self, key: str):
        try:
            value = self.db_operations.getFromPostgres(key)
            if value is not None:
                self.db_operations.putInRedis(key, value)
                logger.info(f"Key '{key}' fetched from Postgres and stored in Redis.")
            else:
                logger.warning(f"Key '{key}' not found in Postgres.")
        except Exception as e:
            logger.error(f"Error fetching from Postgres or putting in Redis: {e}")
    
    def close(self):
        self.db_operations.close_connections()

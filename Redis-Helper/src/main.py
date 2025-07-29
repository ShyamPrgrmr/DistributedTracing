import time
from services.dbService import DBService
from dao.DBOperations import DBConnections
from config.logger import get_logger
from config.properties import schedule_config

logger = get_logger(__name__)

import schedule # type: ignore

def main():
    db_service = DBService(DBConnections())
    if db_service.check_connectivity():
        logger.info("All database connections are healthy.")
    else:
        logger.info("One or more database connections are unhealthy.")

    db_service.refresh_redis()
    logger.info("Redis data has been refreshed.")
 
def schedule_refresh():
    schedule.every(schedule_config['intervalSecond']).seconds.do(main)
    logger.info(f"Scheduler has been started - {schedule_config['intervalSecond']} seconds.")
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting
    
if __name__ == "__main__":
    schedule_refresh()

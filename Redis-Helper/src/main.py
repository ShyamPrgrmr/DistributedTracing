import sys
import os
import requests # type: ignore
import json

from  dao.DBOperations import DBConnections

from config.logger import get_logger
logger = get_logger(__name__)

def main():
    db_connections = DBConnections()
    if db_connections.check_connectivity():
        logger.info("All database connections are healthy.")
    else:
        logger.info("One or more database connections are unhealthy.")

if __name__ == "__main__":
    main()

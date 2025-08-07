from service.OTLPService import OTLPService
from service.kafkaService import KafkaService
from service.DBService import DBService

import json

from config.logger import get_logger
import random
logger = get_logger(__name__)


class ExporterService:
    def __init__(self):
        self.kafka_service = KafkaService()
        self.db_service = DBService()
        self.otlp_service = OTLPService()

    def get_app_id(self, trace_request):
        attributes = trace_request.get("resource", {}).get("attributes", [])
        for attr in attributes:
            if attr.get("key") == "service.name":
                return attr.get("value", {}).get("string_value", "")
        return ""

    def export_traces(self, otlp_message):
        json_data = self.otlp_service.otlp_to_json(otlp_message)
        data = json.loads(json_data)["resource_spans"]
        for resource_span in data:
            app_id = self.get_app_id(resource_span)
            partition_id = self.db_service.get_from_redis(app_id)

            logger.info(f"app_id: {app_id}, partition_id: {partition_id} is found in Redis.")

            if partition_id != None:
                logger.info(f"Partition ID found for app_id: {app_id}, using Redis.")
                result = self.kafka_service.produce_message(resource_span, partition=int(partition_id))
                
                if result is None:
                    logger.error(f"Failed to produce message to Kafka for app_id: {app_id} with partition: {partition_id}")
                else:
                    logger.info(f"Produced message to Kafka for app_id: {app_id} with partition: {partition_id}")

            else:
                try:
                    logger.warning(f"Partition ID not found for app_id: {app_id}, generating a new partition ID.")
                    partition_id = self.kafka_service.add_next_partition()
                    logger.info(f"Generated new partition ID: {partition_id} for app_id: {app_id}.")
                    self.db_service.put_in_postgres({"application_id": app_id, "partition_id": str(partition_id)})
                    result = self.kafka_service.produce_message(resource_span, partition=partition_id)

                    if result is None:
                        logger.error(f"Failed to produce message to Kafka for app_id: {app_id} with partition: {partition_id}")
                    else:
                        logger.info(f"Produced message to Kafka for app_id: {app_id} with partition: {partition_id}")

                except Exception as e:
                    logger.error(f"Error while fetching partition ID for app_id: {app_id}, error: {e}")
                    continue
                
    def export_metrics(self, otlp_message):
        json_data = self.otlp_service.otlp_to_json(otlp_message)
        self.kafka_service.produce_message(json_data)

    def export_logs(self, otlp_message):
        json_data = self.otlp_service.otlp_to_json(otlp_message)
        self.kafka_service.produce_message(json_data)


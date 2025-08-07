from config.properties import kafka_config  # type: ignore
from config.logger import get_logger
from kafka import KafkaProducer, KafkaAdminClient # type: ignore
from kafka.admin import KafkaAdminClient, NewPartitions # type: ignore
from typing import Any, Dict
from kafka import KafkaProducer # type: ignore
import json

logger = get_logger(__name__)

class KafkaService:
    def __init__(self):
        self.bootstrap_servers = kafka_config.get('bootstrap_servers', 'localhost:9092')
        self.topic = kafka_config.get('topic', 'otlp-bridge-topic')
        self.group_id = kafka_config.get('group_id', 'otlp-bridge-group')
        self.auto_offset_reset = kafka_config.get('auto_offset_reset', 'earliest')
        self.enable_auto_commit = kafka_config.get('enable_auto_commit', True)
        self.value_serializer = lambda x: x.encode('utf-8') if isinstance(x, str) else x
        logger.info(f"KafkaService initialized with bootstrap servers: {self.bootstrap_servers}, topic: {self.topic}")

    def add_next_partition(self) -> int:

        logger.info("IN add_next_partition: Adding next partition to Kafka topic...")

        topic_name = self.topic
        bootstrap_servers = self.bootstrap_servers

        next_partition = None

        try:
            logger.info("Creating KafkaAdminClient...")
            admin = KafkaAdminClient(
                bootstrap_servers=bootstrap_servers,
                client_id="next-partition-increaser"
            )

            topic_metadata = admin.describe_topics([topic_name])
            current_partition_count = len(topic_metadata[0]["partitions"])
            next_partition = current_partition_count  # Next available partition ID

        except Exception as e:
            logger.error(f"❌ Failed to get current partition count: {e}")
            logger.info("OUT add_next_partition: Adding next partition to Kafka topic...")
            raise
        # Step 2: Increase partition count by 1
        try:
            admin.create_partitions({
                topic_name: NewPartitions(total_count=current_partition_count + 1)
            })
            logger.info(f"✅ Partition {next_partition} added to topic '{topic_name}'.")
            logger.info("OUT add_next_partition: Adding next partition to Kafka topic...")
            return next_partition
        except Exception as e:
            logger.error(f"❌ Failed to add partition: {e}")
            logger.info("OUT add_next_partition: Adding next partition to Kafka topic...")

            raise

    def produce_message(self, message, partition: int = None) -> Any:
        logger.info(f"Producing message to Kafka topic '{self.topic}' partition {partition}")
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Kafka will serialize
            )

            if partition is not None:
                future = producer.send(self.topic, value=message, partition=partition)
            else:
                future = producer.send(self.topic, value=message)

            result = future.get(timeout=10)
            return result
        except Exception as e:
            logger.error(f"Failed to produce message to Kafka: {e}")
            return None
        finally:
            producer.close()
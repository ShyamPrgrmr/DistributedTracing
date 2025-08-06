from config.properties import kafka_config  # type: ignore
from config.logger import get_logger
from kafka import KafkaProducer, KafkaConsumer # type: ignore
from typing import Any, Dict
from kafka import KafkaProducer # type: ignore

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


    def produce_message(self, message, partition: int = None) -> Any:
        
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=self.value_serializer
        )
        # Ensure the message is serialized to bytes
        serialized_message = self.value_serializer(message)
        future = producer.send(self.topic, value=serialized_message, partition=partition)
        result = future.get(timeout=10)  # Wait for the message to be sent
        producer.close()
        return result
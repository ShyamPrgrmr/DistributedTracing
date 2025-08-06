# List of Kafka topics (comma-separated, suitable for shell)
if [ -z "${KAFKA_TOPICS}" ]; then
  echo "Error: KAFKA_TOPICS environment variable is not set or empty."
  exit 1
fi

IFS=',' read -ra TOPICS <<< "${KAFKA_TOPICS}"

# Loop to create each topic
for topic in "${TOPICS[@]}"; do
  /opt/bitnami/kafka/bin/kafka-topics.sh \
    --create \
    --if-not-exists \
    --topic "$topic" \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1
done

FROM bitnami/kafka:latest

USER root

COPY topics.sh /opt/bitnami/kafka/bin/

RUN chmod +x /opt/bitnami/kafka/bin/topics.sh 

CMD ["bash", "-c", "/opt/bitnami/scripts/kafka/run.sh & sleep 10 && /opt/bitnami/kafka/bin/topics.sh && wait"]


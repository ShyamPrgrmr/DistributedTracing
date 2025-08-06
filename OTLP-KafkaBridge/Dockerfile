FROM bitnami/python:3.12

USER root

WORKDIR /app

# Copy all project files including src/ and requirements.txt
COPY . .

# Uninstall any conflicting kafka versions
RUN pip uninstall -y kafka kafka-python six || true

# Clean kafka-python from requirements.txt and install others
RUN grep -v "kafka-python" requirements.txt > clean-requirements.txt && \
    pip install --no-cache-dir -r clean-requirements.txt && \
    pip install git+https://github.com/dpkp/kafka-python.git@master

# Install system and Python tools for compiling protos
RUN apt-get update && apt-get install -y git protobuf-compiler && \
    pip install grpcio-tools

# Clone OpenTelemetry proto definitions
RUN git clone --depth 1 https://github.com/open-telemetry/opentelemetry-proto.git /app/opentelemetry-proto

# Create output directory and compile all required protos
RUN mkdir -p /app/generated && \
    python -m grpc_tools.protoc \
        -I/app/opentelemetry-proto \
        --python_out=/app/generated \
        /app/opentelemetry-proto/opentelemetry/proto/common/v1/common.proto \
        /app/opentelemetry-proto/opentelemetry/proto/resource/v1/resource.proto \
        /app/opentelemetry-proto/opentelemetry/proto/trace/v1/trace.proto \
        /app/opentelemetry-proto/opentelemetry/proto/collector/trace/v1/trace_service.proto

# Create __init__.py files so protobuf packages are importable
RUN touch /app/generated/opentelemetry/__init__.py && \
    touch /app/generated/opentelemetry/proto/__init__.py && \
    touch /app/generated/opentelemetry/proto/common/__init__.py && \
    touch /app/generated/opentelemetry/proto/common/v1/__init__.py && \
    touch /app/generated/opentelemetry/proto/resource/__init__.py && \
    touch /app/generated/opentelemetry/proto/resource/v1/__init__.py && \
    touch /app/generated/opentelemetry/proto/trace/__init__.py && \
    touch /app/generated/opentelemetry/proto/trace/v1/__init__.py && \
    touch /app/generated/opentelemetry/proto/collector/__init__.py && \
    touch /app/generated/opentelemetry/proto/collector/trace/__init__.py && \
    touch /app/generated/opentelemetry/proto/collector/trace/v1/__init__.py

# Verify that protobuf imports work
RUN python -c "import sys; sys.path.insert(0, '/app/generated'); \
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest; \
print('✅ Protobuf import works!')"

# Verify kafka-python works
RUN python -c "from kafka import KafkaProducer, KafkaConsumer; print('✅ Kafka works!')"

WORKDIR /app/src

CMD ["python", "main.py"]

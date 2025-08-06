import sys
sys.path.insert(0, '/app/generated')

from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest # type: ignore


from flask import Flask, request, jsonify # type: ignore
from config.logger import get_logger
from config.properties import port, host
import gzip
from service.exporterService import ExporterService  # type: ignore

logger = get_logger(__name__)

app = Flask(__name__)

exportService = ExporterService()

@app.before_request
def log_request_info():
    logger.info(f"Incoming request: {request.method} {request.path} from {request.remote_addr}")

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called.")
    return jsonify({"status": "healthy"}), 200


@app.route('/v1/traces', methods=['POST'])
def otlp_exporter():
    if request.content_type != 'application/x-protobuf':
        return jsonify({"error": "Unsupported Media Type"}), 415

    # Handle gzip if present
    if request.headers.get('Content-Encoding') == 'gzip':
        data = gzip.decompress(request.get_data())
    else:
        data = request.get_data()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        trace_request = ExportTraceServiceRequest()
        trace_request.ParseFromString(data)
        logger.info(f"Received {len(trace_request.resource_spans)} spans")
    except Exception as e:
        logger.error(f"Failed to parse protobuf: {e}")
        return jsonify({"error": "Invalid protobuf payload"}), 400

    # Send to export service (pass the parsed protobuf object)
    exportService.export_traces(trace_request)

    return jsonify({"status": "received"}), 202



@app.route('/v1/metrics', methods=['POST'])
def otlp_metrics_exporter():
    if request.content_type != 'application/x-protobuf':
        return jsonify({"error": "Unsupported Media Type"}), 415
    data = request.get_data()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    logger.info(f"Received protobuf metrics data of length: {len(data)}")
    return jsonify({"status": "received"}), 202

@app.route('/v1/logs', methods=['POST'])
def otlp_logs_exporter():
    if request.content_type != 'application/x-protobuf':
        return jsonify({"error": "Unsupported Media Type"}), 415
    data = request.get_data()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    logger.info(f"Received protobuf logs data of length: {len(data)}")
    return jsonify({"status": "received"}), 202



if __name__ == '__main__':
    app.run(host=host, port=port)
    logger.info(f"Server running on {host}:{port}")
    logger.info("OTLP Kafka Bridge is ready to receive requests.")

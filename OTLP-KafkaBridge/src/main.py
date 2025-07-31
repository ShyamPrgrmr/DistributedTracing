from flask import Flask, request, jsonify # type: ignore
from config.logger import get_logger
from config.properties import port, host

logger = get_logger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called.")
    return jsonify({"status": "healthy"}), 200


@app.route('/v1/traces', methods=['POST'])
def otlp_exporter():
    if request.content_type != 'application/x-protobuf':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_data()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print("Headers : ", dict(request.headers))
    print("data : ", data)

    logger.info(f"Received protobuf data of length: {len(data)}")
    return jsonify({"status": "received"}), 202


if __name__ == '__main__':
    app.run(host=host, port=port)
    logger.info(f"Server running on {host}:{port}")
    logger.info("OTLP Kafka Bridge is ready to receive requests.")

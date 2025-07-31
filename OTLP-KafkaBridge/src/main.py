from flask import Flask, request, jsonify # type: ignore
from config.logger import get_logger
from config.properties import port, host

logger = get_logger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called.")
    return jsonify({"status": "healthy"}), 200


@app.route('/exporter', methods=['POST'])
def otlp_exporter():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    logger.info(f"Received data: {data}")
    return jsonify({"status": "received", "data": data}), 202


if __name__ == '__main__':
    app.run(host=host, port=port)
    logger.info(f"Server running on {host}:{port}")
    logger.info("OTLP Kafka Bridge is ready to receive requests.")

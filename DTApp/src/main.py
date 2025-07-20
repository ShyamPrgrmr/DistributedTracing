from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.json
    return jsonify({"message": "Data processed successfully", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True)

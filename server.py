from http import HTTPStatus
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    
    # 필요한 처리 수행
    # 예: 데이터베이스에 저장, 추가 처리 수행 등

    return jsonify({"status": "success", "message": "Data received successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
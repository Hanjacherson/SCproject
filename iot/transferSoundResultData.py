from flask import Flask
import requests
import threading
import time

app = Flask(__name__)

def get_latest_url_data():
    # 실제 환경에서는 이 데이터를 데이터베이스, 파일, API 호출 등을 통해 가져올 수 있습니다.
    url = 'http://192.168.21.152:5021/data'
    data = {"key1": "value1", "key2": "value2"}
    return url, data

def send_json_to_spring():
    while True:
        try:
            url, data = get_latest_url_data()  # 최신 URL과 데이터 가져오기
            response = requests.post(url, json=data)
            print(f"JSON sent to {url}. Response status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(10)

@app.before_first_request
def activate_job():
    thread = threading.Thread(target=send_json_to_spring)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return "Flask is running!"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5051)

from flask import Flask
import requests
import threading
import time

app = Flask(__name__)

def send_file_to_spring():
    while True:
        try:
            response = requests.get('http://192.168.21.152:5050')
            print(f"File sent. Response status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(10)  # 10초 대기

@app.before_first_request
def activate_job():
    thread = threading.Thread(target=send_file_to_spring)
    thread.daemon = True  # 주 스레드가 종료될 때 백그라운드 스레드도 종료되도록 설정
    thread.start()

@app.route('/')
def index():
    return "Flask is running!"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5055)

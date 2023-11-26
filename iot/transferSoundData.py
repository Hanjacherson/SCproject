from flask import Flask
import requests
import threading
import time

app = Flask(__name__)

def send_file_to_spring(filename):
    while True:
        try:
            with open(filename, 'rb') as f:
                files = {'file': f}
                response = requests.post('http://192.168.21.152:5021/file', files=files)
                print(f"File sent. Response status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(10)  # 10초 대기

@app.before_first_request
def activate_job(filename):
    thread = threading.Thread(target=send_file_to_spring, args=(filename,))
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return "Flask is running!"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5051)

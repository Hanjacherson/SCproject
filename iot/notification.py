from http import HTTPStatus
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# IFTTT 웹훅 URL
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/dog_check_please/with/key/d4BLCPHNfnxfSnep3Vl4dw'

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/data', methods=['GET','POST'])
def receive_data():
    data = request.json
    # data = request.get_json() post
    print("Received data:", data)
    
    # 값이 2 이상인 경우에만 IFTTT로 알림 보내기
    if 'value' in data and data['value'] == 1:
        send_notification()
        return 'Notification sent'
    else:
        return 'Value is less than 2, no notification sent'

def send_notification():
    # IFTTT로 POST 요청 보내기
    data1 = {'값1': '노드조1'}
    try:
        response = requests.post(ifttt_webhook_url, json=data1)
        response.raise_for_status()  # 나쁜 응답에 대해 HTTPError 발생
        logger.info("알림이 성공적으로 전송되었습니다.")
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP 오류: {errh}")
    except requests.exceptions.RequestException as err:
        logger.error(f"요청 예외: {err}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
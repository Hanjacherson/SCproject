from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# IFTTT 웹훅 URL
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/dog_check_please/with/key/d4BLCPHNfnxfSnep3Vl4dw'

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 라우트 설정
@app.route('/send_value', methods=['POST'])
def send_value():
    # POST 요청으로 전송된 값 가져오기
    data = request.get_json()

    # 값이 2 이상인 경우에만 IFTTT로 알림 보내기
    if 'value' in data and data['value'] >= 2:
        send_notification()
        return 'Notification sent'
    else:
        return 'Value is less than 2, no notification sent'

def send_notification():
    # IFTTT로 POST 요청 보내기
    data1 = {'value1': '노드조'}
    try:
        response = requests.post(ifttt_webhook_url, json=data1)
        response.raise_for_status()  # 나쁜 응답에 대해 HTTPError 발생
        logger.info("알림이 성공적으로 전송되었습니다.")
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP 오류: {errh}")
    except requests.exceptions.RequestException as err:
        logger.error(f"요청 예외: {err}")

if __name__ == '__main__':
    # 서버 실행
    app.run(debug=False)
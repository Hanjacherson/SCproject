import os
import numpy as np
import soundfile as sf
import requests
import threading
import time
import spidev
import tflite_runtime.interpreter as tflite
import wave
import json
import pymysql as ps
import socket

def wait_for_network(host="8.8.8.8", port=53, timeout=10):
    for i in range(timeout):
        try:
            socket.create_connection((host, port), 2)
            return True
        except OSError:
            time.sleep(1)
    return False

# 네트워크 대기
if not wait_for_network():
    exit(1)

# 환경 변수 설정 
os.environ['DB_HOST'] = 'project-db-stu3.smhrd.com'
os.environ['DB_NAME'] = 'Insa4_IOTB_final_4'
os.environ['DB_USER'] = 'Insa4_IOTB_final_4'
os.environ['DB_PASSWORD'] = 'aischool4'
os.environ['DB_PORT'] = '3307'

# 이후 코드에서 환경 변수 사용
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_port = int(os.environ.get('DB_PORT'))

# 데이터베이스 연결
mysql = ps.connect(host=db_host, db=db_name, user=db_user, password=db_password, port=db_port)

# spidev 설정 및 아날로그 읽기 함수
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def DQL(sql, params=None):
    cursor = mysql.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    return result

def DML(sql, params=None):
    cursor = mysql.cursor()
    cursor.execute(sql, params)
    mysql.commit()
    cursor.close()
    return "success!!"

def analog_read(portChannel):
    adc = spi.xfer2([1, (8+portChannel)<<4, 0])
    data = ((adc[1]&3)<<8)+adc[2]
    return data

# 오디오 데이터 수집 및 .wav 파일 저장 함수
def collect_audio_data(duration, sample_rate, base_file_path, inf_idx):

    file_counter = 1
    num = DQL("select voice_idx from t_voice where pet_idx = %s order by voice_idx desc",(inf_idx))
    if num[0][0] > 1:
        file_counter = num[0][0] + 1
    output_file_path = f"{base_file_path}_{file_counter}.wav"

    num_samples = duration * sample_rate
    audio_data = []

    for _ in range(num_samples):
        readData = analog_read(0)
        scaled_data = int((readData / 1023.0) * 65535.0 - 32768)
        audio_data.append(scaled_data)
        time.sleep(1.0 / sample_rate)
    
    audio_array = np.array(audio_data, dtype=np.int16)

    with wave.open("/home/pi/Desktop/TEST/soundFile/"+output_file_path, 'w') as output_file:
        output_file.setnchannels(1)
        output_file.setsampwidth(2)
        output_file.setframerate(sample_rate)
        output_file.writeframes(audio_array.tobytes())
    
    DML("insert into t_voice(pet_idx, voice_data) values(%s, %s)",(inf_idx,output_file_path))
    return output_file_path

# .wav 파일에서 오디오 데이터 로드 함수
def load_audio_data(wav_file_path, sample_rate):
    if not os.path.exists("/home/pi/Desktop/TEST/soundFile/"+wav_file_path):
        print(f"File not found: {wav_file_path}")
        return None, None

    audio, sr = sf.read("/home/pi/Desktop/TEST/soundFile/"+wav_file_path)
    return audio, sr

def process_audio_data(audio_data, sample_rate):
    # TensorFlow Lite 모델 로드 및 텐서 할당
    interpreter = tflite.Interpreter(model_path="/home/pi/Desktop/TEST/model.tflite")
    interpreter.allocate_tensors()

    # 입력 텐서 설정 및 모델 실행
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]['shape']
    
    # 오디오 데이터 타입을 float32로 변환
    audio_data = audio_data.astype(np.float32)

    # 오디오 데이터 형태 변환
    test = np.expand_dims(audio_data, axis=0)
    test = np.expand_dims(test, axis=-1)
    test = np.reshape(test, input_shape)

    interpreter.set_tensor(input_details[0]['index'], test)
    interpreter.invoke()

    # 결과 얻기
    model_result = interpreter.get_tensor(output_details[0]['index'])
    
    return model_result.tolist()[0][0]

def send_json_to_server(url, data, wav_file, inf_idx):
    try:
        voice_idx = DQL("select voice_idx from t_voice where pet_idx = %s and voice_data = %s",(inf_idx, wav_file))
        jdata = json.dumps({"voice_idx":voice_idx,"value":data})
        response = requests.post(url, data=jdata, headers={'Content-Type' : 'application/json'})
        print(f"JSON sent to {url}. Response status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def periodic_task(duration, wav_file_path, sample_rate, server_url):
    file_path = '/home/pi/Desktop/TEST/data.txt'
    while True:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(str(DQL("select count(*) from t_pet")[0][0]))
        with open(file_path, 'r') as file:
            inf_idx = file.read()
        
        # 파일 생성
        wav_file = collect_audio_data(duration, sample_rate, wav_file_path, inf_idx)
        # 파일 로드
        audio_data, sr = load_audio_data(wav_file, sample_rate)
        # 오디오 데이터가 유효한 경우에만 처리
        if audio_data is not None:
            result = process_audio_data(audio_data, sr)
            send_json_to_server(server_url, result, wav_file, inf_idx)

        time.sleep(60)  # 60초 간격으로 반복
def server_location():
    try:
        return 'http://'+str(DQL("select ip_val from t_ip where ad_idx=%s",1)[0][0])+':5000/data'
    except e:
        print(e)
    return 'http://192.168.20.99:5000/data'
    
def main():
    wav_file_path = 'Sound.wav'  # .wav 파일 경로
    sample_rate = 22050  # 샘플링 레이트
    duration = 4 # 재생 시간
    server_url = server_location()
    thread = threading.Thread(target=periodic_task, args=(duration, wav_file_path, sample_rate, server_url))
    thread.daemon = True
    thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

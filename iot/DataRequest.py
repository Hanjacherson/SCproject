import numpy as np
import librosa
import requests
import threading
import time
import spidev
import tflite_runtime.interpreter as tflite
import wave

# spidev 설정 및 아날로그 읽기 함수
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def analog_read(portChannel):
    adc = spi.xfer2([1, (8+portChannel)<<4, 0])
    data = ((adc[1]&3)<<8)+adc[2]
    return data

# 오디오 데이터 수집 및 변환 함수
def collect_audio_data(duration, sample_rate, output_file_path='output.wav'):
    num_samples = duration * sample_rate
    audio_data = []

    for _ in range(num_samples):
        readData = analog_read(0)  # spidev를 통해 데이터를 읽음
        scaled_data = int((readData / 1023.0) * 65535.0 - 32768)  # 16비트 오디오로 변환
        audio_data.append(scaled_data)
        time.sleep(1.0 / sample_rate)
    
    audio_array = np.array(audio_data, dtype=np.int16)

    # wave 파일 저장 설정
    output_file = wave.open(output_file_path, 'w')
    output_file.setnchannels(1)  # 모노
    output_file.setsampwidth(2)  # 샘플당 2바이트 (16비트)
    output_file.setframerate(sample_rate)
    output_file.writeframes(audio_array.tobytes())
    output_file.close()

    return audio_array

def process_audio_data(audio_data, sample_rate):
    # TensorFlow Lite 모델 로드 및 텐서 할당
    interpreter = tflite.Interpreter(model_path="/home/pi/Desktop/TEST/model.tflite")
    interpreter.allocate_tensors()
    
    # 오디오 데이터를 부동소수점 형태로 변환 및 전처리
    audio = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
    sr=sample_rate

    # 2차원 배열로 변환
    test = np.expand_dims(audio, axis=0)
    test = np.expand_dims(test, axis=-1)

    # 입력 텐서 설정 및 모델 실행
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], test)
    interpreter.invoke()

    # 결과 얻기
    output_details = interpreter.get_output_details()
    model_result = interpreter.get_tensor(output_details[0]['index'])

    return model_result

# 결과를 JSON 형식으로 전송하는 함수
def send_json_to_server(url, data):
    try:
        response = requests.post(url, json=data)
        print(f"JSON sent to {url}. Response status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 주기적으로 오디오 데이터 처리 및 전송을 수행하는 함수
def periodic_task(sample_rate, duration, server_url):
    while True:
        audio_data = collect_audio_data(duration, sample_rate)
        result = process_audio_data(audio_data, sample_rate)
        send_json_to_server(server_url, result)
        time.sleep(60) 

# 멀티스레딩을 이용한 주기적 작업 실행
def main():
    sample_rate = 22050  # 샘플링 레이트
    duration = 4         # 녹음 시간
    server_url = 'http://192.168.20.99:5000/data'  # 업로드 할 서버

    thread = threading.Thread(target=periodic_task, args=(sample_rate, duration, server_url))
    thread.daemon = True
    thread.start()

    # 메인 스레드는 다른 작업을 계속 수행할 수 있음
    while True:
        time.sleep(1)

# 스크립트가 직접 실행될 때만 main 함수 호출
if __name__ == "__main__":
    main()

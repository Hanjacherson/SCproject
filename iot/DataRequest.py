import numpy as np
import librosa
import requests
import threading
import time
import spidev

# spidev 설정 및 아날로그 읽기 함수
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def analog_read(portChannel):
    adc = spi.xfer2([1, (8+portChannel)<<4, 0])
    data = ((adc[1]&3)<<8)+adc[2]
    return data

# 오디오 데이터 수집 및 변환 함수
def collect_audio_data(duration, sample_rate):
    num_samples = duration * sample_rate
    audio_data = []

    for _ in range(num_samples):
        readData = analog_read(0)  # spidev를 통해 데이터를 읽음
        scaled_data = int((readData / 1023.0) * 65535.0 - 32768)  # 16비트 오디오로 변환
        audio_data.append(scaled_data)
        time.sleep(1.0 / sample_rate)
    
    return np.array(audio_data, dtype=np.int16)

# 오디오 데이터 전처리 및 모델 처리 함수
def process_audio_data(audio_data, sample_rate):
    S = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    tempo, _ = librosa.beat.beat_track(audio_data, sr=sample_rate)

    # 모델 처리 (가정)
    model_result = process_with_model(log_S, tempo)

    return model_result

# 모델 처리 함수 (가정)
def process_with_model(spectrogram, tempo):
    # 이 부분은 실제 모델에 따라 다르게 구현되어야 함
    return {"processed_data": spectrogram, "tempo": tempo}

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
        time.sleep(10)

# 멀티스레딩을 이용한 주기적 작업 실행
def main():
    sample_rate = 44100  # 샘플링 레이트
    duration = 5         # 녹음 시간 (초)
    server_url = '데이터를 받을 서버'  # 서버 URL (가정)

    thread = threading.Thread(target=periodic_task, args=(sample_rate, duration, server_url))
    thread.daemon = True
    thread.start()

    # 메인 스레드는 다른 작업을 계속 수행할 수 있음
    while True:
        time.sleep(1)

# 스크립트가 직접 실행될 때만 main 함수 호출
if __name__ == "__main__":
    main()


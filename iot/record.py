import wave
import struct
import spidevRead as sr
import time

# 설정
sample_rate = 44100  # 샘플링 레이트
duration = 5         # 녹음할 시간 (초)
num_samples = duration * sample_rate

# 데이터 수집
audio_data = []
start_time = time.time()
while len(audio_data) < num_samples:
    # spidevRead를 통해 데이터를 읽는다고 가정합니다.
    readData = sr.analog_read(0)
    # 0-1023 범위의 데이터를 16비트 오디오(-32768 to 32767)로 변환
    scaled_data = int((readData / 1023.0) * 65535.0 - 32768)
    audio_data.append(scaled_data)
    time.sleep(1.0 / sample_rate)

# wave 파일 저장 설정
output_file = wave.open('output.wav', 'w')
output_file.setnchannels(1)  # 모노
output_file.setsampwidth(2)  # 샘플당 2바이트 (16비트)
output_file.setframerate(sample_rate)

# 오디오 데이터를 wave 파일에 쓴다
for value in audio_data:
    data = struct.pack('<h', value)
    output_file.writeframesraw(data)

output_file.close()
print("Recording is finished and saved to 'output.wav'")

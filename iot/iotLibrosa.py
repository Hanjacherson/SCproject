import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# 오디오 파일 로드
file_path = 'output.wav'
# 오디오 파일의 일부만 로드
y, sr = librosa.load(file_path, sr=22050, offset=0.0, duration=30.0)  # 처음 30초만 로드

# 멜 스펙트로그램 생성
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
log_S = librosa.power_to_db(S, ref=np.max)

plt.figure()
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
plt.title('Mel Spectrogram')
plt.colorbar(format='%+02.0f dB')
plt.tight_layout()
plt.show()

# 템포 추정
tempo, _ = librosa.beat.beat_track(y, sr=sr)
print(f"Estimated Tempo: {tempo} BPM")

import librosa
import librossa.display
import matplotlib.pyplot as plt

f = 'output.wav'
y, sh = librosa.load(f)

plt.figure(figsize(12,4))
librosa.display.waveshow(y, sr=sr)
plt.show()
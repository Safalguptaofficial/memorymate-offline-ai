# record.py
import sounddevice as sd
from scipy.io.wavfile import write


def record_voice(filename="my_voice.wav", duration=5):
    fs = 16000  # Sample rate

    print(f"🎤 Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    write(filename, fs, recording)
    print(f"✅ Recording saved as '{filename}'")

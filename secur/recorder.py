import pyaudio
import wave
from datetime import datetime

FORMAT = pyaudio.paInt16  # Format of audio samples (16-bit signed integers)
CHANNELS = 2              # Number of audio channels (2 for stereo)
RATE = 44100              # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 5        # Duration of recording in seconds

# Get the current timestamp to save wav file 
current_time = datetime.now().strftime("%Y-%m-%d at %H.%M.%S")
output_wav_file = f"Evidence {current_time}.wav"

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_wav_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Evidence has been captured")
import pyaudio
import wave

chunk = 4096
sample_format = pyaudio.paInt16
channels = 1
rate = 44100
seconds = 4
soundname = "uploads/output_sound.wav"
p = pyaudio.PyAudio()


def voice():
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input_device_index=1,
                    input=True)

    frames = []
    for i in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(soundname, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    return 0

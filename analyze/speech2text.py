import json

from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from io import BytesIO


class Recognizer:
    def __init__(
        self,
        model_path: str,
        frame_rate: int = 16_000,
        channels: int = 1
    ):
        self.frame_rate = frame_rate
        self.channels = channels

        model = Model(model_path)
        self.recognizer = KaldiRecognizer(model, self.frame_rate)
        self.recognizer.SetWords(True)

    def recognize(self, raw_bytes: bytes):
        mp3 = AudioSegment.from_file(BytesIO(raw_bytes))
        mp3 = mp3.set_channels(self.channels)
        mp3 = mp3.set_frame_rate(self.frame_rate)

        self.recognizer.AcceptWaveform(mp3.raw_data)
        return json.loads(self.recognizer.Result())["text"]

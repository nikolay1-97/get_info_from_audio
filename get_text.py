"""Модуль переводит речь из аудиофайла в текстовый формат"""
import json

from pydub import AudioSegment
from vosk import Model, KaldiRecognizer


def get_text(path_to_audio_file: str, model: str = 'ru') -> str:
    CHANNELS=1
    FRAME_RATE = 16000

    model = Model(lang=model)

    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    mp3 = AudioSegment.from_mp3(path_to_audio_file)
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)

    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    result = json.loads(result)["text"]

    return result

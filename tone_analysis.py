"""Модуль определяет тон голоса спикера"""
from parselmouth import Sound

def get_tone(path_to_audio_file: str, gender: str) -> bool:
    sound = Sound(path_to_audio_file)
    pitch = sound.to_pitch()
    result = pitch.get_mean_absolute_slope()

    if gender == 'male':
        if result >= 200:
            return True
        return False
    elif gender == 'female':
        if result >= 380:
            return True
        return False
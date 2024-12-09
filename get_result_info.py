"""Модуль собирает результирующую информацию об аудиофайле"""
from os import getcwd, remove
from time import time
from json import dumps

from pyannote.audio import Pipeline
from pydub import AudioSegment

from get_gender import get_gender
from get_text import get_text
from tone_analysis import get_tone


# функция извлекает результирующую информаци об аудио
def get_info_from_audio(path_to_audio_file: str) -> str:
    rec = AudioSegment.from_mp3(path_to_audio_file)
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization-3.1', use_auth_token='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')
    DEMO_FILE = {'uri': 'blabal', 'audio': path_to_audio_file}
    dz = pipeline(DEMO_FILE)
    
    # словарь для сбора информации об аудио
    data = {}

    # собираем текст диалога и продолжительность разговора каждого спикера
    for turn, _, speaker in dz.itertracks(yield_label=True):
        if speaker not in data:
            data[speaker] = {'segments':[{
                'start': turn.start,
                'end': turn.end,
                'duration': round(turn.end - turn.start, 2),
                'speaker': speaker,
                'text': get_text(rec[turn.start * 1000: turn.end * 1000].export(format='mp3')),
            }]}
        else:
            data[speaker]['segments'].append({
                'start': turn.start,
                'end': turn.end,
                'duration': round(turn.end - turn.start, 2),
                'speaker': speaker,
                'text': get_text(rec[turn.start * 1000: turn.end * 1000].export(format='mp3')),
            })

    # определяем гендер спикера и тон
    for speaker in data.keys():
        start = data[speaker]['segments'][0]['start'] * 1000
        end = data[speaker]['segments'][0]['end'] * 1000
        audio_of_speaker = rec[start:end]

        if len(data[speaker]['segments']) > 1:
            for number_segments in range(1, len(data[speaker]['segments'])):
                start = data[speaker]['segments'][number_segments]['start'] * 1000
                end = data[speaker]['segments'][number_segments]['end'] * 1000
                audio_of_speaker += rec[start:end] 
        data[speaker]['gender'] = get_gender(audio_of_speaker.export(format='wav'))
        path = getcwd() + '\\temp_audio\\' + str(time()) + '.wav'
        audio_of_speaker.export(path, format='wav')
        gender = data[speaker]['gender']
        data[speaker]['raised_voice'] = get_tone(path, gender)
        remove(path)
    
    # список для сбора информации об аудио
    pre_data = []

    # собираем информацию о каждом отрзке речи для каждого спикера
    for speaker in data.keys():
        for segment in data[speaker]['segments']:
            segment['gender'] = data[speaker]['gender']
            segment['raised_voice'] = data[speaker]['raised_voice']
            pre_data.append(segment)
    
    # сортируем список с данными по времени
    pre_data.sort(key=lambda row: row['start'])
    result_dict = {}

    # словарь для сбора информации об общей длительности речи для каждого спикера
    total_duration = {}

    # определяем общую длительность речи для каждого сикера
    for row in pre_data:
        if row["speaker"] not in total_duration:
            total_duration[row["speaker"]] = row["duration"]
        else:
            total_duration[row["speaker"]] += row["duration"]

    result_dict["dialog"] = []
    result_dict["result_duration"] = total_duration

    # собираем результирующую информацию
    for row in pre_data:
        result_dict["dialog"].append(
            {
                "sourse": row["speaker"],
                "text": row["text"],
                "duration": row["duration"],
                "raised_voice": row["raised_voice"],
                "gender": row["gender"],
            }
        )
    return dumps(result_dict, ensure_ascii=False)

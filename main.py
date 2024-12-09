"""Файл запуска приложения."""
from fastapi import FastAPI
import uvicorn

from pydantic_model import RequestModel
from get_result_info import get_info_from_audio

def get_application() -> FastAPI:
    """Возвращает экземпляр приложения.

    Returns:
        FastAPI: _description_
    """
    application = FastAPI()
    return application


application = get_application()

@application.post('/')
def get_info_about_audio(request: RequestModel) -> str:
    try:
        return get_info_from_audio(request.path_to_audio_file)
    except:
        return {'ошибка': 'возможно указан неправильный путь до аудиофайла'}


if __name__ == '__main__':
    uvicorn.run(
        app=application,
        host='127.0.0.1',
        port=8000,
    )
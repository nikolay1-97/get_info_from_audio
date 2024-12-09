"""Модель данных запроса"""
from pydantic import BaseModel


class RequestModel(BaseModel):
    """Модель данных запроса."""

    path_to_audio_file: str
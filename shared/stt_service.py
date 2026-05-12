"""Transcripción de voz a texto (Speech-to-Text).

Recibe bytes de audio OGG/OPUS (formato que envía Telegram) y devuelve texto.
Usa Google Speech Recognition, gratuito y sin API key.

Requisito del sistema: ffmpeg instalado y en el PATH.
  Instalar en Windows: winget install ffmpeg
Quien lo usa: telegram_bot.py
"""
from __future__ import annotations

import io

import speech_recognition as sr
from pydub import AudioSegment

from shared.logger import log_de

log = log_de("stt")


def transcribir_ogg(ogg_bytes: bytes, idioma: str = "es-ES") -> str:
    """Transcribe audio OGG/OPUS a texto.

    Devuelve cadena vacía si no se pudo entender el audio.
    Lanza RuntimeError si ffmpeg no está instalado.
    """
    try:
        audio = AudioSegment.from_file(io.BytesIO(ogg_bytes), format="ogg")
    except Exception as e:
        if "ffmpeg" in str(e).lower() or "avconv" in str(e).lower():
            raise RuntimeError(
                "ffmpeg no está instalado. Ejecuta en PowerShell: winget install ffmpeg\n"
                "Después cierra y vuelve a abrir la terminal."
            ) from e
        raise

    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)

    try:
        texto = recognizer.recognize_google(audio_data, language=idioma)
        log.info(f"STT ok: '{texto[:120]}'")
        return texto
    except sr.UnknownValueError:
        log.warning("STT: no se pudo entender el audio")
        return ""
    except sr.RequestError as e:
        log.error(f"STT: error de red con Google: {e}")
        raise RuntimeError(f"Error conectando con Google Speech: {e}") from e

"""Síntesis de voz para Durruti usando Microsoft Edge TTS.

Gratuito, sin API key, voces neurales de alta calidad en español.
Permite elegir voz via /voz en Telegram.
Quien lo usa: telegram_bot.py, scripts/test_voz.py
"""
from __future__ import annotations

import asyncio
import io
import os
import tempfile
from pathlib import Path

import edge_tts

from shared.logger import log_de

log = log_de("tts")

# Voz por defecto: Álvaro (masculina, español de España, neural)
VOZ_POR_DEFECTO = "es-ES-AlvaroNeural"

# Voces recomendadas en español para que el usuario elija
VOCES_ESPANOL = [
    {"id": "es-ES-AlvaroNeural",   "nombre": "Alvaro (ES)",   "genero": "M"},
    {"id": "es-ES-ElviraNeural",   "nombre": "Elvira (ES)",   "genero": "F"},
    {"id": "es-MX-JorgeNeural",    "nombre": "Jorge (MX)",    "genero": "M"},
    {"id": "es-MX-DaliaNeural",    "nombre": "Dalia (MX)",    "genero": "F"},
    {"id": "es-AR-TomasNeural",    "nombre": "Tomas (AR)",    "genero": "M"},
    {"id": "es-AR-ElenaNeural",    "nombre": "Elena (AR)",    "genero": "F"},
    {"id": "es-CO-GonzaloNeural",  "nombre": "Gonzalo (CO)",  "genero": "M"},
    {"id": "es-US-AlonsoNeural",   "nombre": "Alonso (US-ES)","genero": "M"},
]


def listar_voces() -> list[dict]:
    """Devuelve las voces en español disponibles."""
    return VOCES_ESPANOL


def sintetizar(texto: str, voice_id: str | None = None) -> bytes:
    """Convierte texto a audio MP3. Devuelve bytes. Síncrono."""
    voz = voice_id or os.getenv("DURRUTI_VOICE_ID", VOZ_POR_DEFECTO)

    async def _generar() -> bytes:
        communicate = edge_tts.Communicate(texto, voz)
        chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)

    audio = asyncio.run(_generar())
    log.info(f"TTS: {len(audio)} bytes, voz={voz}, chars={len(texto)}")
    return audio


def guardar_voz_en_env(voice_id: str) -> None:
    """Persiste el voice_id en .env y en el proceso actual."""
    from dotenv import set_key
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        env_path.write_text(f"DURRUTI_VOICE_ID={voice_id}\n", encoding="utf-8")
    else:
        set_key(str(env_path), "DURRUTI_VOICE_ID", voice_id)
    os.environ["DURRUTI_VOICE_ID"] = voice_id
    log.info(f"Voz guardada: {voice_id}")

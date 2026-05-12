"""Test de voz con Microsoft Edge TTS (gratuito, sin API key).

Genera una frase de prueba con la voz configurada en .env y la reproduce.
Con --voces lista las voces disponibles en español.

Uso:
    uv run python scripts/test_voz.py
    uv run python scripts/test_voz.py --voces
"""
from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import os
import edge_tts
from playsound3 import playsound

FRASE = "Aqui estoy. Listo para trabajar contigo."
VOZ   = os.getenv("DURRUTI_VOICE_ID", "es-ES-AlvaroNeural")

VOCES_ESPANOL = [
    ("es-ES-AlvaroNeural",  "Alvaro  — hombre, España (actual)"),
    ("es-ES-ElviraNeural",  "Elvira  — mujer,  España"),
    ("es-MX-JorgeNeural",   "Jorge   — hombre, México"),
    ("es-MX-DaliaNeural",   "Dalia   — mujer,  México"),
    ("es-AR-TomasNeural",   "Tomas   — hombre, Argentina"),
]


async def probar_voz(voz: str, frase: str) -> None:
    print(f"\n  Voz: {voz}")
    communicate = edge_tts.Communicate(frase, voz)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp = f.name
    await communicate.save(tmp)
    size = Path(tmp).stat().st_size
    print(f"  Audio: {size} bytes")
    playsound(tmp)
    Path(tmp).unlink(missing_ok=True)


async def main() -> None:
    if "--voces" in sys.argv:
        print("\nProbando todas las voces en español:")
        for voz_id, desc in VOCES_ESPANOL:
            print(f"\n[{desc}]")
            await probar_voz(voz_id, FRASE)
    else:
        print(f"\nProbando voz configurada en .env:")
        await probar_voz(VOZ, FRASE)
        print("\nOK. Para probar todas las voces: uv run python scripts/test_voz.py --voces")


if __name__ == "__main__":
    asyncio.run(main())

"""Durruti — asistente de voz siempre activo.

Wake word : "Durruti"  (Whisper lo entiende con variantes: durruti, duruti, du ruti…)
Activacion: Durruti responde "Dime." y abre conversacion
Dormir    : di "a dormir" → micro y voz se apagan; trabajos en curso siguen vivos
Salida    : Ctrl+C

Uso:
    uv run python scripts/durruti_escucha.py
"""
from __future__ import annotations

import asyncio
import os
import queue
import sys
import tempfile
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import numpy as np
import sounddevice as sd
import soundfile as sf
import edge_tts
from playsound3 import playsound
from rich.console import Console

console = Console()

# ── Config ────────────────────────────────────────────────────────────
SAMPLE_RATE    = 16000
VOZ            = os.getenv("DURRUTI_VOICE_ID", "es-ES-AlvaroNeural")
SILENCIO_NIVEL = 0.008   # amplitud mínima para detectar voz
SILENCIO_CORTE = 2.5     # segundos de silencio para terminar turno
SILENCIO_MAX   = 20.0    # segundos sin hablar para volver a espera automáticamente

# Variantes fonéticas que Whisper produce para "Durruti"
_WAKE = [
    "durruti", "duruti", "du ruti", "de ruti", "durr", "druti",
    "durrute", "durrutti", "duro ti", "du rti", "durti",
]

# Comandos de dormir
_DORMIR = [
    "a dormir", "duerme", "descansa", "silencio", "modo silencio",
    "para de hablar", "cierra la boca", "calla",
]

# Bloqueo mientras Durruti habla (para no grabarse a sí mismo)
_hablando = threading.Event()

# ── Cliente Groq ──────────────────────────────────────────────────────
from groq import Groq as _Groq
_groq_client = _Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── TTS ───────────────────────────────────────────────────────────────
def hablar(texto: str) -> None:
    """Sintetiza y reproduce. Bloquea el micro mientras habla."""
    _hablando.set()
    try:
        async def _gen():
            communicate = edge_tts.Communicate(texto, VOZ)
            tmp = tempfile.mktemp(suffix=".mp3")
            await communicate.save(tmp)
            return tmp
        mp3 = asyncio.run(_gen())
        playsound(mp3)
        Path(mp3).unlink(missing_ok=True)
    finally:
        time.sleep(0.3)
        _hablando.clear()

def hablar_async(texto: str) -> None:
    """Lanza hablar() en hilo daemon (no bloquea el flujo principal)."""
    threading.Thread(target=hablar, args=(texto,), daemon=True).start()

# ── STT via Groq Whisper Large v3 ────────────────────────────────────
def transcribir(audio: np.ndarray) -> str:
    if len(audio) < SAMPLE_RATE * 0.3:
        return ""
    tmp = tempfile.mktemp(suffix=".wav")
    sf.write(tmp, audio, SAMPLE_RATE)
    try:
        with open(tmp, "rb") as f:
            resp = _groq_client.audio.transcriptions.create(
                file=("audio.wav", f.read()),
                model="whisper-large-v3",
                language="es",
                response_format="text",
            )
        return (resp if isinstance(resp, str) else resp.text).strip().lower()
    except Exception as e:
        console.print(f"[red]STT error: {e}[/red]")
        return ""
    finally:
        Path(tmp).unlink(missing_ok=True)

# ── Detección de intención ────────────────────────────────────────────
def es_wake_word(t: str) -> bool:
    return any(v in t for v in _WAKE)

def es_dormir(t: str) -> bool:
    return any(p in t for p in _DORMIR)

# ── Grabación ─────────────────────────────────────────────────────────
def grabar_chunk(segs: float) -> np.ndarray:
    """Bloque fijo de audio para detección de wake word."""
    n = int(SAMPLE_RATE * segs)
    audio = sd.rec(n, samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def grabar_turno() -> tuple[np.ndarray, float]:
    """Graba hasta silencio. Devuelve (audio, segundos_de_silencio_al_final)."""
    frames: list[np.ndarray] = []
    ultimo_sonido = time.time()
    inicio = time.time()
    cola: queue.Queue = queue.Queue()

    def cb(indata, *_):
        if not _hablando.is_set():
            cola.put(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                        dtype="float32", callback=cb, blocksize=1024):
        while True:
            try:
                bloque = cola.get(timeout=0.1)
            except queue.Empty:
                continue
            frames.append(bloque)
            if float(np.abs(bloque).mean()) > SILENCIO_NIVEL:
                ultimo_sonido = time.time()
            silencio = time.time() - ultimo_sonido
            duracion  = time.time() - inicio
            if duracion > 0.8 and silencio >= SILENCIO_CORTE:
                break
            if duracion > 40:
                break

    audio = np.concatenate(frames).flatten() if frames else np.array([], dtype="float32")
    return audio, time.time() - ultimo_sonido

# ── Modos ─────────────────────────────────────────────────────────────
def modo_espera() -> None:
    """Escucha en silencio hasta oír 'Durruti'."""
    console.print("[dim]Esperando... di [bold]'Durruti'[/bold][/dim]")
    while True:
        audio = grabar_chunk(2.5)
        if _hablando.is_set() or float(np.abs(audio).mean()) < 0.002:
            continue
        texto = transcribir(audio)
        if texto:
            console.print(f"[dim]>> {texto}[/dim]")
        if es_wake_word(texto):
            return  # sale para entrar en modo_conversacion


def modo_conversacion() -> None:
    """Conversación activa. 'A dormir' la suspende sin matar trabajos."""
    from shared.conversacion import Conversacion

    console.print("\n[bold green]=== DURRUTI ACTIVO ===[/bold green]")

    try:
        conv = Conversacion()
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        hablar("No tengo la clave de Groq. Revisa el punto env.")
        return

    hablar_async("Dime.")
    time.sleep(1.2)

    ultimo_habla = time.time()

    while True:
        console.print("[cyan]Escuchando...[/cyan]")
        audio, silencio_final = grabar_turno()

        # Silencio prolongado → volver a espera sin anuncio de voz
        if time.time() - ultimo_habla > SILENCIO_MAX:
            console.print("[dim]Silencio prolongado. Volviendo a espera.[/dim]")
            return

        if len(audio) < SAMPLE_RATE * 0.4:
            continue

        texto = transcribir(audio)
        if not texto:
            continue

        console.print(f"[bold blue]Tú:[/bold blue] {texto}")
        ultimo_habla = time.time()

        # Comando dormir
        if es_dormir(texto):
            hablar("Descansando. Llámame cuando me necesites.")
            console.print("[dim]Micro y voz apagados. Los trabajos siguen. Di 'Durruti' para volver.[/dim]\n")
            return

        # LLM
        console.print("[dim]...[/dim]")
        try:
            respuesta = conv.responder(texto)
        except Exception as e:
            console.print(f"[red]LLM error: {str(e)[:120]}[/red]")
            respuesta = "Ha habido un error. Intenta de nuevo."

        console.print(f"[bold green]Durruti:[/bold green] {respuesta}")
        hablar(respuesta)
        ultimo_habla = time.time()

# ── Main ──────────────────────────────────────────────────────────────
def main() -> None:
    console.print("[bold cyan]Durruti — escucha permanente[/bold cyan]")
    console.print(f"Wake word: [bold]Durruti[/bold]   |   Dormir: [bold]'a dormir'[/bold]   |   Salir: Ctrl+C")
    console.print(f"Voz: [dim]{VOZ}[/dim]\n")

    hablar_async("Sistema iniciado.")

    try:
        while True:
            modo_espera()
            modo_conversacion()
    except KeyboardInterrupt:
        console.print("\n[dim]Detenido. Los trabajos en curso siguen si los lanzaste aparte.[/dim]")

if __name__ == "__main__":
    main()

"""Bakunin — asistente tecnico de voz siempre activo.

Wake word : "Bakunin"
Activacion: responde "Dime." y abre conversacion
Dormir    : di "a dormir" → micro y voz se apagan; trabajos siguen vivos
Salida    : Ctrl+C

Diferencia con Durruti: Bakunin es el tecnico. Habla de codigo, sistema,
archivos, herramientas. Durruti es el CEO de negocio.

Uso:
    uv run python scripts/bakunin_escucha.py
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
VOZ            = "es-ES-ElviraNeural"   # voz distinta a Durruti para distinguirlos
SILENCIO_NIVEL = 0.008
SILENCIO_CORTE = 2.5
SILENCIO_MAX   = 20.0

SYSTEM_PROMPT = """Eres Bakunin, asistente tecnico del Founder de FORRARSE. Hablas siempre en castellano.

CARACTER: Tecnico, directo, sin rodeos. Tuteas al Founder. Cero protocolo.
Si algo no lo sabes, lo dices claro. Humor seco cuando toca.

REGLAS PARA VOZ:
- Maximo 2-3 frases por respuesta salvo que te pidan mas detalle.
- Cero markdown: sin asteriscos, sin guiones, sin listas. Solo texto hablado natural.
- No repitas lo que acaba de decir el Founder. Ve directo.

CAPACIDADES: codigo, sistema, herramientas, arquitectura, debugging, cualquier tema tecnico.
Recuerdas toda la conversacion de esta sesion.

IDENTIDAD: El Founder es quien habla contigo. Durruti es el CEO de negocio (colega tuyo)."""

# Variantes fonicas de "Bakunin"
_WAKE = [
    "bakunin", "bakun", "bakunen", "bakunim", "vakun", "vakunin",
    "bacunin", "bakounin", "baku nin", "ba kunin",
]

_DORMIR = [
    "a dormir", "duerme", "descansa", "silencio", "modo silencio",
    "para de hablar", "cierra la boca", "calla",
]

_hablando = threading.Event()

# ── Groq ──────────────────────────────────────────────────────────────
from groq import Groq as _Groq
_groq_client = _Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── TTS ───────────────────────────────────────────────────────────────
def hablar(texto: str) -> None:
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
    threading.Thread(target=hablar, args=(texto,), daemon=True).start()

# ── STT ───────────────────────────────────────────────────────────────
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

# ── Deteccion ─────────────────────────────────────────────────────────
def es_wake_word(t: str) -> bool:
    return any(v in t for v in _WAKE)

def es_dormir(t: str) -> bool:
    return any(p in t for p in _DORMIR)

# ── Grabacion ─────────────────────────────────────────────────────────
def grabar_chunk(segs: float) -> np.ndarray:
    n = int(SAMPLE_RATE * segs)
    audio = sd.rec(n, samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def grabar_turno() -> tuple[np.ndarray, float]:
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
            silencio  = time.time() - ultimo_sonido
            duracion  = time.time() - inicio
            if duracion > 0.8 and silencio >= SILENCIO_CORTE:
                break
            if duracion > 40:
                break

    audio = np.concatenate(frames).flatten() if frames else np.array([], dtype="float32")
    return audio, time.time() - ultimo_sonido

# ── Modos ─────────────────────────────────────────────────────────────
def modo_espera() -> None:
    console.print("[dim]Esperando... di [bold]'Bakunin'[/bold][/dim]")
    while True:
        audio = grabar_chunk(2.5)
        if _hablando.is_set() or float(np.abs(audio).mean()) < 0.002:
            continue
        texto = transcribir(audio)
        if texto:
            console.print(f"[dim]>> {texto}[/dim]")
        if es_wake_word(texto):
            return


def modo_conversacion() -> None:
    from groq import Groq

    console.print("\n[bold magenta]=== BAKUNIN ACTIVO ===[/bold magenta]")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[red]GROQ_API_KEY no configurada.[/red]")
        hablar("No tengo la clave de Groq. Revisa el punto env.")
        return

    client = Groq(api_key=api_key)
    historial: list[dict] = []

    hablar_async("Dime.")
    time.sleep(1.2)

    ultimo_habla = time.time()

    while True:
        console.print("[magenta]Escuchando...[/magenta]")
        audio, _ = grabar_turno()

        if time.time() - ultimo_habla > SILENCIO_MAX:
            console.print("[dim]Silencio prolongado. Volviendo a espera.[/dim]")
            return

        if len(audio) < SAMPLE_RATE * 0.4:
            continue

        texto = transcribir(audio)
        if not texto:
            continue

        console.print(f"[bold blue]Tu:[/bold blue] {texto}")
        ultimo_habla = time.time()

        if es_dormir(texto):
            hablar("Descansando. Llámame cuando me necesites.")
            console.print("[dim]Micro y voz apagados. Di 'Bakunin' para volver.[/dim]\n")
            return

        console.print("[dim]...[/dim]")
        historial.append({"role": "user", "content": texto})
        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=180,
                temperature=0.7,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial,
            )
            respuesta = resp.choices[0].message.content.strip()
            historial.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            console.print(f"[red]LLM error: {str(e)[:120]}[/red]")
            respuesta = "Ha habido un error. Intenta de nuevo."

        console.print(f"[bold magenta]Bakunin:[/bold magenta] {respuesta}")
        hablar(respuesta)
        ultimo_habla = time.time()

# ── Main ──────────────────────────────────────────────────────────────
def main() -> None:
    console.print("[bold magenta]Bakunin — asistente tecnico[/bold magenta]")
    console.print(f"Wake word: [bold]Bakunin[/bold]   |   Dormir: [bold]'a dormir'[/bold]   |   Salir: Ctrl+C")
    console.print(f"Voz: [dim]{VOZ}[/dim]\n")

    hablar_async("Sistema iniciado.")

    try:
        while True:
            modo_espera()
            modo_conversacion()
    except KeyboardInterrupt:
        console.print("\n[dim]Detenido.[/dim]")

if __name__ == "__main__":
    main()

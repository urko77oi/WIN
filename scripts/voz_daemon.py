"""Voz Daemon — Bakunin y Durruti siempre disponibles.

Wake words:
  "Bakunin" -> asistente tecnico (voz: Elvira, magenta)
  "Durruti"  -> CEO de FORRARSE  (voz: Alvaro, verde)

Wake word : Groq Whisper Large v3 (reconoce nombres propios correctamente)
Conversacion: Groq Whisper Large v3 (calidad maxima)
LLM       : Groq Llama 3.3 70B

Nunca muere: cualquier excepcion reinicia el bucle automaticamente.
VS Code lo lanza solo al abrir la carpeta (ver .vscode/tasks.json).

Uso manual: uv run python scripts/voz_daemon.py
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
SILENCIO_NIVEL = 0.008
SILENCIO_CORTE = 2.5
SILENCIO_MAX   = 20.0

VOZ_BAKUNIN = "es-ES-ElviraNeural"
VOZ_DURRUTI = "es-ES-AlvaroNeural"

SYSTEM_BAKUNIN = """Eres Bakunin, asistente tecnico del Founder de FORRARSE. Hablas siempre en castellano.
CARACTER: Tecnico, directo, sin rodeos. Tuteas. Cero protocolo. Humor seco cuando toca.
REGLAS VOZ: Maximo 2-3 frases. Cero markdown. No repitas al Founder. Ve directo.
CAPACIDADES: codigo, sistema, herramientas, arquitectura, debugging, cualquier tema tecnico.
Recuerdas toda la conversacion de esta sesion."""

SYSTEM_DURRUTI = """Eres Durruti, CEO Operativo de FORRARSE. Hablas siempre en castellano.
CARACTER: Directo, inteligente, personalidad propia. Nada servil. Tuteas al Founder.
Tienes criterio: si algo no te parece bien, lo dices. Humor seco ocasional.
REGLAS VOZ: Maximo 2-3 frases. Cero markdown. No repitas al Founder. Ve directo.
CAPACIDADES: cualquier tema. FORRARSE (nichos, landings, etc.). Recuerdas toda la sesion.
IDENTIDAD: Tu equipo: Scout y Domenech."""

# Variantes fonicas
_WAKE_BAKUNIN = [
    "bakunin", "bakun", "bakunen", "bakunim", "vakun", "vakunin",
    "bacunin", "bakounin", "baku nin", "ba kunin",
    "macun", "makun", "bacun", "bakune", "bakunin",
]
_WAKE_DURRUTI = [
    "durruti", "duruti", "du ruti", "de ruti", "durr", "druti",
    "durrute", "durrutti", "duro ti", "du rti", "durti",
    "dorote", "dorotea", "durote", "de rote",
]
_DORMIR = [
    "a dormir", "duerme", "descansa", "silencio",
    "para de hablar", "cierra la boca", "calla",
]

_hablando = threading.Event()

# ── Groq ──────────────────────────────────────────────────────────────
from groq import Groq as _Groq
_groq = _Groq(api_key=os.getenv("GROQ_API_KEY"))
console.print("[green]Listo.[/green]")

# ── Auto-mejora: instala paquetes declarados por los agentes ──────────
def _auto_mejora() -> None:
    needs_file = PROJECT_ROOT / "needs" / "packages.txt"
    if not needs_file.exists():
        return
    pendientes = [
        l.strip() for l in needs_file.read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.startswith("#")
    ]
    if not pendientes:
        return
    console.print(f"[yellow]Auto-mejora: instalando {pendientes}[/yellow]")
    import subprocess
    for pkg in pendientes:
        result = subprocess.run(
            ["uv", "add", pkg, "--link-mode=copy"],
            cwd=str(PROJECT_ROOT), capture_output=True, text=True
        )
        if result.returncode == 0:
            console.print(f"[green]  + {pkg} instalado[/green]")
        else:
            console.print(f"[red]  ! {pkg} fallo: {result.stderr[:80]}[/red]")
    # Limpia el archivo tras instalar
    needs_file.write_text("", encoding="utf-8")

# ── TTS ───────────────────────────────────────────────────────────────
def hablar(texto: str, voz: str) -> None:
    _hablando.set()
    try:
        async def _gen():
            communicate = edge_tts.Communicate(texto, voz)
            tmp = tempfile.mktemp(suffix=".mp3")
            await communicate.save(tmp)
            return tmp
        mp3 = asyncio.run(_gen())
        playsound(mp3)
        Path(mp3).unlink(missing_ok=True)
    except Exception as e:
        console.print(f"[red]TTS error: {e}[/red]")
    finally:
        time.sleep(0.3)
        _hablando.clear()

def hablar_async(texto: str, voz: str) -> None:
    threading.Thread(target=hablar, args=(texto, voz), daemon=True).start()

# ── STT — Groq Whisper Large v3 (wake word y conversacion) ───────────
def transcribir_wake(audio: np.ndarray) -> str:
    return _transcribir_groq(audio)

def transcribir_conv(audio: np.ndarray) -> str:
    return _transcribir_groq(audio)

def _transcribir_groq(audio: np.ndarray) -> str:
    if len(audio) < SAMPLE_RATE * 0.4:
        return ""
    tmp = tempfile.mktemp(suffix=".wav")
    sf.write(tmp, audio, SAMPLE_RATE)
    try:
        with open(tmp, "rb") as f:
            resp = _groq.audio.transcriptions.create(
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
def detectar_wake(t: str) -> str | None:
    """Devuelve 'bakunin', 'durruti' o None."""
    if any(v in t for v in _WAKE_BAKUNIN):
        return "bakunin"
    if any(v in t for v in _WAKE_DURRUTI):
        return "durruti"
    return None

def es_dormir(t: str) -> bool:
    return any(p in t for p in _DORMIR)

# ── Grabacion ─────────────────────────────────────────────────────────
def grabar_chunk(segs: float = 1.5) -> np.ndarray:
    n = int(SAMPLE_RATE * segs)
    audio = sd.rec(n, samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def grabar_turno() -> np.ndarray:
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

    return np.concatenate(frames).flatten() if frames else np.array([], dtype="float32")

# ── Conversacion ──────────────────────────────────────────────────────
def modo_conversacion(agente: str) -> None:
    voz    = VOZ_BAKUNIN if agente == "bakunin" else VOZ_DURRUTI
    system = SYSTEM_BAKUNIN if agente == "bakunin" else SYSTEM_DURRUTI
    color  = "magenta" if agente == "bakunin" else "green"
    nombre = agente.capitalize()

    console.print(f"\n[bold {color}]=== {nombre.upper()} ACTIVO ===[/bold {color}]")
    hablar_async("Dime.", voz)
    time.sleep(1.2)

    historial: list[dict] = []
    ultimo_habla = time.time()

    while True:
        console.print(f"[{color}]Escuchando...[/{color}]")
        audio = grabar_turno()

        if time.time() - ultimo_habla > SILENCIO_MAX:
            console.print("[dim]Silencio prolongado. Volviendo a espera.[/dim]")
            return

        if len(audio) < SAMPLE_RATE * 0.4:
            continue

        texto = transcribir_conv(audio)
        if not texto:
            continue

        console.print(f"[bold blue]Tu:[/bold blue] {texto}")
        ultimo_habla = time.time()

        if es_dormir(texto):
            hablar(f"Descansando. Llamamе cuando me necesites.", voz)
            console.print(f"[dim]Di '{nombre}' para volver.[/dim]\n")
            return

        console.print("[dim]...[/dim]")
        historial.append({"role": "user", "content": texto})
        try:
            resp = _groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=180,
                temperature=0.7,
                messages=[{"role": "system", "content": system}] + historial,
            )
            respuesta = resp.choices[0].message.content.strip()
            historial.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            console.print(f"[red]LLM error: {str(e)[:120]}[/red]")
            respuesta = "Ha habido un error. Intenta de nuevo."

        console.print(f"[bold {color}]{nombre}:[/bold {color}] {respuesta}")
        hablar(respuesta, voz)
        ultimo_habla = time.time()

# ── Main loop (nunca muere) ───────────────────────────────────────────
def main() -> None:
    console.print("[bold cyan]Voz Daemon[/bold cyan] — Bakunin + Durruti")
    console.print("Wake words: [bold magenta]Bakunin[/bold magenta]  |  [bold green]Durruti[/bold green]")
    console.print("Dormir: 'a dormir'  |  Salir: Ctrl+C\n")

    _auto_mejora()
    hablar_async("Sistema iniciado. Llamamе cuando me necesites.", VOZ_BAKUNIN)

    try:
        while True:
            try:
                console.print("[dim]Esperando...[/dim]")
                audio = grabar_chunk(1.5)
                if _hablando.is_set() or float(np.abs(audio).mean()) < 0.002:
                    continue
                texto = transcribir_wake(audio)
                if not texto:
                    continue
                console.print(f"[dim]>> {texto}[/dim]")
                agente = detectar_wake(texto)
                if agente:
                    modo_conversacion(agente)
            except Exception as e:
                console.print(f"[red]Error (reiniciando en 2s): {e}[/red]")
                time.sleep(2)
    except KeyboardInterrupt:
        console.print("\n[dim]Detenido.[/dim]")

if __name__ == "__main__":
    main()

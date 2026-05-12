"""Conversacion en tiempo real con Durruti por voz.

Flujo:
  1. Pulsa ENTER para empezar a hablar.
  2. Habla. Pulsa ENTER de nuevo (o espera silencio) para terminar.
  3. Durruti transcribe, procesa y responde por voz.
  4. Repite.

Escribe 'salir' para terminar.

Uso:
    uv run python scripts/voz_chat.py
"""
from __future__ import annotations

import asyncio
import os
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
from faster_whisper import WhisperModel
from playsound3 import playsound
from rich.console import Console
from rich.panel import Panel

console = Console()

SAMPLE_RATE = 16000
CANALES = 1
VOZ = os.getenv("DURRUTI_VOICE_ID", "es-ES-AlvaroNeural")
SILENCE_THRESHOLD = 0.01   # amplitud minima para considerar que hay voz
SILENCE_DURATION = 1.8     # segundos de silencio para cortar la grabacion

# ─────────────────────────────────────────────────────────────────────
# Cargar modelo Whisper (tiny = rapido, sin GPU necesaria)
# ─────────────────────────────────────────────────────────────────────

console.print("[dim]Cargando modelo de transcripcion (primera vez puede tardar ~30s)...[/dim]")
_whisper = WhisperModel("tiny", device="cpu", compute_type="int8")
console.print("[green]Modelo listo.[/green]")


# ─────────────────────────────────────────────────────────────────────
# Captura de audio con deteccion automatica de silencio
# ─────────────────────────────────────────────────────────────────────

def grabar_hasta_silencio() -> np.ndarray:
    """Graba desde el microfono hasta detectar silencio prolongado."""
    console.print("[cyan]Escuchando... (habla ahora)[/cyan]")

    frames = []
    ultimo_sonido = time.time()
    grabando = True

    def callback(indata, frame_count, time_info, status):
        nonlocal ultimo_sonido, grabando
        frames.append(indata.copy())
        amplitud = np.abs(indata).mean()
        if amplitud > SILENCE_THRESHOLD:
            ultimo_sonido = time.time()
        elif time.time() - ultimo_sonido > SILENCE_DURATION and len(frames) > int(SAMPLE_RATE / 1024 * 1.5):
            grabando = False

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CANALES, dtype="float32", callback=callback, blocksize=1024):
        while grabando:
            time.sleep(0.05)

    if not frames:
        return np.array([], dtype="float32")
    return np.concatenate(frames, axis=0).flatten()


# ─────────────────────────────────────────────────────────────────────
# Transcripcion con Whisper
# ─────────────────────────────────────────────────────────────────────

def transcribir(audio: np.ndarray) -> str:
    if len(audio) < SAMPLE_RATE * 0.5:
        return ""

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, SAMPLE_RATE)
        tmp_wav = f.name

    segments, _ = _whisper.transcribe(tmp_wav, language="es", beam_size=1)
    texto = " ".join(s.text for s in segments).strip()
    Path(tmp_wav).unlink(missing_ok=True)
    return texto


# ─────────────────────────────────────────────────────────────────────
# Sintesis y reproduccion de voz
# ─────────────────────────────────────────────────────────────────────

def hablar(texto: str) -> None:
    async def _gen():
        communicate = edge_tts.Communicate(texto, VOZ)
        tmp = tempfile.mktemp(suffix=".mp3")
        await communicate.save(tmp)
        return tmp

    tmp_mp3 = asyncio.run(_gen())
    playsound(tmp_mp3)
    Path(tmp_mp3).unlink(missing_ok=True)


# ─────────────────────────────────────────────────────────────────────
# Durruti en modo conversacion
# ─────────────────────────────────────────────────────────────────────

def procesar_con_durruti(texto: str) -> str:
    """Llama a Durruti y devuelve la respuesta en texto."""
    from agents.durruti import Durruti
    from shared.human_channel import CLIChannel

    class _SilentChannel(CLIChannel):
        """Canal mudo: captura la respuesta sin imprimirla (ya la mostramos nosotros)."""
        def __init__(self):
            self._last = ""
        def notificar(self, mensaje: str) -> None:
            self._last = mensaje
        def alertar(self, mensaje: str) -> None:
            self._last = mensaje

    canal = _SilentChannel()
    d = Durruti(canal=canal)
    resultado = d.procesar(texto)
    return resultado.texto_para_humano


# ─────────────────────────────────────────────────────────────────────
# Bucle principal
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    console.print(Panel(
        "[bold]Durruti[/bold] - Conversacion por voz\n\n"
        "Habla cuando veas 'Escuchando...'\n"
        "Pausa 2 segundos para que Durruti responda.\n"
        "Escribe [bold]salir[/bold] y Enter para terminar.",
        border_style="cyan",
    ))

    # Saludo inicial por voz
    hablar("Listo, mi amo. Estoy escuchando. Dime que necesitas.")

    while True:
        try:
            console.print("\n[dim]Pulsa ENTER para hablar (o escribe 'salir')...[/dim]", end="")
            entrada = input()
            if entrada.strip().lower() in ("salir", "exit", "quit"):
                hablar("Hasta pronto.")
                console.print("[dim]Hasta pronto.[/dim]")
                break

            # Grabar
            audio = grabar_hasta_silencio()
            if len(audio) == 0:
                continue

            # Transcribir
            console.print("[dim]Transcribiendo...[/dim]")
            texto = transcribir(audio)
            if not texto:
                hablar("No te he entendido bien. Repite, por favor.")
                continue

            console.print(Panel(f"[bold cyan]Tu:[/bold cyan] {texto}", border_style="blue"))

            # Procesar con Durruti
            console.print("[dim]Durruti pensando...[/dim]")
            respuesta = procesar_con_durruti(texto)

            console.print(Panel(f"[bold green]Durruti:[/bold green] {respuesta[:400]}", border_style="green"))

            # Responder por voz (maximo 600 chars para TTS fluido)
            tts_text = respuesta[:600]
            hablar(tts_text)

        except KeyboardInterrupt:
            hablar("Hasta pronto.")
            console.print("\n[dim]Hasta pronto.[/dim]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            hablar("Ha habido un error. Intentalo de nuevo.")


if __name__ == "__main__":
    main()

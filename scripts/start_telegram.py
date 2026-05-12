"""Arranca Durruti en modo Telegram.

Uso:
    uv run python scripts/start_telegram.py

Requisitos previos (en .env):
    TELEGRAM_BOT_TOKEN   — token de tu bot (obtenido de @BotFather)
    TELEGRAM_CHAT_ID     — tu ID de Telegram (manda /start al bot y aparece en logs)
    ELEVENLABS_API_KEY   — para que Durruti hable (opcional, si no hay solo texto)

Requisito del sistema para mensajes de voz entrantes:
    winget install ffmpeg
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import os  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402

console = Console()


def _validar_config() -> bool:
    """Comprueba que las variables mínimas están configuradas."""
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        console.print(Panel(
            "TELEGRAM_BOT_TOKEN no configurado.\n"
            "Obtenlo de @BotFather en Telegram y ponlo en .env",
            title="[red]Falta TELEGRAM_BOT_TOKEN en .env[/red]",
            border_style="red",
        ))
        return False
    if not os.getenv("TELEGRAM_CHAT_ID"):
        console.print(Panel(
            "TELEGRAM_CHAT_ID vacío — modo detección.\n"
            "Manda /start al bot desde Telegram y el ID aparecerá aquí.",
            title="[yellow]Esperando Chat ID[/yellow]",
            border_style="yellow",
        ))
    return True


def _banner() -> None:
    modo = os.getenv("LLM_MODE", "mock")
    color_modo = "yellow" if modo == "mock" else "green"
    voz = os.getenv("DURRUTI_VOICE_ID", "es-ES-AlvaroNeural")
    voz_estado = f"[green]ON (edge-tts: {voz})[/green]"
    texto = (
        f"[bold]Durruti[/bold] - modo Telegram\n"
        f"LLM: [{color_modo}]{modo}[/{color_modo}]   Voz: {voz_estado}\n\n"
        f"Abre Telegram y habla con tu bot.\n"
        f"Ctrl+C para detener."
    )
    console.print(Panel(texto, border_style="cyan"))


def main() -> int:
    if not _validar_config():
        return 1
    _banner()

    try:
        from shared.telegram_bot import crear_y_arrancar
        crear_y_arrancar()
    except KeyboardInterrupt:
        console.print("\n[dim]Bot detenido.[/dim]")
    except Exception as e:
        console.print(Panel(
            f"{e}\n\nEjecuta [bold]uv run python scripts/doctor.py[/bold] para diagnóstico.",
            title="[red]Error arrancando el bot[/red]",
            border_style="red",
        ))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

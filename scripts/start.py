"""Arranca Durruti en CLI.

Uso:
    uv run python scripts/start.py

Loop simple: lee orden del usuario, se la pasa a Durruti, imprime resultado.
Para salir: `salir`, `exit`, o Ctrl+C.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Hace que `import shared`, `import agents` funcionen sin instalar el paquete.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from agents.durruti import Durruti  # noqa: E402
from shared.human_channel import CLIChannel  # noqa: E402
from shared.logger import log_de  # noqa: E402

log = log_de("start")
console = Console()


def _banner() -> None:
    import os
    modo = os.getenv("LLM_MODE", "mock").strip().lower()
    if modo == "real":
        backend = "[green]Anthropic Claude (real)[/green]"
    else:
        backend = "[yellow]Mock (sin creditos — cambia LLM_MODE=real en .env)[/yellow]"
    texto = (
        f"[bold]Durruti[/bold] — CEO Operativo\n"
        f"Backend: {backend}\n"
        f"Comandos: escribe tu orden en español, o 'salir' / 'exit' para terminar."
    )
    console.print(Panel(texto, border_style="cyan"))


def main() -> int:
    _banner()
    durruti = Durruti(canal=CLIChannel())

    while True:
        try:
            orden = console.input("[bold cyan]> [/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Hasta pronto.[/dim]")
            return 0

        if not orden:
            continue
        if orden.lower() in ("salir", "exit", "quit", ":q"):
            console.print("[dim]Hasta pronto.[/dim]")
            return 0

        try:
            durruti.procesar(orden)
        except Exception as e:
            log.exception("Fallo procesando orden")
            console.print(Panel(
                f"Algo ha fallado: {e}\n\n"
                f"Ejecuta `uv run python scripts/doctor.py` para diagnóstico.",
                title="[red]Error[/red]",
                border_style="red",
            ))


if __name__ == "__main__":
    raise SystemExit(main())

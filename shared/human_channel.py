"""Canal de comunicación con el humano.

Interfaz abstracta para que Durruti pueda:
  - Notificar info / alertas.
  - Solicitar aprobación con motivos y coste estimado.
  - Hacer preguntas abiertas.

Implementaciones:
  - `CLIChannel`: interactivo en terminal. Único canal de Fase 0.
  - `TelegramChannel` (Fase 1+): mismo interfaz, detrás bot de Telegram.

Quien lo usa: Durruti, principalmente. También scripts auxiliares.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from shared.logger import log_de

log = log_de("human")
_console = Console()


@dataclass(frozen=True)
class Aprobacion:
    """Resultado de una solicitud de aprobación humana."""
    aprobada: bool
    comentario: str = ""


class HumanChannel(ABC):
    """Interfaz común. Telegram heredará esto en Fase 1."""

    @abstractmethod
    def notificar(self, mensaje: str) -> None: ...

    @abstractmethod
    def alertar(self, mensaje: str) -> None: ...

    @abstractmethod
    def preguntar(self, pregunta: str) -> str: ...

    @abstractmethod
    def solicitar_aprobacion(
        self,
        *,
        accion: str,
        motivos: list[str],
        coste_estimado_eur: float = 0.0,
        contexto: str = "",
    ) -> Aprobacion: ...


# ─────────────────────────────────────────────────────────────────────
# Implementación CLI (Fase 0)
# ─────────────────────────────────────────────────────────────────────

class CLIChannel(HumanChannel):
    """Canal interactivo por terminal."""

    def notificar(self, mensaje: str) -> None:
        _console.print(Panel(mensaje, title="[blue]Durruti — info[/blue]", border_style="blue"))
        log.info(f"[notif] {mensaje[:200]}")

    def alertar(self, mensaje: str) -> None:
        _console.print(Panel(mensaje, title="[red]Durruti — alerta[/red]", border_style="red"))
        log.warning(f"[alerta] {mensaje[:200]}")

    def preguntar(self, pregunta: str) -> str:
        _console.print(Panel(pregunta, title="[yellow]Durruti — pregunta[/yellow]", border_style="yellow"))
        respuesta = Prompt.ask("> ")
        log.info(f"[pregunta] {pregunta[:120]} -> {respuesta[:120]}")
        return respuesta

    def solicitar_aprobacion(
        self,
        *,
        accion: str,
        motivos: list[str],
        coste_estimado_eur: float = 0.0,
        contexto: str = "",
    ) -> Aprobacion:
        cuerpo = (
            f"[bold]Acción propuesta:[/bold] {accion}\n"
            f"[bold]Motivos por los que pido OK:[/bold] {', '.join(motivos) or 'ninguno'}\n"
            f"[bold]Coste estimado:[/bold] {coste_estimado_eur:.4f} €\n"
        )
        if contexto:
            cuerpo += f"\n[dim]{contexto}[/dim]\n"
        _console.print(Panel(
            cuerpo,
            title="[magenta]Durruti — APROBACIÓN REQUERIDA[/magenta]",
            border_style="magenta",
        ))
        respuesta = Prompt.ask(
            "[bold]¿Apruebas?[/bold]",
            choices=["si", "no", "discutir"],
            default="no",
        )
        aprobada = respuesta == "si"
        comentario = ""
        if respuesta == "discutir":
            comentario = Prompt.ask("¿Qué quieres discutir?")
            aprobada = False
        log.info(f"[aprobacion] accion={accion!r} -> aprobada={aprobada} comentario={comentario!r}")
        return Aprobacion(aprobada=aprobada, comentario=comentario)


# ─────────────────────────────────────────────────────────────────────
# Stub para Telegram (Fase 1)
# ─────────────────────────────────────────────────────────────────────

class TelegramChannel(HumanChannel):
    """Implementación pendiente para Fase 1.

    Cuando se active: leerá `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` de
    `.env`, abrirá conexión con la API de Telegram Bot, enviará mensajes
    con botones inline para aprobar/rechazar, y bloqueará hasta recibir
    respuesta (con timeouts y reintentos según `runtime.espera_aprobacion_max_min`).
    """

    def __init__(self) -> None:
        raise NotImplementedError(
            "TelegramChannel se activa en Fase 1. "
            "Por ahora usa CLIChannel."
        )

    def notificar(self, mensaje: str) -> None: raise NotImplementedError
    def alertar(self, mensaje: str) -> None: raise NotImplementedError
    def preguntar(self, pregunta: str) -> str: raise NotImplementedError
    def solicitar_aprobacion(
        self,
        *,
        accion: str,
        motivos: list[str],
        coste_estimado_eur: float = 0.0,
        contexto: str = "",
    ) -> Aprobacion: raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Selector
# ─────────────────────────────────────────────────────────────────────

def canal_por_defecto() -> HumanChannel:
    """Devuelve el canal humano apropiado para esta fase.

    Fase 0: CLI siempre. Fase 1+: Telegram si está configurado, CLI como fallback.
    """
    return CLIChannel()

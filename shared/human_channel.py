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
# Implementación Telegram (Fase 1)
# ─────────────────────────────────────────────────────────────────────

class TelegramChannel(HumanChannel):
    """Canal Telegram. Delega el envío en shared.telegram_bot (importación lazy
    para evitar circular imports). Requiere que el bot esté corriendo."""

    def notificar(self, mensaje: str) -> None:
        from shared import telegram_bot as tb
        tb.enviar_texto_sync(mensaje)
        log.info(f"[telegram/notif] {mensaje[:120]}")

    def alertar(self, mensaje: str) -> None:
        from shared import telegram_bot as tb
        tb.enviar_texto_sync(f"⚠️ *ALERTA*\n\n{mensaje}")
        log.warning(f"[telegram/alerta] {mensaje[:120]}")

    def preguntar(self, pregunta: str) -> str:
        # En Fase 1 las preguntas abiertas se envían como texto.
        # El usuario responde en el siguiente mensaje; por ahora devolvemos
        # cadena vacía y Durruti reintentará si necesita la respuesta.
        from shared import telegram_bot as tb
        tb.enviar_texto_sync(f"❓ *Pregunta de Durruti:*\n\n{pregunta}")
        log.info(f"[telegram/pregunta] {pregunta[:120]}")
        return ""

    def solicitar_aprobacion(
        self,
        *,
        accion: str,
        motivos: list[str],
        coste_estimado_eur: float = 0.0,
        contexto: str = "",
    ) -> Aprobacion:
        from shared import telegram_bot as tb
        aprobada, comentario = tb.solicitar_aprobacion_sync(
            accion=accion,
            motivos=motivos,
            coste_estimado_eur=coste_estimado_eur,
            contexto=contexto,
        )
        log.info(f"[telegram/aprobacion] accion={accion!r} aprobada={aprobada}")
        return Aprobacion(aprobada=aprobada, comentario=comentario)


# ─────────────────────────────────────────────────────────────────────
# Selector
# ─────────────────────────────────────────────────────────────────────

def canal_por_defecto() -> HumanChannel:
    """CLI en Fase 0. Telegram si el token está configurado."""
    import os
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        return TelegramChannel()
    return CLIChannel()

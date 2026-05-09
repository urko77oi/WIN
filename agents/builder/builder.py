"""Implementación del Builder.

En Fase 0 todas las llamadas pasan por `llm_client.llamar(...)` en modo mock.
En Fase 1+ se le añadirá la habilidad de escribir archivos reales en `outputs/`.
"""
from __future__ import annotations

from pathlib import Path

from shared import llm_client
from shared.logger import PROJECT_ROOT, log_de

_AGENTE = "builder"
log = log_de(_AGENTE)

PROMPT_PATH: Path = PROJECT_ROOT / "agents" / "builder" / "system_prompt.md"


class Builder:
    """Agente constructor de entregables."""

    def __init__(self) -> None:
        self.system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    def proponer_landing(self, brief: str) -> str:
        """Devuelve propuesta de landing (estructura + copy) para revisión."""
        log.info(f"Proponiendo landing: {brief[:120]!r}")
        mensaje = (
            f"Brief para landing:\n\n{brief}\n\n"
            f"Devuelve: (1) estructura de bloques, (2) copy por bloque, "
            f"(3) decisiones por defecto que has tomado."
        )
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=mensaje,
            orden=brief[:120],
        )
        return resp.texto

    def generar_contenido(self, brief: str) -> str:
        """Devuelve borrador de contenido (post, hilo, email) para revisión."""
        log.info(f"Generando contenido: {brief[:120]!r}")
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=brief,
            orden=brief[:120],
        )
        return resp.texto

"""Implementación del Researcher.

En Fase 0 todas las llamadas pasan por `llm_client.llamar(...)`, que en
modo mock devuelve una respuesta plantilla. En Fase 1+ se le añadirán
herramientas (web search, fetch, scraping) en `shared/tools/`.
"""
from __future__ import annotations

from pathlib import Path

from shared import llm_client
from shared.logger import PROJECT_ROOT, log_de

_AGENTE = "researcher"
log = log_de(_AGENTE)

PROMPT_PATH: Path = PROJECT_ROOT / "agents" / "researcher" / "system_prompt.md"


class Researcher:
    """Agente de investigación."""

    def __init__(self) -> None:
        self.system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    def investigar(self, brief: str) -> str:
        """Devuelve un informe estructurado a partir de un brief."""
        log.info(f"Investigando: {brief[:120]!r}")
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=brief,
            orden=brief[:120],
        )
        return resp.texto

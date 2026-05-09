"""Implementación del Scout — Analista de Oportunidades.

Reemplaza al Researcher de la versión inicial de Fase 0. La identidad,
playbook, scoring y guardrails completos están en los archivos `.md` del
mismo directorio (definidos por el founder).

En Fase 0 todas las llamadas pasan por `llm_client.llamar(...)` en modo
mock. En Fase 1+ se le añadirán las tools externas descritas en
`tools.md` (Brave, Reddit, Google Trends, marketplaces, etc.) y el
heartbeat 24/7 descrito en `heartbeat.md`.
"""
from __future__ import annotations

from shared import llm_client
from shared.agent_loader import cargar_prompt_de
from shared.logger import log_de

_AGENTE = "scout"
log = log_de(_AGENTE)

# Archivos .md del Scout que se concatenan para formar su prompt completo.
# Orden pensado para que el modelo los lea de "quién soy" → "qué hago" →
# "cómo lo hago" → "límites".
_SCOUT_PROMPT_FILES: list[str] = [
    "identity.md",
    "mission.md",
    "system_prompt.md",
    "skills.md",
    "tools.md",
    "playbook.md",
    "scoring.md",
    "outputs.md",
    "guardrails.md",
]


class Scout:
    """Agente analista de oportunidades de negocio online."""

    def __init__(self) -> None:
        self.system_prompt = cargar_prompt_de(_AGENTE, _SCOUT_PROMPT_FILES)

    # ─────────────────────────────────────────────────────────────────
    # API que Durruti consume
    # ─────────────────────────────────────────────────────────────────

    def investigar(self, brief: str) -> str:
        """Procesa un briefing del founder (vía Durruti) y devuelve un memo
        estructurado con triple scoring y bandera de confianza.

        Mapeo a workflows internos del Scout:
        - Briefing manual → WF-1 (`playbook.md`).
        En Fase 0 todo es mock: el contenido es simulado pero la estructura
        es la real (TL;DR + triple scoring + hallazgos + riesgos + fuentes).
        """
        log.info(f"WF-1 (briefing): {brief[:120]!r}")
        mensaje = (
            f"Briefing recibido (vía Durruti, originalmente del founder):\n\n"
            f"«{brief}»\n\n"
            f"Aplica WF-1 (investigación dirigida) según tu playbook. Devuelve "
            f"el memo siguiendo el formato canónico (TL;DR, triple scoring, "
            f"hallazgos, riesgos, recomendación, fuentes)."
        )
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=mensaje,
            orden=brief[:120],
        )
        return resp.texto

    def auditar_competidor(self, competidor: str) -> str:
        """Análisis dirigido a un competidor concreto (S1.3 en `skills.md`)."""
        log.info(f"Auditando competidor: {competidor!r}")
        mensaje = (
            f"Audita al competidor: «{competidor}». Devuelve: tamaño "
            f"estimado, propuesta de valor, fortalezas, debilidades, gaps "
            f"explotables. Cita fuentes."
        )
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=mensaje,
            orden=competidor[:120],
        )
        return resp.texto

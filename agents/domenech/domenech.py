"""Implementación de Domenech — Builder (constructor) del equipo.

Reemplaza al Builder placeholder de la versión inicial de Fase 0. La
identidad, system_prompt, skills, playbooks, heartbeat, guardrails,
memoria, interfaces y output_templates completos están en los `.md` del
mismo directorio (definidos por el founder).

En Fase 0 todas las llamadas pasan por `llm_client.llamar(...)` en modo
mock. En Fase 1+:
- Se implementan las skills reales del catálogo (web.astro, saas.kit_basic,
  pay.stripe, deploy.vercel, etc.) en `shared/tools/`.
- Se materializan los contratos JSON (`BuildOrder`, `BuildPlan`,
  `MilestoneReport`, etc.) en `tasks/`.
- Se añaden los modos del heartbeat y la escalación agresiva ante bloqueo.
"""
from __future__ import annotations

from pathlib import Path

from shared import llm_client
from shared.logger import PROJECT_ROOT, log_de

_AGENTE = "domenech"
log = log_de(_AGENTE)

PROMPT_PATH: Path = PROJECT_ROOT / "agents" / "domenech" / "system_prompt.md"


class Domenech:
    """Agente constructor (Builder)."""

    def __init__(self) -> None:
        self.system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    # ─────────────────────────────────────────────────────────────────
    # API que Durruti consume
    # ─────────────────────────────────────────────────────────────────

    def proponer_landing(self, brief: str) -> str:
        """Devuelve propuesta de landing (estructura + copy + ADR de stack).

        En Fase 1+ ejecutará el Playbook 1 (`playbook.md` § Playbook 1):
        Hito 1 identidad → Hito 2 build (web.astro / web.next_static) →
        verificación → aprobación → producción → handoff.
        """
        log.info(f"Playbook 1 (landing): {brief[:120]!r}")
        mensaje = (
            f"Brief para landing (vía Durruti, originalmente del founder):\n\n"
            f"«{brief}»\n\n"
            f"Aplica Playbook 1 (landing). Devuelve: ADR de stack (Astro vs "
            f"Next vs HTML según el caso), estructura de bloques, copy por "
            f"bloque, hitos previstos con coste estimado, riesgos, decisiones "
            f"que requieren OK del founder."
        )
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=mensaje,
            orden=brief[:120],
        )
        return resp.texto

    def generar_contenido(self, brief: str) -> str:
        """Devuelve borrador de contenido (post, hilo, email, copy)."""
        log.info(f"Generando contenido: {brief[:120]!r}")
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=brief,
            orden=brief[:120],
        )
        return resp.texto

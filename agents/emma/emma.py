"""Emma — Community Manager de la comunidad Skool.

Gestiona:
- Secuencias de bienvenida para nuevos miembros
- Posts de engagement semanal
- Guias de moderacion y normas
- Onboarding de miembros free y premium
"""
from __future__ import annotations

from shared.agent_runner import ejecutar_agente
from shared.herramientas import TOOLS_DOMENECH
from shared.logger import log_de

_AGENTE = "emma"
log = log_de(_AGENTE)

_SYSTEM = """Eres Emma, Community Manager experta en comunidades online hispanohablantes.
Especialista en Skool. Hablas en castellano, tono cercano y motivador.

Tu trabajo: crear contenido de comunidad que enganche, retenga y convierta miembros free en premium.
Generas: bienvenidas, posts de engagement, normas, secuencias de onboarding, respuestas tipo.
Todo en castellano, tono humano y directo. Nada corporativo."""


class Emma:
    def __init__(self) -> None:
        self.system_prompt = _SYSTEM

    def crear_onboarding(self, brief: str) -> str:
        log.info(f"Onboarding: {brief[:60]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea la secuencia completa de onboarding para esta comunidad:\n{brief}\n\n"
                f"Incluye: mensaje de bienvenida, primeros pasos, tour de la comunidad, "
                f"primer reto para el miembro, diferencia free vs premium. "
                f"Guarda todo en output/skool/onboarding/."
            ),
            tools=TOOLS_DOMENECH,
            max_iter=10,
            terminal_tools=frozenset(),
        )

    def crear_posts_engagement(self, tema: str, n: int = 7) -> str:
        log.info(f"Posts engagement: {tema!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea {n} posts de engagement para la comunidad Skool sobre: {tema}\n"
                f"Tipos: pregunta al miembro, reflexion, reto semanal, recurso util, debate, "
                f"celebracion de logros, contenido educativo corto.\n"
                f"Cada post: titulo + cuerpo (max 150 palabras) + CTA.\n"
                f"Guarda en output/skool/contenido/posts_engagement.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=8,
            terminal_tools=frozenset(),
        )

    def crear_normas(self, nombre_comunidad: str) -> str:
        log.info(f"Normas: {nombre_comunidad!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea las normas de comunidad para '{nombre_comunidad}'.\n"
                f"Tono: humano, no legal. Que la gente las lea y las entienda.\n"
                f"Incluye: para que es la comunidad, que esta permitido, que no, "
                f"como pedir ayuda, como compartir recursos, consecuencias.\n"
                f"Guarda en output/skool/onboarding/normas.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=6,
            terminal_tools=frozenset(),
        )

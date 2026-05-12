"""Viral — Estratega de Redes Sociales.

Gestiona:
- Calendario editorial mensual (Instagram, TikTok, LinkedIn)
- Captions y hashtags optimizados
- Estrategia de crecimiento organico
- Contenido de captacion hacia Skool
"""
from __future__ import annotations

from shared.agent_runner import ejecutar_agente
from shared.herramientas import TOOLS_DOMENECH
from shared.logger import log_de

_AGENTE = "viral"
log = log_de(_AGENTE)

_SYSTEM = """Eres Viral, estratega de redes sociales especializado en crecimiento organico
para negocios dirigidos a autónomos y profesionales hispanohablantes.

Plataformas: Instagram, TikTok, LinkedIn. Sin trucos baratos, sin bots.
Crecimiento real: contenido de valor que la gente comparte porque le ayuda.
Todo el contenido apunta a llevar trafico a la comunidad Skool."""


class Viral:
    def __init__(self) -> None:
        self.system_prompt = _SYSTEM

    def crear_calendario(self, comunidad: str, mes: str, posts_semana: int = 5) -> str:
        log.info(f"Calendario {mes}: {comunidad[:40]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea el calendario editorial de {mes} para la comunidad '{comunidad}'.\n"
                f"Frecuencia: {posts_semana} posts/semana por plataforma.\n"
                f"Plataformas: Instagram, TikTok, LinkedIn.\n\n"
                f"Para cada post incluye: dia, plataforma, tipo de contenido, "
                f"idea del post, caption (completo), hashtags, CTA hacia Skool.\n"
                f"Mix de contenido: 40% educativo, 30% motivacional, 20% detras de camaras, 10% venta.\n"
                f"Guarda en output/skool/redes/calendario_{mes.replace(' ','-')}.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=10,
            terminal_tools=frozenset(),
        )

    def crear_estrategia(self, comunidad: str, objetivo: str) -> str:
        log.info(f"Estrategia redes: {comunidad[:40]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea la estrategia de redes sociales para '{comunidad}'.\n"
                f"Objetivo: {objetivo}\n\n"
                f"Incluye: perfil ideal del seguidor, tono y voz, pilares de contenido (5), "
                f"estrategia de hashtags por plataforma, horarios optimos de publicacion, "
                f"como convertir seguidores en miembros Skool, metricas clave a seguir.\n"
                f"Guarda en output/skool/redes/estrategia.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=8,
            terminal_tools=frozenset(),
        )

    def crear_bio_perfiles(self, comunidad: str, propuesta: str) -> str:
        log.info(f"Bios: {comunidad[:40]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Escribe las bios optimizadas para todos los perfiles de '{comunidad}':\n"
                f"Propuesta de valor: {propuesta}\n\n"
                f"Entrega bio para: Instagram (150 chars), TikTok (80 chars), "
                f"LinkedIn (220 chars), Skool (sin limite).\n"
                f"Cada bio debe incluir: quien eres, para quien, que obtienes, CTA con link.\n"
                f"Guarda en output/skool/redes/bios.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=6,
            terminal_tools=frozenset(),
        )

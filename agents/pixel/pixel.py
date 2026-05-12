"""Pixel — Diseñador Digital.

Genera:
- Identidad visual completa (colores, tipografia, estilo)
- Briefs detallados para Canva (con medidas, colores, copy exacto)
- Banners y thumbnails en HTML/CSS (previsualización)
- Guia de marca para toda la comunidad
"""
from __future__ import annotations

from shared.agent_runner import ejecutar_agente
from shared.herramientas import TOOLS_DOMENECH
from shared.logger import log_de

_AGENTE = "pixel"
log = log_de(_AGENTE)

_SYSTEM = """Eres Pixel, diseñador digital especializado en identidad visual para comunidades online.
Hablas en castellano. Practico y visual.

Generas: briefs de diseño detallados, guias de marca, mockups HTML/CSS, instrucciones exactas para Canva.
Cuando hagas un brief para Canva, especifica: medidas exactas, colores hex, fuentes, textos, disposicion.
Cuando hagas HTML/CSS: codigo real y completo, visualmente atractivo."""


class Pixel:
    def __init__(self) -> None:
        self.system_prompt = _SYSTEM

    def crear_identidad_visual(self, brief: str) -> str:
        log.info(f"Identidad visual: {brief[:60]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea la identidad visual completa para:\n{brief}\n\n"
                f"Entrega:\n"
                f"1. Paleta de colores (5 colores con hex)\n"
                f"2. Tipografia (fuentes de Google Fonts, uso de cada una)\n"
                f"3. Estilo visual (referencias, mood, que transmite)\n"
                f"4. Brief Canva para: banner Skool (1920x384px), thumbnail post (1200x675px), "
                f"foto de perfil comunidad (400x400px)\n"
                f"5. Mockup HTML del banner principal\n"
                f"Guarda todo en output/skool/identidad/"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=12,
            terminal_tools=frozenset(),
        )

    def crear_plantillas_canva(self, tipo: str, specs: str) -> str:
        log.info(f"Plantillas Canva: {tipo!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Crea briefs detallados para plantillas Canva de tipo: {tipo}\n"
                f"Specs adicionales: {specs}\n\n"
                f"Para cada plantilla incluye: medidas, fondo, colores exactos (hex), "
                f"posicion y estilo del texto, elementos graficos, variantes.\n"
                f"Guarda en output/skool/identidad/plantillas_{tipo}.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=8,
            terminal_tools=frozenset(),
        )

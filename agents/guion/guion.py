"""Guion — Copywriter y Guionista.

Genera:
- Scripts de video (YouTube, Reels, TikTok)
- Posts escritos para Skool
- Hooks y titulares
- Emails de la newsletter
- Descripciones de cursos y modulos
"""
from __future__ import annotations

from shared.agent_runner import ejecutar_agente
from shared.herramientas import TOOLS_DOMENECH
from shared.logger import log_de

_AGENTE = "guion"
log = log_de(_AGENTE)

_SYSTEM = """Eres Guion, copywriter y guionista especializado en contenido para autónomos españoles.
Hablas en castellano. Tono: directo, sin relleno, cercano pero profesional.

Escribes para personas ocupadas que no tienen tiempo para rollos. Cada palabra cuenta.
Especialidad: hooks que enganchen en los primeros 3 segundos, CTAs que conviertan,
contenido educativo que sea accionable."""


class Guion:
    def __init__(self) -> None:
        self.system_prompt = _SYSTEM

    def crear_script_video(self, tema: str, formato: str = "youtube", duracion: str = "5-7min") -> str:
        log.info(f"Script {formato}: {tema[:60]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Escribe un script completo de {formato} ({duracion}) sobre: {tema}\n\n"
                f"Estructura: hook (0-15s) + problema (15-60s) + solucion + desarrollo "
                f"+ CTA final.\n"
                f"Incluye: indicaciones de camara [entre corchetes], transiciones, "
                f"texto en pantalla sugerido.\n"
                f"Guarda en output/skool/contenido/script_{formato}_{tema[:30].replace(' ','-')}.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=8,
            terminal_tools=frozenset(),
        )

    def crear_hooks(self, tema: str, n: int = 10) -> str:
        log.info(f"Hooks para: {tema[:60]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Genera {n} hooks de alto impacto para contenido sobre: {tema}\n"
                f"Formatos: 3 para Reels/TikTok (max 10 palabras), "
                f"3 para titulares YouTube, "
                f"2 para asuntos de email, "
                f"2 para titulares de post Skool.\n"
                f"Guarda en output/skool/contenido/hooks_{tema[:30].replace(' ','-')}.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=6,
            terminal_tools=frozenset(),
        )

    def crear_descripcion_curso(self, nombre: str, contenido: str) -> str:
        log.info(f"Descripcion curso: {nombre!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Escribe la descripcion de venta del curso '{nombre}'.\n"
                f"Contenido del curso: {contenido}\n\n"
                f"Incluye: titular, subtitular, para quien es, que aprenderas (bullets), "
                f"por que ahora, precio sugerido, garantia, CTA.\n"
                f"Guarda en output/skool/contenido/curso_{nombre[:30].replace(' ','-')}.md"
            ),
            tools=TOOLS_DOMENECH,
            max_iter=8,
            terminal_tools=frozenset(),
        )

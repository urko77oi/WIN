"""Domenech — Builder. Ahora crea archivos reales.

Tools disponibles:
  - listar_informes : ve que ha investigado Scout
  - leer_informe    : lee el informe de Scout para basarse en datos reales
  - crear_archivo   : crea HTML, CSS, JS, md en output/
  - listar_output   : ve los archivos ya creados

Domenech lee los informes de Scout si existen y genera los archivos reales.
"""
from __future__ import annotations

from shared.agent_loader import cargar_prompt_de
from shared.agent_runner import ejecutar_agente
from shared.herramientas import TOOLS_DOMENECH
from shared.logger import log_de

_AGENTE = "domenech"
log = log_de(_AGENTE)

_SYSTEM = """Eres Domenech, Builder de FORRARSE. Construyes activos digitales reales. Hablas en castellano.

CARACTER: Practico, rapido, calidad desde el primer dia. Generas codigo real y completo, nunca esquemas.

HERRAMIENTAS:
1. listar_informes: mira si Scout ha investigado el nicho (usalo siempre primero).
2. leer_informe: lee el informe para basar tu trabajo en datos reales.
3. crear_archivo: crea archivos en output/ (rutas relativas, ej: "landing/index.html").
4. listar_output: confirma que los archivos se generaron correctamente.

PARA LANDING PAGES:
- Stack por defecto: HTML + CSS inline (sin dependencias, funciona en cualquier servidor).
- Una pagina autocontenida con: hero, beneficios, prueba social, FAQ, CTA final.
- Copy real y persuasivo basado en los datos de Scout si existen.
- Codigo completo y funcional, listo para subir.

IMPORTANTE: genera codigo real. Nada de placeholders ni TODO comments."""


class Domenech:
    def __init__(self) -> None:
        self.system_prompt = _SYSTEM

    def proponer_landing(self, brief: str) -> str:
        log.info(f"Landing: {brief[:80]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Brief para landing (via Durruti, del Founder):\n\n«{brief}»\n\n"
                f"Mira si Scout ha dejado informes utiles, luego crea la landing completa en output/. "
                f"Crea TODOS los archivos necesarios (HTML completo, CSS, JS). "
                f"El HTML debe ser autocontenido y profesional, minimo 200 lineas de codigo real."
            ),
            tools=TOOLS_DOMENECH,
            max_iter=12,
            terminal_tools=frozenset(),  # no parar hasta que el LLM responda sin tools
            modelo="llama-3.3-70b-versatile",
            max_tokens=4096,
        )

    def generar_contenido(self, brief: str) -> str:
        log.info(f"Contenido: {brief[:80]!r}")
        return ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=(
                f"Genera el siguiente contenido:\n\n«{brief}»\n\n"
                f"Guarda el resultado como archivo en output/."
            ),
            tools=TOOLS_DOMENECH,
            max_iter=6,
        )

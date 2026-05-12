"""Durruti — CEO Operativo. Orquesta con resultados reales.

Ahora usa Groq directamente para la conversacion libre y delega trabajo
real a Scout y Domenech (que tienen tools de verdad).
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from agents.domenech.domenech import Domenech
from agents.emma.emma import Emma
from agents.guion.guion import Guion
from agents.pixel.pixel import Pixel
from agents.scout.scout import Scout
from agents.viral.viral import Viral
from shared import memory
from shared.agent_loader import cargar_prompt_de
from shared.agent_runner import ejecutar_agente
from shared.herramientas import TOOLS_DURRUTI
from shared.human_channel import HumanChannel, canal_por_defecto
from shared.logger import log_de

_AGENTE = "durruti"
log = log_de(_AGENTE)

_SYSTEM = """Eres Durruti, CEO Operativo de FORRARSE. Hablas en castellano.

CARACTER: Directo, inteligente, con criterio propio. Tuteas al Founder. Humor seco ocasional.

HERRAMIENTAS para status y coordinacion:
- listar_informes: ve los informes que Scout ha guardado.
- leer_informe: lee un informe concreto.
- listar_tareas: ve las tareas pendientes.
- guardar_tarea: guarda una tarea para el equipo.
- listar_output: ve los archivos que Domenech ha creado.

REGLAS: maximo 3-4 frases en conversacion libre. Sin markdown en respuestas de voz. Directo al grano."""


@dataclass
class Resultado:
    texto_para_humano: str
    proyecto_slug: str | None = None


def _clasificar(orden: str) -> str:
    o = orden.lower()
    if any(k in o for k in ("investiga", "analiza", "nicho", "mercado", "competenci", "audita")):
        return "investigar"
    if any(k in o for k in ("crea landing", "haz landing", "monta landing", "landing", "web", "pagina")):
        return "landing"
    if any(k in o for k in ("escribe", "genera contenido", "post", "email", "copy", "hilo")):
        return "contenido"
    if any(k in o for k in ("status", "estado", "como va", "que han hecho", "que trabajo")):
        return "status"
    return "libre"


class Durruti:
    def __init__(self, canal: HumanChannel | None = None) -> None:
        self.canal = canal or canal_por_defecto()
        self.system_prompt = _SYSTEM
        self.scout    = Scout()
        self.domenech = Domenech()
        self.emma     = Emma()
        self.pixel    = Pixel()
        self.guion    = Guion()
        self.viral    = Viral()
        log.info("Durruti listo. Canal: " + self.canal.__class__.__name__)

    def procesar(self, orden: str) -> Resultado:
        log.info(f"Orden: {orden!r}")
        tipo = _clasificar(orden)
        log.info(f"Tipo: {tipo}")

        if tipo == "investigar":
            return self._investigar(orden)
        if tipo == "landing":
            return self._landing(orden)
        if tipo == "contenido":
            return self._contenido(orden)
        if tipo == "status":
            return self._status(orden)
        return self._libre(orden)

    def _investigar(self, orden: str) -> Resultado:
        proyecto = memory.crear_proyecto(nombre=f"Investigacion: {orden[:60]}", descripcion=orden)
        memory.anotar_en_bitacora(proyecto.slug, "Scout investiga con herramientas reales.")
        self.canal.notificar("Scout esta investigando... (puede tardar 1-2 min)")
        informe = self.scout.investigar(orden)
        memory.anotar_en_bitacora(proyecto.slug, "Scout entrego informe.")
        self.canal.notificar(informe)
        return Resultado(texto_para_humano=informe, proyecto_slug=proyecto.slug)

    def _landing(self, orden: str) -> Resultado:
        proyecto = memory.crear_proyecto(nombre=f"Landing: {orden[:60]}", descripcion=orden)
        self.canal.notificar("Domenech esta construyendo la landing... (puede tardar 1-2 min)")
        resultado = self.domenech.proponer_landing(orden)
        memory.anotar_en_bitacora(proyecto.slug, "Domenech genero archivos en output/.")
        self.canal.notificar(resultado)
        return Resultado(texto_para_humano=resultado, proyecto_slug=proyecto.slug)

    def _contenido(self, orden: str) -> Resultado:
        self.canal.notificar("Domenech generando contenido...")
        resultado = self.domenech.generar_contenido(orden)
        self.canal.notificar(resultado)
        return Resultado(texto_para_humano=resultado)

    def _status(self, orden: str) -> Resultado:
        texto = ejecutar_agente(
            nombre=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje=f"El Founder pregunta: «{orden}». Usa tus herramientas para dar un status real del equipo.",
            tools=TOOLS_DURRUTI,
            max_iter=4,
        )
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto)

    def _libre(self, orden: str) -> Resultado:
        """Conversacion libre — sin tools, respuesta directa."""
        modo = os.getenv("LLM_MODE", "mock").strip().lower()
        if modo != "real":
            texto = (
                "[MOCK · Durruti] Entendido. "
                "Activa LLM_MODE=real con creditos Anthropic para conversacion real."
            )
            self.canal.notificar(texto)
            return Resultado(texto_para_humano=texto)

        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=self.system_prompt,
            messages=[{"role": "user", "content": orden}],
        )
        texto = resp.content[0].text.strip()
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto)

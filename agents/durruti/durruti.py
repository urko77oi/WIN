"""Implementación de Durruti, el CEO Operativo.

Único interlocutor con el humano. Recibe órdenes, las clasifica, delega en
Researcher o Builder, supervisa, pide aprobaciones y reporta.

En Fase 0 esta clase orquesta el flujo end-to-end con respuestas mock.
En Fase 1+ se ampliará con: telegram, parsing de órdenes más rico,
catálogo dinámico, etc.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agents.builder.builder import Builder
from agents.researcher.researcher import Researcher
from shared import llm_client, memory
from shared.human_channel import HumanChannel, canal_por_defecto
from shared.logger import PROJECT_ROOT, log_de


_AGENTE = "durruti"
log = log_de(_AGENTE)

PROMPT_PATH: Path = PROJECT_ROOT / "agents" / "durruti" / "system_prompt.md"


@dataclass
class Resultado:
    """Resultado consolidado que Durruti devuelve tras procesar una orden."""
    texto_para_humano: str
    proyecto_slug: str | None = None


def _cargar_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _clasificar_orden(orden: str) -> str:
    """Clasificación heurística simple por palabras clave.

    En Fase 1+ esto lo hará el LLM. En Fase 0 nos basta con keywords para
    que el flujo sea predecible y barato.
    """
    o = orden.lower()
    if any(k in o for k in ("investiga", "research", "analiza", "estudia", "competencia", "nicho", "palabras clave")):
        return "investigar_nicho"
    if any(k in o for k in ("crea landing", "haz landing", "monta landing", "web", "landing")):
        return "crear_landing"
    if any(k in o for k in ("escribe", "genera contenido", "post", "hilo", "email", "copy")):
        return "generar_contenido"
    if "status" in o or "estado" in o or "como vas" in o:
        return "status"
    if "crea proyecto" in o or "nuevo proyecto" in o:
        return "crear_proyecto"
    return "desconocida"


class Durruti:
    """CEO Operativo. Punto de entrada del sistema."""

    def __init__(self, canal: HumanChannel | None = None) -> None:
        self.canal = canal or canal_por_defecto()
        self.system_prompt = _cargar_system_prompt()
        self.researcher = Researcher()
        self.builder = Builder()
        log.info("Durruti listo. Canal: " + self.canal.__class__.__name__)

    # ─────────────────────────────────────────────────────────────────
    # API pública
    # ─────────────────────────────────────────────────────────────────

    def procesar(self, orden: str) -> Resultado:
        """Procesa una orden del humano de principio a fin.

        Retorna `Resultado`. El texto ya ha sido también enviado al canal humano.
        """
        log.info(f"Orden recibida: {orden!r}")
        tipo = _clasificar_orden(orden)
        log.info(f"Tipo clasificado: {tipo}")

        if tipo == "status":
            return self._handle_status()
        if tipo == "investigar_nicho":
            return self._handle_investigar(orden)
        if tipo == "crear_landing":
            return self._handle_crear_landing(orden)
        if tipo == "generar_contenido":
            return self._handle_generar_contenido(orden)
        if tipo == "crear_proyecto":
            return self._handle_crear_proyecto(orden)
        return self._handle_desconocida(orden)

    # ─────────────────────────────────────────────────────────────────
    # Handlers
    # ─────────────────────────────────────────────────────────────────

    def _handle_status(self) -> Resultado:
        from shared import cost_tracker

        proyectos = memory.listar_proyectos()
        coste_dia = cost_tracker.coste_acumulado("dia")
        coste_mes = cost_tracker.coste_acumulado("mes")
        modo = llm_client.modo_actual()

        lineas = [
            f"**Modo LLM:** `{modo}`",
            f"**Proyectos activos:** {len(proyectos)}",
        ]
        for p in proyectos[:10]:
            lineas.append(f"- `{p.slug}` — {p.nombre} (act: {p.actualizado[:10]})")
        lineas.append("")
        lineas.append(f"**Coste API hoy:** {coste_dia:.4f} €")
        lineas.append(f"**Coste API mes:** {coste_mes:.4f} €")

        texto = "\n".join(lineas)
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto)

    def _handle_investigar(self, orden: str) -> Resultado:
        proyecto = memory.crear_proyecto(
            nombre=f"Investigación: {orden[:60]}",
            descripcion=orden,
        )
        memory.anotar_en_bitacora(proyecto.slug, f"Durruti delega investigación a Researcher.")
        informe = self.researcher.investigar(orden)
        memory.anotar_en_bitacora(proyecto.slug, "Researcher entrega informe.")

        texto = self._llamar_consolidacion(
            orden=orden,
            entrega_de_especialista=informe,
            tipo_entrega="informe del Researcher",
        )
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto, proyecto_slug=proyecto.slug)

    def _handle_crear_landing(self, orden: str) -> Resultado:
        proyecto = memory.crear_proyecto(
            nombre=f"Landing: {orden[:60]}",
            descripcion=orden,
        )
        memory.anotar_en_bitacora(proyecto.slug, "Durruti delega creación de landing en Builder.")
        propuesta = self.builder.proponer_landing(orden)
        memory.anotar_en_bitacora(proyecto.slug, "Builder entrega propuesta de landing.")

        texto = self._llamar_consolidacion(
            orden=orden,
            entrega_de_especialista=propuesta,
            tipo_entrega="propuesta de landing del Builder",
        )
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto, proyecto_slug=proyecto.slug)

    def _handle_generar_contenido(self, orden: str) -> Resultado:
        propuesta = self.builder.generar_contenido(orden)
        texto = self._llamar_consolidacion(
            orden=orden,
            entrega_de_especialista=propuesta,
            tipo_entrega="contenido generado por Builder",
        )
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto)

    def _handle_crear_proyecto(self, orden: str) -> Resultado:
        nombre = orden.replace("crea proyecto", "").replace("nuevo proyecto", "").strip(": -")
        if not nombre:
            nombre = "Sin nombre"
        proyecto = memory.crear_proyecto(nombre=nombre, descripcion=orden)
        texto = (
            f"Proyecto **{proyecto.nombre}** creado.\n"
            f"- Slug: `{proyecto.slug}`\n"
            f"- Archivo: `{proyecto.archivo_md.relative_to(PROJECT_ROOT)}`"
        )
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto, proyecto_slug=proyecto.slug)

    def _handle_desconocida(self, orden: str) -> Resultado:
        texto = (
            "No tengo una orden-tipo que encaje exactamente con tu mensaje.\n\n"
            "Catálogo actual: investigar_nicho, crear_landing, generar_contenido, "
            "crear_proyecto, status.\n\n"
            f"Tu mensaje: «{orden[:200]}»\n\n"
            "¿Lo reformulas o quieres que lo trate como una conversación libre con Durruti?"
        )
        self.canal.notificar(texto)
        return Resultado(texto_para_humano=texto)

    # ─────────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────────

    def _llamar_consolidacion(
        self,
        *,
        orden: str,
        entrega_de_especialista: str,
        tipo_entrega: str,
    ) -> str:
        """Pide al LLM (en modo del agente Durruti) que consolide la entrega.

        En modo mock devuelve respuesta plantilla coherente.
        """
        mensaje = (
            f"Orden del humano: «{orden}»\n\n"
            f"He recibido la siguiente {tipo_entrega}:\n\n"
            f"---\n{entrega_de_especialista}\n---\n\n"
            f"Consolida la respuesta para el humano siguiendo tu patrón "
            f"(Qué hice / Qué encontré / Qué propongo / Qué necesito)."
        )
        resp = llm_client.llamar(
            agente=_AGENTE,
            system_prompt=self.system_prompt,
            mensaje_usuario=mensaje,
            orden=orden[:120],
        )
        return resp.texto

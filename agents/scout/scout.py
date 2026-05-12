"""Scout — Analista de Oportunidades.

Arquitectura eficiente:
  FASE 1: recoleccion (Python puro, sin LLM) — busquedas + lectura de paginas
  FASE 2: sintesis (una sola llamada Anthropic) — analiza todo el contexto compacto

LLM_MODE=mock  → sintesis simulada, sin creditos
LLM_MODE=real  → Claude Haiku (rapido y barato)
"""
from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from shared.herramientas import buscar_web, guardar_informe, leer_pagina
from shared.logger import PROJECT_ROOT, log_de

load_dotenv(PROJECT_ROOT / ".env")
log = log_de("scout")

_MODELO = "claude-haiku-4-5-20251001"

_SYSTEM = """Eres Scout, analista de oportunidades de negocio online. Hablas en castellano.
Analitico, preciso, basas TODO en los datos que te dan. No inventas. Directo al grano.
Formato de salida: markdown estructurado, datos reales, sin relleno."""


class Scout:
    def __init__(self) -> None:
        self._modo = os.getenv("LLM_MODE", "mock").strip().lower()
        if self._modo == "real":
            from anthropic import Anthropic
            self._client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            self._client = None

    # ── API publica ────────────────────────────────────────────────────

    def investigar(self, brief: str) -> str:
        log.info(f"Investigando: {brief[:80]!r}")
        contexto = self._recolectar(brief)
        resultado = self._sintetizar(brief, contexto)
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        slug = brief[:40].lower().replace(" ", "-").replace("/", "")
        nombre = f"{ts}_{slug}.md"
        guardar_informe(nombre, resultado)
        log.info(f"Informe guardado: {nombre}")
        return resultado

    def auditar_competidor(self, competidor: str) -> str:
        log.info(f"Auditando: {competidor!r}")
        queries = [
            f"{competidor} precios planes",
            f"{competidor} opiniones resenas",
            f"{competidor} alternativas competidores",
        ]
        fragmentos = self._buscar_multiples(queries, paginas_por_query=2)
        return self._sintetizar(
            f"Audita el competidor: {competidor}",
            fragmentos,
            instruccion="Analiza: propuesta de valor, precios, fortalezas, debilidades, gaps explotables.",
        )

    # ── Recoleccion (Python puro, sin LLM) ────────────────────────────

    def _recolectar(self, brief: str, n_queries: int = 5) -> str:
        temas = self._extraer_temas(brief)
        return self._buscar_multiples(temas[:n_queries], paginas_por_query=2)

    def _extraer_temas(self, brief: str) -> list[str]:
        """Genera queries de busqueda especificos a partir del brief. Sin LLM."""
        nucleo = next(
            (l.strip() for l in brief.splitlines() if l.strip() and not l.startswith("#")),
            brief[:80].strip(),
        )[:60]

        brief_lower = brief.lower()
        if any(k in brief_lower for k in ("negocio", "oportunidad", "monetiz", "ingreso", "mercado")):
            return [
                "negocios online sin inversion mercado hispanohablante 2025 2026",
                "servicios digitales espanol no existen version inglesa oportunidad nicho",
                "quejas autonomos freelancers espana problemas sin resolver herramientas",
                "nichos contenido youtube instagram espanol poca competencia alta demanda 2025",
                "herramientas SaaS B2B pymes espanolas carencias digitales necesidades",
                "modelos negocio suscripcion recurrente ticket bajo espanol latam",
                "colectivos desatendidos online seniors autonomos profesionales espana 2025",
                "arbitraje digital comprar barato revender valor anadido online espana",
                "idea negocio servicio bajo demanda espana latinoamerica ganar dinero rapido",
                "tendencias emprendimiento digital 2025 espana latam mercado en crecimiento",
            ]

        return [
            f"{nucleo} mercado oportunidad 2025",
            f"{nucleo} competidores principales espana",
            f"{nucleo} monetizacion modelos de negocio",
            f"{nucleo} tendencias 2025 2026",
            f"{nucleo} problemas clientes dolor punto",
            f"{nucleo} precio ticket modelo suscripcion",
        ]

    # Dominios que nunca aportan contexto de negocio útil
    _IGNORAR = {
        "rae.es", "leroymerlin.es", "wikipedia.org", "wikihow.com",
        "ayuntamiento.es", "gva.es", "boe.es", "mapa.gob.es",
        "sedipualba.es", "raspeig.es", "conjugador.reverso.net",
        "buscapalabra.com", "okdiario.com", "wallapop.com",
        "totherramienta.com", "trendmodels.es", "marie-claire.es",
        "modelmanagement.com", "modelos.net", "youtube.com",
    }

    def _url_ignorada(self, url: str) -> bool:
        return any(d in url for d in self._IGNORAR)

    def _buscar_multiples(self, queries: list[str], paginas_por_query: int = 2) -> str:
        fragmentos: list[str] = []
        urls_vistas: set[str] = set()

        for query in queries:
            log.info(f"[buscar] {query!r}")
            resultados_raw = buscar_web(query, max_results=6)
            fragmentos.append(f"**Busqueda:** {query}\n{resultados_raw[:600]}")
            time.sleep(0.3)

            leidas = 0
            for bloque in resultados_raw.split("###")[1:]:
                if leidas >= paginas_por_query:
                    break
                lineas = bloque.strip().split("\n")
                url = next((l for l in lineas if l.startswith("http")), None)
                if not url or url in urls_vistas or self._url_ignorada(url):
                    continue
                urls_vistas.add(url)
                contenido = leer_pagina(url)
                if not contenido.startswith("Error"):
                    fragmentos.append(f"**Pagina:** {url}\n{contenido[:800]}")
                    leidas += 1
                time.sleep(0.2)

        return "\n\n---\n\n".join(fragmentos)

    # ── Sintesis ──────────────────────────────────────────────────────

    def _sintetizar(self, brief: str, contexto: str,
                    instruccion: str | None = None) -> str:
        """Una llamada LLM con contexto compacto."""
        instr = instruccion or (
            "Genera un informe con 10 propuestas de negocio online viables con inversion cero. "
            "Para cada una: nombre, descripcion de 2 lineas, modelo de monetizacion, "
            "tiempo hasta primer ingreso, nivel de competencia (bajo/medio/alto), "
            "por que es viable ahora."
        )
        mensaje = (
            f"Brief: {brief}\n\n"
            f"Datos recopilados de internet:\n{contexto[:3000]}\n\n"
            f"Instruccion: {instr}"
        )

        if self._modo != "real" or self._client is None:
            return (
                "[MOCK · Scout] Sintesis simulada. "
                "Activa LLM_MODE=real con creditos Anthropic para analisis real.\n\n"
                f"Brief recibido: {brief[:200]}"
            )

        resp = self._client.messages.create(
            model=_MODELO,
            max_tokens=1500,
            system=_SYSTEM,
            messages=[{"role": "user", "content": mensaje}],
        )
        return resp.content[0].text.strip()

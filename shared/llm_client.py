"""Cliente unificado para llamar al modelo (LLM).

Tiene dos modos, controlados por la variable de entorno `LLM_MODE`:

  - `mock`: respuestas simuladas, deterministas, coste 0. Ideal para Fase 0
    y para depurar la orquestación sin gastar dinero.
  - `real`: llamadas reales a la API de Anthropic. Requiere
    `ANTHROPIC_API_KEY` y créditos en console.anthropic.com.

Cada llamada se registra en `cost_tracker` para auditoría y métricas.

Quien lo usa: cualquier agente que necesite hablar con un modelo.
"""
from __future__ import annotations

import hashlib
import os
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from dotenv import load_dotenv

from shared import cost_tracker
from shared.logger import PROJECT_ROOT, log_de

# Cargar .env de la raíz del proyecto si existe.
load_dotenv(PROJECT_ROOT / ".env")

log = log_de("llm")

LLMMode = Literal["mock", "real"]


@dataclass(frozen=True)
class LLMResponse:
    """Respuesta de una llamada al modelo."""
    texto: str
    modelo: str
    tokens_input: int
    tokens_output: int
    coste_eur: float
    modo: LLMMode


def _modo_actual() -> LLMMode:
    modo = os.environ.get("LLM_MODE", "").strip().lower()
    if modo in ("mock", "real"):
        return modo  # type: ignore[return-value]
    # Si no hay env, leemos del settings.
    cfg_path = PROJECT_ROOT / "config" / "settings.yaml"
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        m = ((data.get("llm") or {}).get("mode_default") or "mock").lower()
        if m in ("mock", "real"):
            return m  # type: ignore[return-value]
    return "mock"


def _modelo_para_agente(agente: str) -> str:
    """Devuelve el modelo asignado a un agente desde config/models.yaml."""
    cfg_path = PROJECT_ROOT / "config" / "models.yaml"
    if not cfg_path.exists():
        return "haiku-4-5"
    with cfg_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if _modo_actual() == "mock":
        return ((data.get("modo_mock") or {}).get("modelo_simulado") or "mock")
    return ((data.get("defaults") or {}).get(agente) or "haiku-4-5")


# Mapeo de nuestros nombres internos al ID real de la API.
_MODEL_ID_REAL: dict[str, str] = {
    "haiku-4-5": "claude-haiku-4-5-20251001",
    "sonnet-4-6": "claude-sonnet-4-6",
    "opus-4-7": "claude-opus-4-7",
}


# ─────────────────────────────────────────────────────────────────────
# Modo MOCK
# ─────────────────────────────────────────────────────────────────────

def _generar_mock(*, agente: str, system_prompt: str, mensaje_usuario: str) -> str:
    """Devuelve una respuesta determinista basada en el agente y el mensaje.

    Es una falsa pero plausible respuesta. Útil para validar la orquestación
    sin gastar nada. Nunca se debe usar en producción.
    """
    semilla = hashlib.sha1(f"{agente}|{mensaje_usuario}".encode("utf-8")).hexdigest()[:8]

    plantillas = {
        "durruti": textwrap.dedent(f"""
            [MOCK · {semilla}] He recibido tu orden: «{mensaje_usuario.strip()[:120]}».

            Plan que voy a seguir:
            1. Identificar de qué tipo de tarea se trata.
            2. Decidir qué especialista es el adecuado (Researcher / Builder).
            3. Delegar y supervisar.
            4. Consolidar la respuesta y pedir aprobación si toca.

            (Respuesta simulada en modo mock. Para respuestas reales,
            mete créditos en console.anthropic.com y pon LLM_MODE=real en .env.)
        """).strip(),

        "researcher": textwrap.dedent(f"""
            [MOCK · {semilla}] Investigación simulada sobre: «{mensaje_usuario.strip()[:120]}».

            Hallazgos (simulados):
            - Tamaño de mercado: medio, en crecimiento.
            - Competencia: 3-5 actores establecidos, espacio para nicho diferenciado.
            - Palabras clave principales: [palabra1, palabra2, palabra3].
            - Ángulo recomendado: enfoque en un sub-nicho específico con dolor real.

            Próximo paso sugerido: pasar el brief al Builder para una landing
            con copy orientado al ángulo identificado.
        """).strip(),

        "builder": textwrap.dedent(f"""
            [MOCK · {semilla}] Propuesta del Builder para: «{mensaje_usuario.strip()[:120]}».

            Estructura propuesta:
            - Hero con headline directo + sub-headline + CTA.
            - 3 bloques de beneficios con iconos.
            - Sección de prueba social (testimonios o logos).
            - FAQ corta (3-5 preguntas).
            - CTA final.

            Stack: HTML + CSS + Tailwind (sin JS innecesario).
            Hosting recomendado: Cloudflare Pages (gratis).

            Listo para crear archivos cuando me des luz verde.
        """).strip(),
    }

    return plantillas.get(
        agente,
        f"[MOCK · {semilla}] Respuesta simulada del agente {agente!r}.",
    )


# ─────────────────────────────────────────────────────────────────────
# Modo REAL
# ─────────────────────────────────────────────────────────────────────

def _llamar_real(
    *,
    agente: str,
    modelo_interno: str,
    system_prompt: str,
    mensaje_usuario: str,
) -> tuple[str, int, int]:
    """Llamada real a la API de Anthropic. Devuelve (texto, tokens_in, tokens_out)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "LLM_MODE=real pero falta ANTHROPIC_API_KEY en .env. "
            "Cambia a LLM_MODE=mock o consigue una key en console.anthropic.com."
        )

    if cost_tracker.excede_limite_diario():
        raise RuntimeError(
            "Límite diario de gasto superado. Sistema en pausa. "
            "Edita config/budget.yaml o espera a mañana."
        )

    # Import diferido para que el modo mock no requiera tener anthropic instalado.
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    model_id = _MODEL_ID_REAL.get(modelo_interno, modelo_interno)

    log.info(f"Llamada real a {model_id} (agente={agente})")
    resp = client.messages.create(
        model=model_id,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": mensaje_usuario}],
    )
    texto = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    return (texto, resp.usage.input_tokens, resp.usage.output_tokens)


# ─────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────

def llamar(
    *,
    agente: str,
    system_prompt: str,
    mensaje_usuario: str,
    orden: str | None = None,
) -> LLMResponse:
    """Llama al modelo. Punto de entrada único para todos los agentes.

    Ramifica entre mock y real según `LLM_MODE`. Registra coste en SQLite.
    """
    modo = _modo_actual()
    modelo = _modelo_para_agente(agente)

    if modo == "mock":
        texto = _generar_mock(
            agente=agente,
            system_prompt=system_prompt,
            mensaje_usuario=mensaje_usuario,
        )
        # Tokens simulados: aproximación grosera para que el tracker tenga datos.
        tokens_in = len(system_prompt) // 4 + len(mensaje_usuario) // 4
        tokens_out = len(texto) // 4
    else:
        texto, tokens_in, tokens_out = _llamar_real(
            agente=agente,
            modelo_interno=modelo,
            system_prompt=system_prompt,
            mensaje_usuario=mensaje_usuario,
        )

    coste = cost_tracker.registrar(
        agente=agente,
        modelo=modelo,
        tokens_input=tokens_in,
        tokens_output=tokens_out,
        orden=orden,
        nota=f"modo={modo}",
    )

    return LLMResponse(
        texto=texto,
        modelo=modelo,
        tokens_input=tokens_in,
        tokens_output=tokens_out,
        coste_eur=coste,
        modo=modo,
    )


def modo_actual() -> LLMMode:
    """Expone el modo actual (útil para banners y diagnóstico)."""
    return _modo_actual()

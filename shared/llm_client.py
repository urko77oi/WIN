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
    defaults = data.get("defaults") or {}
    if agente in defaults:
        return defaults[agente]
    # Compatibilidad: si Scout no está en defaults, usa el del Researcher.
    return "haiku-4-5"


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

        "scout": textwrap.dedent(f"""
            [MOCK · {semilla}]

            ## TL;DR
            Oportunidad simulada sobre «{mensaje_usuario.strip()[:120]}».
            Veredicto: **validar con landing test**. Mejor perfil: ⚖️ Equilibrado.
            Score primario: 7.4/10 · Confianza 🟡.

            ## Triple scoring
            - 🛡️ Conservador: 6.8/10 — Validar — 🟡
            - ⚖️ Equilibrado: 7.4/10 — Validar — 🟡
            - 🔥 Agresivo: 7.9/10 — Sprint validación 14 días — 🟡

            ## Hallazgos clave
            - Tamaño de mercado: medio, en crecimiento ~+25% YoY (simulado).
            - Competencia: 3-5 actores establecidos; ningún dominador en nicho hispano.
            - Pain points repetidos en comunidades: precio, accesibilidad, idioma.
            - Saturación SEO: keywords core con KD medio; long-tail abierto.

            ## Riesgos y dudas
            - Datos de CAC/LTV son aproximaciones; falta validación real.
            - No hay benchmarks públicos del sub-segmento exacto.

            ## Recomendación
            Landing test 14 días con 80€ de ads. Métrica de éxito definida
            ANTES del test (ej: opt-in rate ≥ 3%). Si falla, pivotar al
            sub-nicho B2B o cambiar ángulo.

            ## Fuentes
            1. [MOCK] Datos simulados — modo Fase 0. Para fuentes reales,
               activar tools externas (Brave/Reddit/Trends) en Fase 1+.
        """).strip(),


        "domenech": textwrap.dedent(f"""
            [MOCK · {semilla}] Propuesta de Domenech (Builder).

            ## ADR de stack
            - Frontend: **Astro** (mejor Lighthouse out-of-the-box, contenido mayoritariamente estático).
            - Hosting: **Cloudflare Pages** (free tier, edge global).
            - Email: **Resend** (form de captura).
            - Pagos: ninguno en este hito.
            - Justificación: minimiza JS, coste 0/mes, deploy en minutos.

            ## Estructura propuesta
            - Hero con headline directo + sub-headline + CTA.
            - 3 bloques de beneficios con iconos.
            - Sección de prueba social.
            - FAQ corta (3-5 preguntas).
            - CTA final.
            - Páginas legales mínimas (privacidad, términos).

            ## Hitos (Playbook 1 abreviado)
            - Hito 1 — Identidad (60 min, ~0,30€): moodboard + tokens.
            - Hito 2 — Build (180 min, ~0,40€): Astro + Tailwind + form Resend.
            - Hito 3 — Verificación (30 min, ~0,05€): Lighthouse mobile ≥ 90.
            - Hito 4 — Aprobación de publicación (humano).
            - Hito 5 — Producción + uptime monitor.
            - Hito 6 — Handoff (build report).

            ## Riesgos
            - Dominio: el founder debe comprarlo (no lo hago yo).
            - Form Resend: requiere DNS verificado.

            ## Decisiones que necesitan OK del founder
            - Confirmar nombre del proyecto y dominio.
            - Aprobación de publicación (Hito 4).

            (Respuesta simulada en modo mock. En modo real ejecuto el Playbook 1
            completo según `agents/domenech/playbook.md`.)
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

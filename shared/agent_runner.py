"""Bucle de tool-calling para agentes con Anthropic Claude.

Patron:
  1. LLM recibe mensaje + tools disponibles
  2. Si usa una tool -> ejecutarla -> devolver resultado al LLM
  3. Repetir hasta respuesta final o max_iter

Modos:
  LLM_MODE=mock  → respuesta simulada, sin API key, coste 0
  LLM_MODE=real  → llamada real a Anthropic (requiere ANTHROPIC_API_KEY + creditos)

Quien lo usa: Scout, Domenech, Durruti.
"""
from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from shared.herramientas import ejecutar, openai_to_anthropic
from shared.logger import PROJECT_ROOT as _ROOT, log_de

load_dotenv(_ROOT / ".env")

log = log_de("agent_runner")

_MODELO_FAST  = "claude-haiku-4-5-20251001"
_MODELO_HEAVY = "claude-sonnet-4-6"
_MODELO       = _MODELO_FAST


def _mock_response(nombre: str, mensaje: str) -> str:
    return (
        f"[MOCK · {nombre}] Briefing recibido. "
        f"Para activar respuestas reales: añade créditos en console.anthropic.com "
        f"y cambia LLM_MODE=real en .env"
    )


def ejecutar_agente(
    *,
    nombre: str,
    system_prompt: str,
    mensaje: str,
    tools: list[dict],
    max_iter: int = 8,
    terminal_tools: set[str] = frozenset({"guardar_informe", "crear_archivo"}),
    modelo: str | None = None,
    max_tokens: int = 2048,
) -> str:
    """Ejecuta el bucle de tool-calling y devuelve la respuesta final."""
    modo = os.getenv("LLM_MODE", "mock").strip().lower()
    if modo != "real":
        return _mock_response(nombre, mensaje)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "[ERROR] Falta ANTHROPIC_API_KEY en .env"

    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    _model = modelo or _MODELO

    anthropic_tools = [openai_to_anthropic(t) for t in tools] if tools else []

    messages: list[dict[str, Any]] = [{"role": "user", "content": mensaje}]
    ultimo_resultado = ""
    log.info(f"[{nombre}] inicio modelo={_model} mensaje={mensaje[:80]!r}")

    for i in range(max_iter):
        kwargs: dict[str, Any] = dict(
            model=_model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
        if anthropic_tools:
            kwargs["tools"] = anthropic_tools

        resp = client.messages.create(**kwargs)

        # Respuesta final — sin tool calls
        if resp.stop_reason == "end_turn":
            texto = "".join(b.text for b in resp.content if b.type == "text")
            log.info(f"[{nombre}] fin tras {i+1} iter ({len(texto)} chars)")
            return texto.strip() or ultimo_resultado

        # Tool use
        if resp.stop_reason != "tool_use":
            texto = "".join(b.text for b in resp.content if b.type == "text")
            return texto.strip() or ultimo_resultado

        # Añade respuesta del asistente al historial
        messages.append({"role": "assistant", "content": resp.content})

        tool_results = []
        terminar = False

        for block in resp.content:
            if block.type != "tool_use":
                continue
            resultado = ejecutar(block.name, block.input)
            ultimo_resultado = resultado
            log.info(f"[{nombre}] tool={block.name} resultado={resultado[:80]!r}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": resultado,
            })
            if block.name in terminal_tools:
                terminar = True

        messages.append({"role": "user", "content": tool_results})

        if terminar:
            log.info(f"[{nombre}] terminal tool. Fin tras {i+1} iter.")
            return ultimo_resultado

    log.warning(f"[{nombre}] maximo de iteraciones ({max_iter})")
    return ultimo_resultado or "Revisa output/ y memory/projects/ para los resultados."

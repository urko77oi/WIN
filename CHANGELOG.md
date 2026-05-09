# CHANGELOG

Cambios importantes del proyecto Durruti.
Formato libre, por fases. La fase activa va arriba.

---

## [0.0.1] — 2026-05-09 — Fase 0: Andamiaje (sandbox)

### Añadido
- Estructura completa de directorios (`config/`, `agents/`, `shared/`,
  `memory/`, `tasks/`, `scripts/`, `docs/`).
- Cliente LLM unificado (`shared/llm_client.py`) con dos modos:
  - `mock`: respuestas simuladas, coste 0, ideal para Fase 0.
  - `real`: llamadas a la API de Anthropic (deshabilitado por defecto).
- Canal humano por CLI (`shared/human_channel.py`). Telegram queda
  pendiente para Fase 1.
- Guardrails básicos como código (`shared/guardrails.py`).
- Logger con `loguru` (`shared/logger.py`).
- Tracking de costes en SQLite (`shared/cost_tracker.py`).
- Memoria persistente: archivos `.md` por proyecto + tabla SQLite
  (`shared/memory.py`).
- Tres agentes operativos:
  - **Durruti** (CEO Operativo): identidad, prompt, playbook,
    catálogo de órdenes, clase Python.
  - **Researcher**: identidad, prompt, skills, clase Python.
  - **Builder**: identidad, prompt, skills, clase Python.
- Scripts del usuario: `start.py`, `status.py`, `doctor.py`, `approve.py`.
- Documentación: `README.md`, `PROJECT_BRIEF.md` (fuente de verdad),
  `DOCTOR.md`, `HOW_TO_USE.md`, `HOW_TO_GIVE_ORDERS.md`.
- Inventario de secretos (`secrets/secrets.md`).

### Decisiones de arquitectura tomadas en Fase 0
- **Sandbox sin créditos API**: empezamos con `LLM_MODE=mock`.
  Razón: usuario no quiere meter saldo en la API hasta validar el sistema.
- **CLI primero, Telegram después**: usuario aún no tiene Telegram.
  La capa `shared/human_channel.py` ya está abstracta para enchufar
  Telegram en Fase 1 sin tocar el resto del código.
- **Sin frameworks de agentes**: orquestación construida a mano sobre
  el SDK de Anthropic. Razón: opacidad y churn de LangChain/CrewAI.
- **Estructura de directorios mínima**: las carpetas de Fase 1+
  (`tasks/in_progress/`, `proposals/`, `outputs/landings/`, etc.)
  se crean cuando llegue la funcionalidad, no antes.

### Conocido / pendiente
- `LLM_MODE=real` requiere `ANTHROPIC_API_KEY` en `.env` y créditos
  en `console.anthropic.com`. La suscripción Claude Pro NO da API.
- Telegram no conectado.
- `auditor` agent, `proposals/` flow, `anonymizer.py`, `forget.py`,
  `backup.py`, `rollback.py`: postpuesto a Fase 1+.

# CHANGELOG

Cambios importantes del proyecto Durruti.
Formato libre, por fases. La fase activa va arriba.

---

## [0.0.3] — 2026-05-09 — Integración de Domenech (Builder)

### Cambiado
- **Builder placeholder reemplazado por Domenech.** El founder entregó un
  diseño completo (9 archivos `.md`: identity, system_prompt, skills,
  playbook, heartbeat, guardrails, memory, interfaces, output_templates).
  Encaja con la filosofía de Durruti, así que se adopta tal cual y se
  deprecia el Builder mock.
- `agents/builder/` eliminado.
- `agents/domenech/` creado con los 9 `.md` originales del founder +
  `INTEGRATION.md` que documenta las adaptaciones.
- `Durruti` ahora delega construcción de landings y generación de
  contenido en `Domenech`.
- Mock de Domenech en `shared/llm_client.py` devuelve la estructura
  canónica (ADR de stack + estructura + hitos + riesgos + decisiones
  pendientes del founder).
- `config/models.yaml`: `builder → domenech` en defaults.

### Convenciones de nombres
- **Domenech** = nombre propio del agente.
- **Builder** = rol técnico. Los contratos JSON entre agentes
  (`BuildOrder`, `BuildPlan`, `MilestoneReport`, `Blocker`, `BuildReport`,
  `ScoutFeedback`, `OperatorHandoff`, `BuilderEvent`) **conservan el
  nombre técnico** porque son interfaces estables.

### Adaptaciones explícitas vs. el diseño original (en INTEGRATION.md)
- Domenech reporta a **Durruti**, no al humano.
- Outputs en `.md` (Fase 0); `.docx` (build report final) para Fase 1+.
- Catálogo completo de skills (web.astro, saas.kit_basic, pay.stripe,
  etc.), modos del heartbeat, modo agresivo ante bloqueo y contratos
  JSON: Fase 1+.
- Comandos `builder status / approve / pause / mode promote` no se
  implementan como CLI separada. Domenech se invoca a través de Durruti.

---

## [0.0.2] — 2026-05-09 — Integración del agente Scout

### Cambiado
- **Researcher reemplazado por Scout (Analista de Oportunidades).**
  El founder entregó un diseño completo del Scout (10 archivos `.md`:
  identity, mission, skills, tools, playbook, scoring, outputs, heartbeat,
  memory, guardrails). Encajan con la filosofía de Durruti, así que se
  adopta el Scout y se deprecia el Researcher placeholder.
- `agents/researcher/` eliminado.
- `agents/scout/` creado con los 10 `.md` originales + `system_prompt.md`
  + `scout.py` + `INTEGRATION.md` que documenta las adaptaciones.
- `Durruti` ahora delega investigación y auditoría de competencia en `Scout`.
- Mock de Scout en `shared/llm_client.py` devuelve la estructura canónica
  (TL;DR + triple scoring + hallazgos + riesgos + recomendación + fuentes).
- Nueva orden operativa: `auditar_competencia` (mapea a `Scout.auditar_competidor`).
- `config/models.yaml`: `researcher → scout` en defaults.

### Adaptaciones explícitas vs. el diseño original del Scout
Documentadas en `agents/scout/INTEGRATION.md`. Resumen:
- Scout reporta a **Durruti**, no directamente al humano.
- Outputs en `.md` (Fase 0). `.docx` queda para Fase 1+.
- Heartbeat 24/7, modo pánico, watchdog, tools externas (Brave, Reddit,
  Trends, marketplaces) y vector store: Fase 1+.
- Comandos `agent:start scout` no se implementan; Scout se invoca a
  través de `Durruti`.

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
  - **Builder** (placeholder, después reemplazado por Domenech en v0.0.3).
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

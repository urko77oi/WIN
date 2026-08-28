# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este proyecto

**FORRARSE**: sistema multi-agente en Python que actúa como un equipo digital para investigar y construir negocios online. Corre en local (el PC del Founder, Windows + VS Code), sin servidor. Estado actual: **Fase 0 completada** — todo funciona end-to-end en modo `mock` (sin API, coste 0).

**`PROJECT_BRIEF.md` es la fuente de verdad.** Cualquier decisión de arquitectura debe ser consistente con él o actualizarlo explícitamente. Cuando añadas un archivo nuevo, refléjalo allí. El usuario es no-programador: comunica en español llano y con errores siempre explicados.

## Comandos

```bash
uv sync                              # instalar dependencias (crea .venv)
cp .env.example .env                 # config de entorno (en Windows: copy)
uv run python scripts/start.py      # arranca el CLI de Durruti
uv run python scripts/status.py     # estado y métricas
uv run python scripts/doctor.py     # autodiagnóstico → logs/doctor-*.md
uv run python scripts/approve.py    # aprobar/rechazar tareas pendientes
```

- `LLM_MODE=mock` (default) funciona sin API key ni internet. `LLM_MODE=real` requiere `ANTHROPIC_API_KEY` en `.env`.
- No hay suite de tests ni linter todavía (Fase 0). En Fase 1+ los tests son obligatorios para `shared/` y `guardrails.py`.
- El usuario trabaja en Windows/PowerShell: al darle comandos, usa sintaxis PowerShell.

## Arquitectura

Tres agentes orquestados manualmente sobre el SDK de Anthropic (**prohibido** LangChain/CrewAI/AutoGen; sin Docker ni BBDD vectoriales):

- **Durruti** (`agents/durruti/`) — CEO/orquestador. Único interlocutor con el humano. Descompone órdenes (catálogo en `order_catalog.md`) y delega.
- **Scout** (`agents/scout/`) — analista de oportunidades. Investiga y puntúa con triple scoring; no actúa, reporta.
- **Domenech** (`agents/domenech/`) — builder. Convierte oportunidades en activos (landings, blogs, automatizaciones).

**Los agentes se definen en Markdown, no en código.** Cada carpeta de agente tiene ~10 `.md` (`identity.md`, `system_prompt.md`, `skills.md`, `playbook.md`, `guardrails.md`…) que `shared/agent_loader.py` compone en el prompt completo, anteponiendo el bloque común `CONTEXTO_FORRARSE`. La clase Python del agente (`durruti.py`, etc.) es solo el runtime. Cambiar el comportamiento de un agente = editar sus `.md`.

Infraestructura compartida en `shared/`:

- `llm_client.py` — cliente único del LLM con modos `mock`/`real` (`LLM_MODE`). El routing de modelo por agente/tarea está en `config/models.yaml`.
- `guardrails.py` — reglas inviolables **aplicadas como código**, no solo en prompt. Toda acción con efectos (escribir archivos, shell, APIs) pasa por aquí; si falla lanza `GuardrailViolation` con mensaje en español entendible por no-programador.
- `cost_tracker.py` — registra cada llamada API con coste estimado (precios y límites duros en `config/budget.yaml`; superar el límite pausa el sistema).
- `memory.py` — memoria en 3 capas: RAM del proceso (corta), `.md` en `memory/{projects,learnings,playbooks}/` (media), SQLite en `memory/db.sqlite` (larga; se crea sola al arrancar).
- `human_channel.py` — canal de aprobación humana: CLI en Fase 0, Telegram en Fase 1.

La cola de tareas son archivos en `tasks/pending/` (KISS deliberado, sin broker).

## Guardrails que te afectan directamente

- **Nunca push directo a `main`.** Cambios vía rama + PR que el humano revisa.
- Los agentes no modifican su propio `system_prompt.md`/`identity.md` directamente: propuesta en `proposals/` → aprobación humana → merge.
- Pagos, publicaciones públicas, emails masivos, borrado de archivos y comandos shell requieren aprobación humana explícita (lista en `config/budget.yaml`).
- Secretos jamás en commits: viven en `.env` / `secrets/.env`; `secrets/secrets.md` es solo el inventario documental.
- Si una funcionalidad pedida cae en "no realista" (ver PROJECT_BRIEF §2), avisa y propone alternativa en lugar de simular que funciona.

## Convenciones

- **Idioma**: español en logs, docs, docstrings, comentarios y comunicación; inglés en identificadores de código.
- Commits con formato `[agente] acción` — ej. `[builder] añade plantilla landing minimalista`.
- Nada hardcodeado: valores configurables van a `config/*.yaml`.
- Cada módulo Python lleva docstring explicando qué hace, quién lo usa, inputs/outputs; funciones públicas con type hints.
- Logging vía `shared/logger.py` (loguru), nunca `print` para diagnóstico.
- Ante estructura inesperada del repo, **pregunta antes de improvisar** (regla de `SETUP.md`).

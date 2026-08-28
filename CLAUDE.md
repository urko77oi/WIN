# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este proyecto

**FORRARSE**: sistema multi-agente en Python que actúa como un equipo digital para investigar y construir negocios online. Corre en local en el PC del Founder (**Windows** + VS Code — hay dependencias solo-Windows como `pywin32`, y scripts `.bat`/`.ps1`). El Founder es **no-programador**: comunica en español llano, con errores siempre explicados.

**`PROJECT_BRIEF.md` es la fuente de verdad** del diseño original (Fase 0). El repo ha evolucionado más allá de lo que documenta: voz, Telegram, comunidad Skool y ciclos de investigación de nichos ya están construidos. Ante contradicción entre brief y código, manda el código actual — y actualiza el brief.

## Comandos

```powershell
uv sync                                   # instalar dependencias (crea .venv)
copy .env.example .env                    # config de entorno (primera vez)
uv run python scripts/start.py           # CLI de Durruti
uv run python scripts/status.py          # estado, métricas y costes
uv run python scripts/doctor.py          # autodiagnóstico → logs/doctor-*.md
uv run python scripts/approve.py         # aprobar/rechazar tareas pendientes
uv run python scripts/start_telegram.py  # bot de Telegram
uv run python scripts/voz_chat.py        # chat por voz push-to-talk
uv run python scripts/durruti_escucha.py # voz siempre activa (wake word)
uv run python scripts/buscar_oportunidades.py  # ciclo de investigación de nichos
```

- `LLM_MODE=mock` (default) funciona sin API key ni internet; `LLM_MODE=real` requiere `ANTHROPIC_API_KEY` en `.env`.
- La voz usa un stack gratuito: Groq (Whisper STT + Llama) + Edge TTS. Requiere `GROQ_API_KEY` y `DURRUTI_VOICE_ID` en `.env` (detalles en README).
- No hay suite de tests ni linter configurados. El PROJECT_BRIEF los exige en Fase 1+ para `shared/` y `guardrails.py`.
- El usuario trabaja en PowerShell: al darle comandos, usa sintaxis PowerShell.

## Arquitectura

Orquestación manual sobre el SDK de Anthropic (**prohibido** LangChain/CrewAI/AutoGen; sin Docker ni BBDD vectoriales). Hay **dos generaciones de agentes** conviviendo en `agents/`:

**Generación 1 — definidos en Markdown** (Durruti, Scout, Domenech): cada carpeta tiene ~10 `.md` de diseño (`identity.md`, `system_prompt.md`, `playbook.md`, `guardrails.md`…) que `shared/agent_loader.py` compone en el prompt completo, anteponiendo el bloque común `CONTEXTO_FORRARSE`. El `.py` es solo el runtime. Cambiar su comportamiento = editar sus `.md`.

- **Durruti** — CEO/orquestador, único interlocutor con el humano (catálogo de órdenes en `order_catalog.md`).
- **Scout** — analista de oportunidades, triple scoring; no actúa, reporta.
- **Domenech** — builder: landings, blogs, automatizaciones.

**Generación 2 — ligeros** (Emma, Guion, Pixel, Viral): un solo `.py` con el system prompt inline, ejecutados vía `shared/agent_runner.ejecutar_agente()` con las tools de `shared/herramientas.py` (loop de tool-use con límite de iteraciones). Emma es community manager de la comunidad Skool; guion/pixel/viral son agentes de contenido. Los nuevos agentes siguen este patrón, no el de Markdown.

Infraestructura en `shared/`:

- `llm_client.py` — cliente único del LLM, modos `mock`/`real` (`LLM_MODE`); routing de modelos en `config/models.yaml`.
- `agent_runner.py` + `herramientas.py` — loop de ejecución con tools para los agentes de generación 2.
- `guardrails.py` — reglas inviolables **aplicadas como código**, no solo en prompt. Acciones con efectos pasan por aquí; si falla lanza `GuardrailViolation` con mensaje en español para no-programador.
- `cost_tracker.py` — coste estimado de cada llamada (límites duros en `config/budget.yaml`; superarlos pausa el sistema).
- `memory.py` — memoria en 3 capas: RAM (corta), `.md` en `memory/` (media), SQLite `memory/db.sqlite` (larga, se crea sola).
- `telegram_bot.py` / `human_channel.py` — canales de aprobación humana (Telegram y CLI).
- `stt_service.py` / `tts_service.py` — voz (Groq Whisper / Edge TTS).
- `email_sender.py` — envío de email.

Otras piezas: `tasks/pending/` es la cola de trabajo (archivos, KISS deliberado); `output/` recibe lo que generan los agentes (landings, contenido Skool…); `memory/` acumula los datos de los ciclos de investigación; `scripts/session_end.ps1` hace los auto-commits de fin de sesión.

## Guardrails que te afectan directamente

- **Nunca push directo a `main`.** Cambios vía rama + PR que el humano revisa.
- Los agentes de generación 1 no modifican su propio `system_prompt.md`/`identity.md`: propuesta → aprobación humana → merge.
- Pagos, publicaciones públicas, emails masivos, borrado de archivos y comandos shell requieren aprobación humana explícita (lista en `config/budget.yaml`).
- Secretos jamás en commits: viven en `.env` / `secrets/.env`; `secrets/secrets.md` es solo inventario documental.
- Si una funcionalidad pedida es de las "no realistas" del PROJECT_BRIEF §2 (hacerse rico solo, trading automático…), avisa y propone alternativa realista en lugar de simular que funciona.

## Convenciones

- **Idioma**: español en logs, docs, docstrings, comentarios y comunicación; inglés en identificadores de código (los agentes nuevos usan también nombres en español — sigue el estilo del archivo que toques).
- Commits con formato `[agente] acción` — ej. `[builder] añade plantilla landing minimalista`.
- Nada hardcodeado: valores configurables van a `config/*.yaml`.
- Módulos con docstring explicando qué hace y quién lo usa; funciones públicas con type hints.
- Logging vía `shared/logger.py` (loguru), nunca `print` para diagnóstico.
- Si algo falla y no está claro por qué: `DOCTOR.md` tiene el protocolo de diagnóstico.
- Ante estructura inesperada del repo, pregunta antes de improvisar (regla de `SETUP.md`).

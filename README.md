# Durruti

Sistema multi-agente que actúa como equipo digital para gestionar negocios online.
**Durruti** es el CEO Operativo: único interlocutor con el humano, descompone
órdenes y delega en agentes especializados (Scout, Domenech).

> Fuente de verdad del proyecto: [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md).
> Si algo cambia, se actualiza ahí.

---

## Estado actual

**Fase 0 — Andamiaje (sandbox).**

- ✅ Estructura de directorios.
- ✅ Cliente LLM con dos modos: `mock` (sin coste) y `real` (API Anthropic).
- ✅ Canal humano por CLI (Telegram llegará en Fase 1).
- ✅ Guardrails básicos, logging, tracking de costes.
- ✅ Durruti + Scout (Analista de Oportunidades) + Domenech (Builder) funcionando end-to-end en modo mock.
- ✅ Triple scoring (Conservador / Equilibrado / Agresivo) en los outputs del Scout.
- ⏳ Llamadas reales al modelo: deshabilitadas hasta meter créditos en
  `console.anthropic.com` y cambiar `LLM_MODE=real` en `.env`.

---

## Arranque rápido

Requisitos: **Python 3.11+** y [`uv`](https://github.com/astral-sh/uv) instalado.

```powershell
# 1. Entrar al proyecto
cd durruti

# 2. Instalar dependencias
uv sync

# 3. Copiar plantilla de entorno (la primera vez)
copy .env.example .env

# 4. Arrancar Durruti
uv run python scripts/start.py
```

Aparecerá el prompt CLI de Durruti. Escribe una orden en español, por ejemplo:

```
> investiga el nicho cursos yoga online
```

Durruti la descompondrá, delegará en Scout, y devolverá un informe.
En modo `mock` la respuesta es predecible (sin coste, sin internet).

---

## Comandos disponibles

| Comando | Qué hace |
|---|---|
| `uv run python scripts/start.py` | Arranca Durruti en CLI |
| `uv run python scripts/status.py` | Estado, métricas y costes acumulados |
| `uv run python scripts/doctor.py` | Autodiagnóstico cuando algo falla |
| `uv run python scripts/approve.py` | Aprueba/rechaza tareas pendientes |

---

## Estructura

```
durruti/
├── PROJECT_BRIEF.md     # Fuente de verdad del proyecto
├── DOCTOR.md            # Protocolo cuando algo falla
├── CHANGELOG.md         # Cambios importantes
├── config/              # Settings, budget, modelos
├── secrets/             # ⚠️ NUNCA en git
├── agents/              # Identidades + prompts + código de cada agente
│   ├── durruti/         # CEO Operativo
│   ├── scout/           # Analista de Oportunidades (10 .md de diseño)
│   └── domenech/        # Builder — Constructor de entregables (9 .md de diseño)
├── shared/              # Núcleo común (LLM, memoria, guardrails, logs)
├── memory/              # Conocimiento persistente entre sesiones
├── tasks/               # Cola de trabajo
├── logs/                # Trazas operativas
├── scripts/             # Comandos del usuario
└── docs/                # Manuales
```

---

## Si algo va mal

1. `uv run python scripts/doctor.py` → autodiagnóstico.
2. Mira el log más reciente en `logs/`.
3. Lee [`DOCTOR.md`](DOCTOR.md) para el protocolo.
4. Si nada de lo anterior aclara: copia el último log a Claude Code y pídele que diagnostique.

---

## Próximos pasos (Fase 1)

- Conectar Telegram bot.
- Activar llamadas reales al modelo (`LLM_MODE=real`).
- Memoria SQLite con esquema completo.
- Domenech generando primera landing real (skills web.astro / web.next_static reales).
- 6 órdenes operativas del catálogo (`agents/durruti/order_catalog.md`).

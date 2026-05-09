# FORRARSE

Sistema multi-agente para construir y operar negocios online.
Trabaja en local (Windows + VS Code), con aprobación humana para cualquier
acción con impacto real (pagos, publicación, irreversibles).

> Fuente de verdad del proyecto: [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md).
> Cualquier cambio de arquitectura se refleja ahí.

---

## Organigrama

```
            Founder (humano)
                  │
                  ▼
         ┌────────────────┐
         │    Durruti     │   CEO Operativo
         │                │   Único interlocutor con el Founder.
         └───────┬────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
  ┌──────────┐      ┌───────────┐
  │  Scout   │      │ Domenech  │
  │ Analista │      │  Builder  │
  │ de Oport.│      │           │
  └──────────┘      └───────────┘
```

- **Founder** — el humano. Da las órdenes. Aprueba pagos, publicaciones,
  irreversibles.
- **Durruti** — CEO. Recibe órdenes, descompone, delega, supervisa, reporta.
- **Scout** — Analista de Oportunidades. Investiga, valida, prioriza con
  triple scoring (Conservador/Equilibrado/Agresivo). No actúa: reporta.
- **Domenech** — Builder. Construye los activos digitales (landings, blogs,
  SaaS micro, automatizaciones). Calidad de día 1, modo agresivo ante
  bloqueos, barato por defecto.

---

## Estado actual

**Fase 0 — Andamiaje (sandbox).**

- ✅ Estructura de directorios.
- ✅ Cliente LLM con dos modos: `mock` (sin coste) y `real` (API Anthropic).
- ✅ **Loader de prompts** que compone el contexto completo de cada agente
  uniendo todos sus `.md` de diseño + organigrama de FORRARSE.
- ✅ Canal humano por CLI (Telegram para Fase 1).
- ✅ Guardrails como código + tracking de costes en SQLite.
- ✅ Durruti + Scout + Domenech funcionando end-to-end en modo mock.
- ⏳ Llamadas reales al modelo: deshabilitadas hasta meter créditos en
  `console.anthropic.com` y cambiar `LLM_MODE=real` en `.env`.

---

## Arranque rápido

Requisitos: **Python 3.11+** y [`uv`](https://github.com/astral-sh/uv) instalado.

```powershell
# 1. Entrar al proyecto
cd FORRARSE

# 2. Instalar dependencias
uv sync

# 3. Copiar plantilla de entorno (la primera vez)
copy .env.example .env

# 4. Hablar con Durruti
uv run python scripts/start.py
```

Aparece el prompt CLI de Durruti. Escribe órdenes en español:

```
> investiga el nicho cursos yoga online
> crea una landing para vender un curso de fotografía móvil
> audita competidor mindvalley
> status
```

En modo `mock` las respuestas son simuladas pero estructuradas (sin coste,
sin internet). Cuando metas créditos y pongas `LLM_MODE=real`, las
llamadas pasan a ser reales con el contexto completo de cada agente.

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
FORRARSE/
├── PROJECT_BRIEF.md     # Fuente de verdad del proyecto
├── DOCTOR.md            # Protocolo cuando algo falla
├── CHANGELOG.md         # Cambios importantes
├── config/              # Settings, budget, modelos
├── secrets/             # ⚠️ NUNCA en git
├── agents/              # Equipo (cada agente con su `.md` + código)
│   ├── durruti/         # CEO Operativo
│   ├── scout/           # Analista de Oportunidades (10 .md de diseño)
│   └── domenech/        # Builder — Constructor (9 .md de diseño)
├── shared/              # Núcleo común
│   ├── llm_client.py    # Cliente LLM (mock + real)
│   ├── agent_loader.py  # Compositor del prompt completo de cada agente
│   ├── memory.py        # Memoria persistente (SQLite + .md)
│   ├── guardrails.py    # Reglas inviolables como código
│   ├── cost_tracker.py  # Tracking de gasto por llamada
│   └── human_channel.py # Canal CLI (Telegram en Fase 1)
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

- Conectar Telegram bot (canal humano fuera del PC).
- Activar llamadas reales al modelo (`LLM_MODE=real`).
- Tablas SQLite específicas de Scout (`opportunities`, `score_history`,
  `outcomes`...) y de Domenech (`build_logs`, `build_decisions`...).
- Skills reales del catálogo: `web.astro`, `web.next_static`, `pay.stripe`,
  `email.resend`, `deploy.cloudflare_pages`, etc.
- Domenech generando primera landing real.

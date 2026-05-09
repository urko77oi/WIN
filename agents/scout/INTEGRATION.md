# Notas de integración del Scout en Durruti

Este documento explica cómo el agente **Scout** (definido en `identity.md`,
`mission.md`, `skills.md`, `tools.md`, `playbook.md`, `scoring.md`,
`outputs.md`, `heartbeat.md`, `memory.md`, `guardrails.md`) se integra en
el sistema **Durruti**.

Los archivos `.md` se conservan **tal cual** los entregó el founder. Las
adaptaciones operativas (qué se aplica ahora, qué queda para fases futuras)
se documentan aquí.

---

## 1. Quién habla con quién

El Scout está pensado en sus archivos como un agente que **reporta
directamente al founder**. En Durruti la regla es distinta:

> **Único interlocutor con el humano: Durruti (CEO Operativo).**
> Scout, Domenech (Builder) y futuros agentes reportan a Durruti, no al Founder.

Adaptación operativa:
- Donde los archivos del Scout dicen "founder" en sentido de "humano que
  recibe el output", se entiende **"Durruti"** en Fase 0/1. Durruti
  consolida los hallazgos y los entrega al humano.
- Las decisiones de "go / no-go / investigar más" sobre oportunidades las
  sigue tomando el humano, **a través de Durruti**.

---

## 2. Qué se aplica en Fase 0 (mock + CLI)

- ✅ **Identidad y filosofía:** se respetan al 100%. Scout es el analista
  obsesivo, crítico, datos-primero.
- ✅ **Triple scoring obligatorio (Conservador / Equilibrado / Agresivo):**
  estructura adoptada en los outputs aunque las puntuaciones de Fase 0
  vienen de mock.
- ✅ **Memoria persistente compartida:** Scout usa `shared/memory.py`
  (no monta su propia BD). Las tablas que requiere (`opportunities`,
  `score_history`, `sources`, `decisions`, `outcomes`, `monitor_signals`,
  `agent_metrics`) se añadirán al esquema en Fase 1+ junto con el
  triple-scoring real.
- ✅ **Guardrails inviolables:** las reglas G1-G10 de `guardrails.md`
  se mantienen. La capa técnica de validación vive en `shared/guardrails.py`.

## 3. Qué queda para Fase 1+

- ⏳ **Tools externas** (`tools.md`): Brave, Reddit API, Google Trends,
  marketplaces, etc. En Fase 0 todo es mock. En Fase 1+ se implementan
  en `shared/tools/` con guardrails de coste.
- ⏳ **Outputs en `.docx`** (`outputs.md`): se sustituyen por `.md` en
  Fase 0 para no añadir dependencia `python-docx`. En Fase 1+ se añade
  como skill opcional.
- ⏳ **Heartbeat 24/7** (`heartbeat.md`): los workflows daily/weekly/postmortem
  con cron requieren un demonio en background. Fase 0 es CLI puro;
  Fase 2+ se implementa con un scheduler (APScheduler / cron del SO).
- ⏳ **Modo pánico y watchdog externo:** Fase 1+, junto con el resto del
  ciclo de vida del agente.
- ⏳ **Vector store** (`memory.md`): Chroma/Qdrant para búsqueda semántica
  llega cuando haya histórico real que indexar.
- ⏳ **Comandos CLI propios** (`agent:start scout`, `agent:scout brief ...`):
  no existen como CLI separada. Scout se invoca a través de Durruti.

## 4. Diferencia con el Researcher anterior

El agente `researcher` mock que hubo en la versión inicial de Fase 0 queda
**deprecado** y reemplazado por Scout. La carpeta `agents/researcher/` se
elimina. Durruti pasa a delegar investigación en `Scout`.

## 5. Cuándo se actualiza este documento

Cada vez que un punto de "Fase 1+" se mueva a "implementado en producción",
se mueve aquí también. El objetivo es que la distancia entre los `.md` de
diseño del Scout y la realidad operativa esté **siempre explicitada**.

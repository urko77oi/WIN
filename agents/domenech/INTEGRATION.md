# Notas de integración de Domenech (Builder) en Durruti

Este documento explica cómo el agente **Domenech** (rol técnico: Builder)
se integra en el sistema **Durruti**.

Los archivos `.md` se conservan **tal cual** los entregó el founder. Las
adaptaciones operativas (qué se aplica ahora, qué queda para fases
futuras) se documentan aquí.

---

## 1. Nombre, rol y contratos

- **Nombre propio del agente:** `Domenech`.
- **Rol técnico:** `Builder` (constructor del sistema).
- **Contratos JSON entre agentes** (`BuildOrder`, `BuildPlan`,
  `MilestoneReport`, `Blocker`, `BuildReport`, `ScoutFeedback`,
  `OperatorHandoff`, `BuilderEvent`) **conservan el nombre técnico** —
  son interfaces estables, no nombres propios.

Cuando los `.md` dicen "el Builder" como sujeto/voz, es Domenech hablando.
Cuando dicen "BuildOrder", "BuildPlan", etc., son contratos.

---

## 2. Quién habla con quién

Domenech, igual que Scout, **reporta a Durruti**. Durruti es el único
agente que se comunica con el humano. La cadena es:

```
Founder → Durruti → Domenech (recibe BuildOrder)
                  ↘ Scout (a veces)
Domenech → Durruti (entrega plan, hitos, blockers, build report)
Durruti → Founder (consolida, pide aprobaciones)
```

---

## 3. Qué se aplica en Fase 0 (mock + CLI)

- ✅ **Identidad y filosofía:** se respetan al 100%. Domenech es el
  constructor obsesionado con calidad, resolutivo, barato por defecto,
  honesto operativamente.
- ✅ **Modo `validation` por defecto:** alineado con la filosofía de
  Durruti de "humano en el loop". El paso a `autonomous` se hace cuando
  el founder lo decida explícitamente, después de N proyectos sin
  incidentes.
- ✅ **Skills genéricas adoptadas como API en Fase 0:**
  `proponer_landing(brief)` y `generar_contenido(brief)` exponen al
  Domenech mock devolviendo plantillas plausibles. En Fase 1+ se
  sustituyen por las skills reales del catálogo (web.astro,
  saas.kit_basic, etc.).

## 4. Qué queda para Fase 1+

- ⏳ **Catálogo completo de skills** (`skills.md` § 1-17): web.astro,
  cms.wordpress, ecom.shopify, saas.kit_basic, pay.stripe, deploy.vercel,
  etc. En Fase 0 todo es mock; en Fase 1+ se implementan en
  `shared/tools/` con guardrails de coste.
- ⏳ **Outputs en `.docx`** (`output_templates.md`): el Build Report final
  es `.docx` por preferencia del founder. En Fase 0 se sustituye por `.md`
  para no añadir dependencia `python-docx`.
- ⏳ **Heartbeat con modos** (`heartbeat.md`): los estados
  `idle | planning | building | awaiting_approval | monitoring | escalated | paused`
  y los ciclos auto-iniciados llegan en Fase 1+ con un scheduler.
- ⏳ **Modo agresivo ante bloqueo** (`playbook.md` § Playbook 6): los 5
  niveles de escalada (retry → diagnose → workaround → swap proveedor →
  cambio paradigma → escalate) se implementan cuando haya skills reales
  que puedan bloquearse.
- ⏳ **Contratos JSON** (`interfaces.md`): se adoptan como diseño futuro.
  En Fase 0 los agentes se llaman directamente vía clases Python; los
  contratos se materializarán en `tasks/pending/` cuando haya un loop de
  ejecución asíncrono.
- ⏳ **Tablas SQLite específicas del Builder** (`memory.md`): se añaden
  al esquema de `shared/memory.py` cuando el primer build real esté en
  marcha.
- ⏳ **Comandos CLI propios** (`builder status`, `builder approve`, etc.):
  no se implementan como CLI separada. Domenech se invoca a través de
  Durruti. La aprobación humana usa el canal central
  (`shared/human_channel.py`).

## 5. Diferencia con el Builder placeholder anterior

La versión inicial de Fase 0 tenía un `agents/builder/` con un mock
genérico. Queda **deprecado** y reemplazado por Domenech. La carpeta
`agents/builder/` se elimina. Durruti pasa a delegar construcción en
`Domenech`.

## 6. Cuándo se actualiza este documento

Cada vez que un punto de "Fase 1+" se mueva a "implementado en
producción", se mueve aquí también. La distancia entre los `.md` de
diseño de Domenech y la realidad operativa debe estar **siempre
explicitada**.

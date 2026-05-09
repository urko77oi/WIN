# PROJECT BRIEF v2 — Durruti & Equipo: Sistema Multi-Agente Autónomo de Negocios Online

> **Documento maestro para Claude Code.** Léelo entero antes de proponer nada. Al final, en §17, está el bloque "PRIMER MENSAJE A CLAUDE CODE" con la instrucción inicial exacta. Este documento es la fuente de verdad del proyecto; cualquier decisión que se tome durante el desarrollo debe ser consistente con lo aquí definido o actualizar este archivo explícitamente.

---

## 0. RESUMEN EJECUTIVO (TL;DR)

Construir un **sistema multi-agente** ejecutado localmente en VS Code (Windows) que actúe como un equipo digital capaz de investigar, planificar, ejecutar, operar y reportar negocios online (gestión de redes, creación de webs, automatizaciones, gestión de WhatsApp, contenido).

El sistema gira alrededor de **Durruti**, el CEO Operativo: único interlocutor con el usuario, descompone órdenes y delega en agentes especializados. Toda decisión que implique gastar dinero o ejecutar acciones irreversibles requiere **aprobación humana explícita** vía un canal que el usuario tenga siempre a mano (Telegram).

**Filosofía:** empezar con lo MÍNIMO que funcione, validar, e ir añadiendo capacidades. No construir nada que aún no se necesite. Honestidad por encima de marketing: si algo no es realista, se dice y se propone alternativa.

---

## 1. CONTEXTO DEL USUARIO Y RESTRICCIONES REALES

| Variable | Valor |
|---|---|
| Nivel técnico | No-programador. Depende de Claude Code para escribir y mantener el código. |
| Sistema operativo | Windows + VS Code |
| Plan IA actual | Claude Pro (suscripción). Posible salto a API o Pro Max si la facturación lo justifica. |
| Idioma del sistema | **Español** en prompts, logs, reportes y comunicación con el usuario. Código en inglés (variables, funciones); comentarios y docstrings en español. |
| Negocios objetivo | Negocios automatizados, gestión de redes, creación de webs, gestión de WhatsApp, automatización de procesos. |
| Autonomía | Máxima dentro del plan. **Pagos y acciones financieras siempre con aprobación humana.** |
| Arquitectura | Durruti (CEO) + agentes especializados. Justificada en §3. |
| Canal de aprobación humana | **Telegram bot** desde Fase 1. CLI como respaldo. |
| Horizonte | Construcción iterativa por fases. |

### Restricciones derivadas (no negociables)

1. **Todo escrito para que Claude Code lo entienda en futuras sesiones**, no para que el usuario lo lea línea a línea. Documentación exhaustiva, convenciones explícitas, archivos de contexto persistente.
2. **El usuario no puede depurar errores complejos.** → Logs detallados + comando `doctor` para autodiagnóstico (§11).
3. **Coste de inferencia es la principal preocupación operativa.** → Modelo más barato suficiente para cada tarea, caché agresiva, evitar bucles caros (§10).
4. **Sin servidor inicialmente.** Todo corre en el PC del usuario. El sistema debe poder hibernar y retomarse sin perder contexto.
5. **El sistema piensa y responde en español.** Excepción: el código (nombres de variables, funciones, librerías) sigue en inglés por convención técnica.

---

## 2. EXPECTATIVAS REALISTAS (HONESTIDAD CRÍTICA)

### Realista hoy
- Ahorrar al usuario decenas de horas semanales en tareas repetitivas.
- Generar borradores de contenido, webs, propuestas, posts, respuestas WhatsApp.
- Investigar nichos, competidores, palabras clave, tendencias.
- Mantener un pipeline de tareas y proyectos coordinados.
- Detectar oportunidades y proponer planes al usuario.
- Aprender del feedback humano y mejorar prompts/playbooks con el tiempo.

### Posible pero exige iteración y supervisión
- Auto-mejora del código: factible si está bien acotado. Lo haremos con **PRs hacia ramas separadas + aprobación humana**, nunca push directo a `main`.
- Negocios end-to-end automáticos: posible para nichos concretos (afiliación, contenido SEO, dropshipping de bajo volumen) tras meses de ajuste.
- Aprendizaje persistente: lo simulamos con memoria estructurada (archivos `.md` de aprendizajes), no fine-tuning.

### No realista (no prometemos)
- "Un agente que se hace rico solo." No existe.
- Trading automático rentable consistente. **Fuera de scope.**
- Ejecución 100% sin supervisión durante semanas.
- Decisiones legales, fiscales o financieras complejas sin humano en el loop.

**Si Claude Code detecta que una funcionalidad solicitada cae en "no realista", debe avisar y proponer alternativas realistas en lugar de simular que funciona.**

---

## 3. ARQUITECTURA: DURRUTI Y SU EQUIPO

### Decisión: Orquestador + agentes especializados

Elegido: **Durruti + 3-5 especialistas**. Pros: separación clara, escalable, contextos limpios, fácil ampliar. Contras: orquestación más compleja (asumible).

### Roles

- **Durruti (CEO Operativo)** — único punto de contacto con el humano. Recibe la orden, la descompone, decide qué especialista la ejecuta, supervisa, pide aprobaciones, y entrega el resultado consolidado. Tiene memoria de todos los proyectos activos y prioridades.
- **Researcher** — investigación, scraping ligero, análisis de mercado, palabras clave, competencia, recopilación.
- **Builder** — crea cosas: webs (HTML/Astro), código de automatizaciones, contenido (posts, emails, copy), procesos.
- **Operator** (Fase 2) — mantiene cosas vivas: responde WhatsApp, publica en redes, envía emails, day-to-day.
- **Auditor** (Fase 3) — revisa la calidad antes de entregar al usuario.

### Por qué Fase 1 = Durruti + Researcher + Builder

Operator necesita integraciones externas (WhatsApp, redes) con riesgo y curva de aprendizaje. Conviene postergar hasta tener algo que operar.

---

## 4. STACK TÉCNICO

Diseñado para: **bajo coste, no-programador, Windows, escalable.**

### Core
- **Lenguaje:** Python 3.11+
- **Entornos:** `uv` (rápido).
- **Modelo IA:** API de Anthropic (necesita créditos, no incluido en Claude Pro). Fase 0 corre en modo `mock` sin API.
- **Framework agentes:** **construcción manual sobre el SDK de Anthropic**. NO LangChain/CrewAI/AutoGen.
- **Orquestación de tareas:** archivos JSON/YAML como cola + loop principal. KISS.
- **Memoria:**
  - **Corta:** contexto de la conversación actual (RAM del proceso).
  - **Media:** archivos `.md` versionados en `/memory/`.
  - **Larga:** SQLite local (`projects`, `tasks`, `learnings`, `decisions`, `costs`).
- **Logging:** `loguru`.
- **Notificaciones humano:** **bot de Telegram** (Fase 1). CLI como respaldo (Fase 0).

### Lo que NO usamos y por qué
- LangChain/LangGraph/CrewAI/AutoGen → opaco para no-programador.
- BBDD vectoriales → innecesarias en Fase 1.
- Docker → fricción extra en Windows.
- k8s, microservicios → sobreingeniería.

---

## 5. ESTRUCTURA DE DIRECTORIOS

Ver el README.md y el árbol real del repo. Estructura mínima de Fase 0; las
carpetas adicionales (`tasks/in_progress/`, `proposals/`, `outputs/landings/`,
etc.) se crean cuando llegue su funcionalidad.

### Archivos clave por agente

**`identity.md`** — quién es, en una página: nombre, rol, misión, valores, estilo, qué NO hace.

**`system_prompt.md`** — prompt completo que se inyecta al modelo. Construido a partir de identity + skills + reglas operativas.

**`skills.md`** — lista viva de capacidades: habilidad → cuándo usarla → cómo invocarla → ejemplos. Se actualiza cuando el agente aprende algo nuevo.

**`playbook.md`** (solo Durruti) — cómo decide: para una orden tipo X sigo los pasos Y; cuándo pido aprobación humana; cómo reporta resultados.

**`order_catalog.md`** (solo Durruti) — catálogo de órdenes-tipo (§9).

---

## 6. GUARDRAILS Y SEGURIDAD

Inviolables, aplicados vía código (`shared/guardrails.py`), no solo en prompt.

### Financieros
1. **Ningún pago se ejecuta sin aprobación humana explícita** vía Telegram o CLI.
2. **Límite duro de gasto en APIs** en `config/budget.yaml`. Superado → pausa.
3. **Logs de cada llamada API** con coste estimado.
4. **Nunca almacenar datos de tarjetas, contraseñas bancarias o claves de finanzas** fuera del vault de secretos.

### De acción
5. **Acciones irreversibles requieren confirmación**: publicar contenido público, enviar emails masivos, modificar webs en producción, borrar archivos, ejecutar pagos.
6. **Nunca push directo a `main`.** El agente abre PRs/branches; el usuario revisa y mergea.
7. **Sandbox de ejecución de código:** código generado se revisa antes de ejecutar; ejecución en directorio aislado.
8. **Lista negra de comandos shell:** `rm -rf`, `del /s`, `format`, modificación de sistema → bloqueados.

### Legales y reputacionales
9. **No suplantar a personas reales.** Operator firma como "asistente de [usuario]" y avisa cuando una conversación necesita al humano.
10. **No publicar contenido sin revisión humana en Fase 1.**
11. **Cumplir RGPD** si gestiona datos personales.
12. **No participar en spam, fraude, manipulación de reviews, scraping prohibido por ToS.**

### Auto-modificación
13. **El agente NO modifica su propio `system_prompt.md` ni `identity.md` directamente.** Propone cambios en `proposals/` → aprobación humana → merge.
14. **Toda auto-mejora**: propuesta → revisión → aplicación.

---

## 7. GESTIÓN DE SECRETOS Y CREDENCIALES

1. Ningún secreto jamás en un commit. `.gitignore` bloquea `secrets/`, `.env`, `*.key`, `*.pem`.
2. Todos los secretos viven en `secrets/.env` (o el `.env` de la raíz) con nombres consistentes.
3. `secrets/secrets.md` es un inventario vivo. Lo mantiene Durruti.
4. Pre-commit hook (Fase 0.5) escanea por patrones de claves antes de commitear.
5. Cuando una key se necesita, Durruti pide al usuario por Telegram/CLI.
6. Rotación: `secrets.md` indica cada cuánto rotar.
7. Backup cifrado (Fase 1+).

---

## 8. CANAL HUMANO: TELEGRAM + CLI

Telegram es el canal por defecto desde Fase 1. CLI es el respaldo y el canal
único en Fase 0.

### Tipos de mensaje
- **Info** — "He completado X". No requiere respuesta.
- **Aprobación** — "Voy a hacer Y (coste: Z€). [✅ Aprobar] [❌ Rechazar] [💬 Discutir]".
- **Pregunta** — "Para Y necesito que decidas A o B."
- **Alerta** — "Algo va mal. He pausado X."

### Modo "usuario dormido / asíncrono"

| Tiempo sin respuesta | Acción |
|---|---|
| 0–30 min | Espera silenciosa |
| 30 min – 2 h | Re-notifica una vez |
| 2 h – 24 h | Trabaja en tareas que NO requieren aprobación |
| > 24 h | Resumen diario al usuario |
| > 7 días | Pausa el proyecto correspondiente y avisa |

---

## 9. CATÁLOGO INICIAL DE ÓRDENES OPERATIVAS

Ver `agents/durruti/order_catalog.md` para el catálogo vivo.

### Órdenes Fase 1
1. `investigar_nicho(nicho, profundidad)`
2. `crear_landing(objetivo, estilo, info)`
3. `generar_contenido(tema, formato, cantidad)`
4. `auditar_competencia(competidor)`
5. `crear_proyecto(nombre, descripción, objetivo)`
6. `status()`

### Órdenes Fase 2 (con Operator)
7. `responder_whatsapp(número, contexto)`
8. `publicar_red(red, contenido, programación)`
9. `enviar_email(destinatarios, contenido)`
10. `automatizar_proceso(descripción)`

---

## 10. COSTES Y POLÍTICA DE GASTO

- **Fase 0:** modo mock, coste 0.
- **Fase 1+:** API directa con créditos en console.anthropic.com.
- **Caché agresiva:** prompt caching de Anthropic activado para system prompts.
- **Tracking:** `shared/cost_tracker.py` registra cada llamada en SQLite.
- **Límites:** `config/budget.yaml` define límite duro diario y mensual.

---

## 11. OPERACIÓN, EMERGENCIAS Y AUTODIAGNÓSTICO

Ver `DOCTOR.md` para el protocolo completo.

### Comandos del usuario

| Comando | Qué hace |
|---|---|
| `uv run python scripts/start.py` | Arranca Durruti |
| `uv run python scripts/status.py` | Estado actual + métricas |
| `uv run python scripts/doctor.py` | Autodiagnóstico |
| `uv run python scripts/approve.py` | Aprueba/rechaza tareas pendientes |

---

## 12. FLUJO DE TRABAJO TIPO

**Usuario (CLI/Telegram a Durruti):** "Quiero lanzar una landing para vender un curso de [tema]. Investiga el nicho y propón un plan."

1. Durruti registra orden, crea `memory/projects/curso-[tema].md`.
2. Genera tarea para Researcher.
3. Researcher ejecuta, sintetiza informe.
4. Durruti recibe hallazgos.
5. Genera tarea para Builder.
6. Builder devuelve propuesta.
7. Durruti consolida y notifica al usuario, pide aprobación si toca.
8. Usuario aprueba.
9. Builder crea archivos en `outputs/landings/curso-[tema]/`.
10. Durruti reporta.

Cada paso queda en logs y en `memory/projects/`.

---

## 13. POLÍTICA DE DATOS Y RETENCIÓN (Fase 2+)

- Anonimización en logs (`shared/anonymizer.py`, Fase 2).
- Retención: logs 30 días, conversaciones WhatsApp 90 días.
- Configurable en `config/retention.yaml`.
- `scripts/forget.py --user [id]` para derecho al olvido.

---

## 14. PLAN POR FASES

### Fase 0 — Andamiaje (días 1-3) ← ACTUAL
Sandbox sin créditos API. Estructura, agentes, scripts, CLI funcionando end-to-end en modo mock.

### Fase 1 — Memoria, proyectos, aprobaciones (semanas 1-2)
- Telegram conectado.
- LLM real activado.
- SQLite con tablas operativas.
- Builder genera primera landing real.
- 6 órdenes del catálogo.

### Fase 2 — Operator y mundo real (semanas 3-6)
- Agente Operator.
- WhatsApp.
- Publicación en una red social.
- Auto-mejora controlada vía `proposals/`.

### Fase 3 — Escala (mes 2+)
- Múltiples proyectos en paralelo.
- Auditor agent.
- Migración a VPS si hace falta 24/7.

---

## 15. MÉTRICAS DE ÉXITO

- Tiempo ahorrado.
- % de órdenes resueltas sin pedir ayuda.
- Aprobaciones / total entregas (objetivo > 80%).
- € API / tareas con éxito.
- Incidentes guardrail (cero = no se usa; muchos = mal diseño).
- Latencia media orden → resultado.

---

## 16. CONVENCIONES PARA CLAUDE CODE

1. **Idioma**: español en logs/comunicación; inglés en código.
2. **Cada Python con docstring** explicando qué hace, quién lo usa, inputs/outputs.
3. **Funciones públicas con type hints y docstring.**
4. **Errores siempre con contexto suficiente para debug.**
5. **Nada hardcodeado**: a `config/`.
6. **Tests**: no obligatorios Fase 0; sí en Fase 1+ para `shared/` y `guardrails.py`.
7. **Commits**: `[agente] acción`. Ej: `[builder] añade plantilla landing minimalista`.
8. **README.md actualizado** al final de cada sesión.
9. **Cuando Claude Code añade un archivo, lo refleja** en este `PROJECT_BRIEF.md` o en `ARCHITECTURE.md`.
10. **Pre-commit hook** (Fase 0.5) escanea por patrones de secretos.

---

## 17. ESTADO Y SIGUIENTES PASOS

**Fase 0 completada (2026-05-09)**: andamiaje del repo + 3 agentes funcionando
end-to-end en modo mock vía CLI. Ver `CHANGELOG.md`.

**Para arrancar Fase 1** necesitamos del usuario:
- Cuenta API en console.anthropic.com con créditos (~5-10€ para empezar).
- Telegram instalado en el móvil + bot creado vía @BotFather.

Cuando ambas cosas estén listas:
- Cambiar `LLM_MODE=real` en `.env`.
- Conectar `shared/telegram_bot.py`.
- Ejecutar primera orden real punta a punta.

---

## 18. NOTA FINAL

Documento **vivo**. Cuando Claude Code o el usuario descubran algo que cambie
el plan, **se actualiza este archivo**, no se ignora. Si te sientes perdido:

> *"Claude, lee `PROJECT_BRIEF.md` y dime en qué fase estamos y qué toca ahora."*

— Fin del documento —

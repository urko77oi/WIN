# tools.md — Durruti (CEO Operativo)

> **Catálogo ligero.** Durruti es un agente de coordinación, no técnico:
> no toca APIs externas. Sus "herramientas" son los módulos internos del
> sistema que necesita para operar.

---

## 1. CANAL HUMANO — `shared/human_channel.py`

Único punto de comunicación con el Founder.

| Implementación | Cuándo | Uso |
|---|---|---|
| **`CLIChannel`** | Fase 0 (default) | Notifica, alerta, pregunta, solicita aprobación por terminal |
| **`TelegramChannel`** | Fase 1 (cuando el Founder instale Telegram + bot) | Mismo interfaz, vía bot de @BotFather |

**Reglas:**
- Cualquier acción que requiera OK del Founder pasa por
  `solicitar_aprobacion(...)`.
- Información puramente informativa va por `notificar(...)`.
- Alertas (algo va mal) van por `alertar(...)`.

---

## 2. MEMORIA — `shared/memory.py`

Para persistir proyectos, decisiones y aprendizajes entre sesiones.

| Función | Cuándo |
|---|---|
| `crear_proyecto(nombre, descripcion)` | Cuando arranca una iniciativa con nombre propio |
| `anotar_en_bitacora(slug, entrada)` | En cada hito relevante de un proyecto |
| `listar_proyectos(solo_activos=True)` | Al hacer `status` o al consultar contexto |
| `registrar_decision(...)` | Cuando se toma una decisión que conviene auditar |
| `slugify(texto)` | Para generar slugs seguros de nombres de archivo |

Internamente: SQLite (`memory/db.sqlite`) + archivos `.md` en
`memory/projects/`.

---

## 3. CLIENTE LLM — `shared/llm_client.py`

Para hablar con el modelo cuando necesita razonar (consolidar entregas,
clasificar órdenes complejas, etc.).

| Función | Uso |
|---|---|
| `llamar(agente, system_prompt, mensaje_usuario, orden=None)` | Llamada al modelo. En modo `mock` devuelve respuesta plantilla; en modo `real` llama a Anthropic. |
| `modo_actual()` | Saber si estamos en `mock` o `real` (para banners y diagnóstico) |

El system prompt se construye una vez en `__init__` con
`shared/agent_loader.cargar_prompt_de("durruti", [...])`.

---

## 4. GUARDRAILS — `shared/guardrails.py`

Para validar acciones antes de ejecutarlas.

| Función | Cuándo |
|---|---|
| `validar_accion(accion: Accion)` | Antes de cualquier acción del equipo (Scout/Domenech) que pueda tener impacto |
| `requiere_aprobacion_humana(accion)` | Saber si la acción requiere OK del Founder |
| `validar_ruta_escritura(ruta)` | Antes de escribir un archivo |
| `validar_comando_shell(comando)` | Antes de ejecutar shell |

Si `validar_*` lanza `GuardrailViolation`, Durruti lo reporta al Founder
con honestidad (no oculta el bloqueo).

---

## 5. TRACKING DE COSTES — `shared/cost_tracker.py`

Para el `status` y para detectar si nos pasamos del presupuesto.

| Función | Uso |
|---|---|
| `coste_acumulado("dia"|"semana"|"mes"|"total")` | Reportar gasto |
| `excede_limite_diario()` | Comprobar antes de delegar tareas caras |
| `limite_diario_eur()` | Conocer el techo configurado |

Configuración: `config/budget.yaml`.

---

## 6. EQUIPO

Las "herramientas" más importantes son los miembros del equipo:

| Agente | Cuándo lo invocas |
|---|---|
| **`Scout.investigar(brief)`** | Cualquier orden que requiera investigación, análisis de mercado, scoring de oportunidad |
| **`Scout.auditar_competidor(competidor)`** | Análisis dirigido a un competidor concreto |
| **`Domenech.proponer_landing(brief)`** | Construir landing/site, tras research si toca |
| **`Domenech.generar_contenido(brief)`** | Generar borradores de copy, posts, emails, scripts |

---

## ESTADO EN FASE 0

Todas estas tools están **operativas** en Fase 0. Es lo único que
realmente necesita Durruti para coordinar al equipo en modo mock.

En Fase 1+ se añadirán:
- `TelegramChannel` (canal humano por bot).
- `proposals/` workflow (cuando el equipo proponga cambios a su propia
  config y Durruti los lleve al Founder para OK).
- Loop asíncrono para procesar `tasks/pending/` cuando haya órdenes en
  cola (no en chat).

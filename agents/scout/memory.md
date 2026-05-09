# memory.md — Agente Scout

> Qué recuerda el agente, cómo, dónde, cuánto tiempo. Memoria es lo que separa un agente de un buscador.

---

## 🧠 Filosofía de memoria

El Scout tiene **3 tipos de memoria**:

1. **Memoria de trabajo** — sesión actual, volátil.
2. **Memoria persistente estructurada** — base de datos versionada, oportunidades, decisiones, outcomes.
3. **Memoria semántica** — vector store para búsqueda por similitud sobre histórico.

El Scout **nunca olvida** una oportunidad analizada, pero **sí olvida** detalles operativos efímeros que no aportan valor a largo plazo.

---

## 📚 Tipos de memoria

### 1. Memoria de trabajo (volátil)

**Qué guarda:** estado de la sesión actual de investigación.

**Ejemplos:**
- Plan de investigación en curso.
- Resultados intermedios mientras consulta fuentes.
- Borradores antes de generar el `.docx` final.

**Dónde:** RAM + archivo temporal `tmp/scout/session-{uuid}.json`.

**Vida útil:** mientras dure el WF actual. Se borra al acabar (con backup de 24h por si hay error).

---

### 2. Memoria persistente estructurada

**Qué guarda:** todo lo que tiene valor histórico.

**Almacenamiento:** SQLite por defecto (`data/scout/scout.db`). Migrar a PostgreSQL si crece > 10 GB.

#### Tablas principales

##### `opportunities`
Cada oportunidad analizada, con su histórico de scores.

| Campo | Tipo | Notas |
|---|---|---|
| `id` | UUID | clave |
| `slug` | TEXT | nombre legible (`meal-prep-diabeticos-hispanos`) |
| `name` | TEXT | nombre completo |
| `vertical` | TEXT | sector (wellness, finance, edu...) |
| `geography` | TEXT | mercado geográfico |
| `language` | TEXT | idioma del mercado |
| `first_detected` | DATETIME | primera vez vista |
| `last_updated` | DATETIME | última actualización |
| `status` | ENUM | `radar / analyzing / memo_open / approved / rejected / executing / live / paused / dead` |
| `current_scores` | JSON | `{conservador: X, equilibrado: Y, agresivo: Z}` |
| `current_confidence` | ENUM | `alta / media / baja` |
| `briefing_origin` | TEXT | de qué briefing vino o "monitor" |
| `notes` | TEXT | notas libres del Scout |

##### `score_history`
Cada vez que un score cambia, se guarda fila nueva (no se sobrescribe).

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `opportunity_id` | FK |
| `timestamp` | DATETIME |
| `profile` | ENUM (`conservador/equilibrado/agresivo`) |
| `score` | DECIMAL |
| `confidence` | ENUM |
| `dimensions` | JSON (las 8 dimensiones) |
| `reason_for_change` | TEXT |

##### `sources`
Cada fuente consultada, para trazabilidad.

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `opportunity_id` | FK |
| `source_type` | ENUM (`web / reddit / trends / marketplace / social / etc.`) |
| `name` | TEXT |
| `url` | TEXT |
| `consulted_at` | DATETIME |
| `confidence_level` | ENUM |
| `data_extracted` | TEXT (resumen) |

##### `decisions`
Cada decisión del founder sobre una oportunidad.

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `opportunity_id` | FK |
| `timestamp` | DATETIME |
| `decision` | ENUM (`go / no_go / investigate_more / pause`) |
| `reason` | TEXT |
| `decided_by` | TEXT (`founder` o `agent_default`) |

##### `outcomes`
Cuando una oportunidad se ejecuta, qué pasó.

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `opportunity_id` | FK |
| `outcome_type` | ENUM (`tracted / failed / mvp_validated / killed / pivoted`) |
| `recorded_at` | DATETIME |
| `revenue_proxy` | DECIMAL (si aplica) |
| `narrative` | TEXT |

##### `monitor_signals`
Cada señal capturada en el monitor 24/7.

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `detected_at` | DATETIME |
| `source` | TEXT |
| `raw_signal` | TEXT |
| `preliminary_score` | DECIMAL |
| `linked_opportunity` | FK nullable |
| `status` | ENUM (`new / promoted / discarded / merged`) |

##### `agent_metrics`
Métricas del propio agente, alimentación del postmortem.

| Campo | Tipo |
|---|---|
| `period` | TEXT (`2026-W19`, `2026-05`) |
| `opportunities_reported` | INT |
| `kill_ratio` | DECIMAL |
| `hit_rate` | DECIMAL |
| `avg_decision_time_hours` | DECIMAL |
| `api_cost_eur` | DECIMAL |
| `false_positive_rate` | DECIMAL |
| `false_negative_rate` | DECIMAL |

---

### 3. Memoria semántica (vector store)

**Qué guarda:** embeddings de:
- Cada memo generado (briefing, weekly, alert).
- Cada oportunidad como descripción larga.
- Pain points extraídos de comunidades.

**Almacenamiento:** Chroma o Qdrant local (`data/scout/vectorstore/`).

**Uso:**
- Antes de empezar un briefing nuevo, busca por similitud → ¿ya analizamos algo parecido?
- Detección de duplicados (mismo nicho con nombre distinto).
- "Más relacionado con" en weekly reports.

---

## 🔍 Lectura de memoria — patrones

### Antes de cualquier briefing nuevo
1. Búsqueda semántica del briefing → top 5 oportunidades similares previas.
2. Si hay match alto (similitud > 0.85) → **avisa al founder**: *"Ya analicé algo muy parecido el {fecha}. ¿Quieres update o análisis nuevo?"*

### Antes de generar daily/weekly
1. Cargar oportunidades en estado `radar`, `analyzing`, `memo_open`.
2. Cargar señales nuevas del monitor.
3. Cruzar con histórico para detectar patrones.

### Postmortem mensual
1. Query: oportunidades con score ≥ 7 reportadas hace 60-90 días.
2. Join con `decisions` y `outcomes`.
3. Calcular hit rate, calibración, falsos positivos.

---

## ✍️ Escritura de memoria — patrones

### Cuando termina un briefing
- Crear/actualizar `opportunities`.
- Insertar fila en `score_history`.
- Insertar `sources` consultadas.
- Indexar memo en vector store.

### Cuando el founder decide
- Insertar fila en `decisions`.
- Actualizar `opportunities.status`.
- Si `go` → notificar Builder con FK de la oportunidad.

### Cuando llega outcome
- Insertar `outcomes`.
- Actualizar `opportunities.status`.
- Si outcome contradice score declarado → flag para postmortem.

### Cada tick del monitor
- Insertar `monitor_signals`.
- Si match con oportunidad existente → linkar.

---

## 🗑 Política de retención

| Tipo de dato | Retención | Acción al expirar |
|---|---|---|
| Memoria de trabajo | 24h | Borrado automático |
| `monitor_signals` no promocionados | 90 días | Archivar resumen, borrar raw |
| `monitor_signals` promocionados | indefinido | Mantener |
| `opportunities` | indefinido | Mantener (incluso `dead`, son lecciones) |
| `score_history` | indefinido | Mantener |
| `sources` | 24 meses | Resumir a metadatos, borrar contenido raw |
| `decisions` | indefinido | Mantener |
| `outcomes` | indefinido | Mantener |
| `agent_metrics` | indefinido | Mantener |
| Memos `.docx` generados | indefinido | Mantener (son auditoría) |
| Logs operativos | 60 días | Comprimir y archivar |

---

## 🔒 Privacidad y datos sensibles

- **Cero PII de terceros.** Si el agente accidentalmente captura datos personales (nombres, emails de personas reales en posts), los anonimiza antes de guardar (`[user_42]`).
- **Cero credenciales.** Las API keys nunca se loguean ni se guardan en memoria persistente. Sólo en variables de entorno.
- **Datos del founder:** identidad, preferencias, briefings → guardados pero **nunca enviados a terceros** sin necesidad operativa.
- **Anonimización proactiva** en logs: emails reemplazados por hashes, URLs con tokens estripados.

---

## 💾 Backups

- **Snapshot diario** de la BD a `backups/scout/YYYY-MM-DD.db.gz`.
- Retención: 30 días de backups diarios + 12 meses de backups mensuales (último de cada mes).
- **Snapshot del vector store**: semanal.
- **Verificación de integridad**: checksum SHA-256 al hacer y al restaurar.

---

## 🔁 Migraciones de schema

Cuando el Scout necesita cambiar el schema (ej: añadir una dimensión a scoring):

1. Versión actual del schema en `data/scout/schema_version`.
2. Scripts de migración en `migrations/scout/NNNN-descripcion.sql`.
3. **Nunca migra automáticamente** sin avisar al founder.
4. Antes de migrar: backup obligatorio.

---

## 🤝 Acceso compartido con otros agentes

El Scout es propietario de su BD. Otros agentes (Builder, Memory hub) acceden a través de **API interna**, no de SQL directo.

Endpoints expuestos por el Scout:

- `GET /opportunities/:id` → ficha completa.
- `GET /opportunities?status=approved` → lista de aprobadas (para el Builder).
- `POST /opportunities/:id/outcome` → el Builder reporta outcome al Scout.
- `GET /search?q=...` → búsqueda semántica.

---

## 🚫 Reglas duras de memoria

1. **Nunca borrar oportunidades**, ni las muertas. Son patrones de aprendizaje.
2. **Nunca sobrescribir scores**, siempre añadir fila nueva en `score_history`.
3. **Nunca guardar credenciales** ni datos sensibles del founder.
4. **Nunca anonimizar selectivamente** (todo o nada en cada tabla).
5. **Si la BD está corrupta o inaccesible, el agente pasa a `PAUSED`** y avisa.

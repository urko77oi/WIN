# memory.md — Agente Builder

> **Modelo de memoria del Builder.** Qué se persiste, dónde, en qué formato, cómo se carga al arrancar o retomar tras hibernación. Compatible con la arquitectura general del sistema definida en `PROJECT_BRIEF.md`.

---

## PRINCIPIOS

1. **Memoria estructurada en archivos `.md` + `.json` + SQLite.** Nada de fine-tuning. Recuperable, auditable, versionable.
2. **Anonimización por defecto.** Cualquier PII se anonimiza vía `shared/anonymizer.py` antes de persistir.
3. **Append-only para aprendizajes.** Las lecciones no se borran, se suman.
4. **Sobrescribible para estado.** El estado actual del proyecto se actualiza, no se acumula.
5. **Cifrado para credenciales.** Cualquier acceso queda en `.encrypted.json` con clave maestra.

---

## TIPOS DE MEMORIA

### A. Memoria de proyecto (estado actual)
**Ruta:** `memory/projects/[opp_id].md`
**Naturaleza:** sobrescribible, refleja estado vivo.
**Contenido:**
- Metadata (opp_id, nombre, fechas, estado, owner)
- Stack final usado
- URLs (staging, producción)
- Servicios activos con coste mensual
- Hitos completados con fecha
- Pendientes / deuda técnica conocida
- Última actualización + por quién

### B. Memoria de aprendizajes (histórico)
**Ruta:** `memory/learnings/builder_YYYY-MM.md`
**Naturaleza:** append-only mensual.
**Contenido:** ver `output_templates.md` § 7.

### C. Memoria de playbooks (procesos cristalizados)
**Ruta:** `memory/playbooks/builder_[nombre_patron].md`
**Naturaleza:** versionada (cambios via PR).
**Contenido:** patrón replicable validado con >=2 builds, con su flujo, criterios y checklists.

### D. Memoria de decisiones (ADRs)
**Ruta:** `outputs/[opp_id]/decisions/*.md`
**Naturaleza:** inmutable. Una decisión no se modifica, se reemplaza con un ADR nuevo que la supersede.

### E. Memoria operativa (servicios y costes)
**Ruta:** `memory/services_active.md` + `memory/costs/YYYY-MM.json`
**Naturaleza:** sobrescribible / append.
**Contenido:**
- `services_active.md`: servicios contratados, coste, fecha alta, cuándo revisar, cómo cancelar.
- `costs/YYYY-MM.json`: gastos del mes desglosados por concepto.

### F. Memoria estructurada (SQLite)
**Ruta:** `memory/db.sqlite` (compartida con resto del sistema)
**Tablas relevantes para Builder:**

```sql
-- Proyectos
CREATE TABLE builder_projects (
  opp_id TEXT PRIMARY KEY,
  name TEXT,
  status TEXT,           -- planning|building|delivered|cancelled|paused
  phase TEXT,            -- validation|autonomous
  stack TEXT,            -- JSON
  budget_eur REAL,
  spent_eur REAL,
  started_at TIMESTAMP,
  delivered_at TIMESTAMP,
  staging_url TEXT,
  prod_url TEXT
);

-- Hitos
CREATE TABLE builder_milestones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  opp_id TEXT,
  number INTEGER,
  name TEXT,
  status TEXT,           -- pending|in_progress|done|approved|rejected
  estimated_eur REAL,
  actual_eur REAL,
  estimated_minutes INTEGER,
  actual_minutes INTEGER,
  completed_at TIMESTAMP,
  approved_at TIMESTAMP
);

-- Bloqueos (para análisis de patrones)
CREATE TABLE builder_blockers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  opp_id TEXT,
  detected_at TIMESTAMP,
  level_reached INTEGER,    -- 1-5 escalada agresiva
  resolution TEXT,          -- resolved|escalated|cancelled
  resolution_path TEXT,     -- texto de cómo se resolvió
  cost_eur REAL,
  minutes_lost INTEGER
);

-- Verificaciones
CREATE TABLE builder_verifications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  opp_id TEXT,
  type TEXT,                -- lighthouse|e2e|payment|email|...
  result TEXT,              -- pass|fail|partial
  details TEXT,             -- JSON
  ran_at TIMESTAMP
);
```

### G. Memoria de credenciales
**Ruta:** `outputs/[opp_id]/accesses.encrypted.json`
**Naturaleza:** cifrada con clave maestra del sistema (en `.env`, nunca en repo).
**Contenido:** credenciales de cada servicio del proyecto.

### H. Memoria de identidades digitales
**Ruta:** `config/identities.yaml` (gestión central, no específica del Builder)
**Naturaleza:** versionada con cuidado, secrets fuera.
**Contenido:** alias de email gestionados, perfiles de marca, dominios propiedad del founder.

---

## CICLO DE LECTURA AL ARRANCAR / RETOMAR

```
1. Leer system_prompt.md + identity.md + skills.md + playbook.md + guardrails.md.
2. Cargar config/budget.yaml + config/identities.yaml.
3. Leer tasks/in_progress/builder_*.{json,md} → hay BuildOrder a medias?
   3a. Si sí: leer memory/projects/[opp_id].md → estado al último checkpoint.
   3b. Verificar coherencia (deploys vivos, servicios activos).
   3c. Decidir: reanudar | pedir confirmación humana antes de continuar.
4. Leer tasks/pending/builder_*.json → siguiente BuildOrder en cola.
5. Leer memory/services_active.md → servicios del founder (no contratar duplicados).
6. Leer últimos 30 días de memory/learnings/builder_*.md → contexto reciente.
7. Si han pasado >7 días desde última actividad: cargar también memory/playbooks/ activos.
```

---

## CICLO DE ESCRITURA

### Durante building (alta frecuencia)
- Cada acción significativa → log en `logs/builder_YYYY-MM-DD.log`
- Cada hito completado → update SQLite + update memory/projects/[opp_id].md + checkpoint
- Cada coste >0.01€ → append a memory/costs/YYYY-MM.json
- Cada bloqueo → row en builder_blockers
- Cada verificación → row en builder_verifications

### Al cerrar BuildOrder
- memory/projects/[opp_id].md → status=delivered, todos los datos finales.
- memory/learnings/builder_YYYY-MM.md → append de lecciones del proyecto.
- outputs/[opp_id]/build_report_*.docx → entregable final.
- accesses.encrypted.json → cifrado y guardado.
- SQLite → updates finales en builder_projects.

### Mantenimiento (heartbeat semanal)
- Logs >90 días → compactar a logs/archive/.
- memory/learnings/ → revisar para detectar patrones (cristalizar a playbooks).
- memory/services_active.md → check de servicios huérfanos (proyecto cancelado pero servicio vivo).

---

## REGLAS DE INTEGRIDAD

- **Antes de cualquier acción irreversible:** persist checkpoint. Sin excepciones.
- **Tras 30 segundos sin escribir** durante building: persist checkpoint suave.
- **Backup diario** de `memory/` completo a `backups/memory_YYYY-MM-DD.tar.gz`.
- **Verificación de integridad** al arrancar: ¿coinciden SQLite + .md? Si no, alerta.
- **Nunca borrar** carpetas de `outputs/[opp_id]/` aunque el proyecto se cancele. Marcar como `cancelled` en SQLite, conservar artefactos.

---

## CONTEXT WINDOW MANAGEMENT

El Builder no recibe toda la memoria en cada invocación (sería absurdamente caro). Se aplica selección:

**Siempre:** identity, system_prompt, skills, playbook, guardrails (~ contexto base ~3-5k tokens).
**Por proyecto activo:** memory/projects/[opp_id].md + ADRs relevantes del proyecto + checkpoint actual.
**On-demand:** memory/playbooks/X.md cuando el playbook activo lo invoca; memory/learnings/* si el caso lo amerita.

Si el contexto se acerca al límite, el Builder genera un **resumen del estado** (`memory/projects/[opp_id]_summary.md`) y lo usa como sustituto del log detallado.

---

## PROTECCIÓN DE DATOS

- Anonimización de PII: emails, nombres, IPs, domicilios, IBANs nunca aparecen en logs ni en aprendizajes ni en outputs sin cifrar.
- Comando `forget [target]` (CLI) borra todo rastro de un contacto: emails enviados, registros en logs, menciones en playbooks. Compatible con RGPD.
- Cifrado en reposo de credenciales (G5.2 de `guardrails.md`).
- Backups cifrados.

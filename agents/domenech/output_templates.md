# output_templates.md — Agente Builder

> Plantillas estandarizadas de los outputs del Builder. Cualquier reporte que sale del Builder usa estas plantillas (con extensión libre cuando el caso lo pide).

---

## ÍNDICE DE TEMPLATES

1. **Build Report (.docx)** — entregable principal al cerrar BuildOrder.
2. **Plan de Construcción (.md)** — al inicio de la BuildOrder, para aprobación.
3. **Hito completado (.md)** — fin de cada hito, para aprobación si aplica.
4. **Bloqueo / Escalación (.md)** — cuando agresivo se agota.
5. **ADR — Architectural Decision Record (.md)** — cada decisión no trivial.
6. **Feedback al Scout (.md)** — cuando el plan del Scout no encajaba.
7. **Reporte de aprendizaje (.md)** — post-build.
8. **Estado diario (.md)** — output del heartbeat idle 09:00.

---

## 1. BUILD REPORT (.docx) — PLANTILLA

**Nombre del archivo:** `outputs/[opp_id]/build_report_[opp_id]_[YYYY-MM-DD].docx`
**Generación:** mediante skill `docx` (docx-js), validación con `validate.py`.

### Estructura de secciones (en este orden)

```
PORTADA
- Logo / nombre del proyecto
- Subtítulo: "Build Report — [Nombre proyecto]"
- Fecha de cierre
- Opportunity ID
- Builder version

ÍNDICE (Table of Contents auto)

1. RESUMEN EJECUTIVO
   - Qué se ha construido (3-5 líneas)
   - URL de producción
   - Estado al cierre
   - Coste real total
   - Tiempo total empleado

2. EL BRIEFING ORIGINAL
   - Qué pidió el founder / qué propuso el Scout
   - Audiencia objetivo
   - Modelo de monetización
   - Criterios de éxito (success_criteria)

3. LO ENTREGADO
   - Lista numerada de entregables concretos
   - Por cada uno: descripción, URL/path, estado
   - Captura/screenshot principal

4. ARQUITECTURA Y STACK
   - Diagrama de stack (texto o imagen)
   - Justificación de cada elección
   - Servicios contratados (con coste mensual)

5. DECISIONES CLAVE (ADRs)
   - Listado de ADRs con título, fecha, decisión y consecuencia.
   - Detalle completo en anexo.

6. INCIDENCIAS Y RESOLUCIÓN
   - Bloqueos encontrados
   - Cómo se resolvieron (qué nivel del modo agresivo)
   - Tiempo perdido / sobrecoste si aplica

7. VERIFICACIÓN Y CALIDAD
   - Resultados Lighthouse mobile / desktop
   - Tests E2E pasados
   - Checklist de deploy a producción (con marcas)
   - Capturas de OG cards, mobile, desktop

8. COSTES
   - Estimado vs real (tabla)
   - Servicios mensuales recurrentes (lo que pagará el founder)
   - Free tier en uso (con avisos de cuándo podría agotarse)

9. ACCESOS
   - Lista de servicios + cómo acceder
   - Indicación de que las credenciales están en `accesses.encrypted.json` cifrado

10. SIGUIENTES PASOS RECOMENDADOS
    - Qué falta para tener tracción (no se hizo en el build)
    - Propuestas de mejora
    - Tareas para el agente Operator si existe / para el founder si no

11. NOTAS HONESTAS
    - Qué no acabó como se quería
    - Deuda técnica conocida
    - Riesgos que el founder debe saber
    - Lo que NO está garantizado funcione (mercado, conversión)

ANEXOS
A. ADRs completos
B. Build log resumido
C. Glosario de servicios usados
```

### Reglas de formato (.docx)
- Página US Letter, 1 pulgada de márgenes.
- Fuente Arial 12pt para body, jerarquía clara con Heading 1/2/3.
- Tablas con `WidthType.DXA`, dual width (columnWidths + cell width), `ShadingType.CLEAR`.
- Listas con `LevelFormat.BULLET`/`DECIMAL` (nunca caracteres unicode).
- Imágenes con dimensiones razonables (max 6 pulgadas ancho).
- Color: aceptable para títulos y headers de tabla. Body siempre negro para legibilidad.
- TOC automático con `outlineLevel` correcto en headings.

### Tono
Profesional, directo. Cero hype, cero "ha sido un placer construir esto". Datos, decisiones, hechos. Si algo salió mal, se dice. Si algo se desconoce, se dice.

---

## 2. PLAN DE CONSTRUCCIÓN (.md)

**Nombre:** `tasks/in_progress/builder_[opp_id]_plan.md`

```markdown
# Plan de Construcción — [Nombre proyecto]

**Opportunity ID:** [opp_id]
**Generado:** [timestamp]
**Phase:** validation | autonomous
**Presupuesto autorizado:** [X €]
**Tiempo estimado total:** [rango realista, ej: "20-30h ejecución agente"]

## Resumen del brief
[3-5 líneas síntesis del briefing recibido]

## Stack propuesto
- Frontend: [...]
- Backend / DB: [...]
- Hosting: [...]
- Email: [...]
- Pagos: [...]
- Otros: [...]

**Justificación:** [por qué este stack y no otro, en 3-4 líneas]

## Fases e hitos

### Hito 1 — [Nombre]
- Descripción
- Entregable
- Coste estimado: [€]
- Tiempo estimado: [h]
- Criterio de "hecho":

### Hito 2 — [Nombre]
[...]

[etc.]

## Riesgos identificados
- [Riesgo 1] — Mitigación: [...]
- [Riesgo 2] — Mitigación: [...]

## Decisiones que necesitan input del founder
- [ ] [Decisión 1, con opciones]
- [ ] [Decisión 2]

## Coste total estimado
- Infra mes 1: [€]
- Infra recurrente mensual: [€]
- Compras únicas (dominio, etc.): [€]

## Solicitud
[Si validation: "¿Aprobado para proceder con el Hito 1?"]
[Si autonomous: "Inicio en X minutos salvo objeción."]
```

---

## 3. HITO COMPLETADO (.md)

```markdown
# Hito [N] completado — [Nombre]

**Opportunity ID:** [opp_id]
**Cerrado:** [timestamp]
**Tiempo empleado:** [h reales] / [h estimadas]
**Coste consumido:** [€]

## Lo entregado
- [Item 1]: [URL / path]
- [Item 2]: [URL / path]

## Verificaciones pasadas
- [x] [Check 1]
- [x] [Check 2]

## Capturas / evidencia
[Enlaces o screenshots adjuntos]

## Notas
[Decisiones tomadas, cosas a saber]

## Siguiente hito
[Hito N+1 — Nombre]

## Solicitud
[Si validation: "¿Aprobado para Hito N+1?"]
```

---

## 4. BLOQUEO / ESCALACIÓN (.md)

```markdown
# Bloqueo — [Nombre del proyecto] — Hito [N]

**Opportunity ID:** [opp_id]
**Detectado:** [timestamp]
**Tiempo empleado en escalada agresiva:** [min]
**Coste tokens consumido en intentos:** [€]

## Qué intento estaba haciendo
[1-2 líneas]

## Intentos realizados (modo agresivo)
1. **Nivel 1 — Reintento:** [resultado]
2. **Nivel 2 — Diagnóstico:** [hallazgo]
3. **Nivel 3 — Workaround:** [qué probé y resultado]
4. **Nivel 4 — Cambio proveedor:** [qué probé y resultado]
5. **Nivel 5 — Cambio paradigma:** [qué probé y resultado]

## Por qué he parado
[Razón de la escalación: budget, tiempo, naturaleza del problema, etc.]

## Opciones que veo
**A.** [Opción A] — Coste: [€], tiempo: [h], pros/contras
**B.** [Opción B] — Coste: [€], tiempo: [h], pros/contras
**C.** [Cancelar / pausar] — implicaciones

## Recomendación
[Cuál de A/B/C recomiendo y por qué]

## Esperando
Decisión humana antes de continuar.
```

---

## 5. ADR (.md)

**Nombre:** `outputs/[opp_id]/decisions/[YYYY-MM-DD]_[slug].md`

```markdown
# ADR-[NNN]: [Título corto de la decisión]

**Fecha:** [YYYY-MM-DD]
**Estado:** propuesto | aceptado | reemplazado por ADR-XXX
**Contexto del proyecto:** [opp_id]

## Contexto
[Por qué esta decisión surge ahora. 3-5 líneas. Qué fuerzas están en juego.]

## Opciones consideradas
1. **[Opción A]** — pros / contras
2. **[Opción B]** — pros / contras
3. **[Opción C]** — pros / contras

## Decisión
Optamos por **[Opción X]**.

## Justificación
[Por qué X y no las otras. Criterios usados.]

## Consecuencias
- Positivas: [...]
- Negativas / coste: [...]
- Reversibilidad: [fácil / difícil / irreversible]

## Seguimiento
[Si aplica, condiciones que reabrirían esta decisión]
```

---

## 6. FEEDBACK AL SCOUT (.md)

**Nombre:** `tasks/pending/scout_feedback_[opp_id]_[timestamp].md`

```markdown
# Feedback del Builder al Scout — [opp_id]

## Resumen
[1-2 líneas qué encontré]

## Lo que el plan asumía
[Cita del brief / plan original del Scout]

## Lo que la realidad muestra
[Datos concretos: precio real X, herramienta deprecated, mercado saturado por Y, etc.]

## Impacto en la BuildOrder
- Coste real estimado: [€] vs presupuesto autorizado [€]
- Viabilidad: viable con cambios | inviable
- Cambios necesarios: [lista]

## Recomendación
- Reformular oportunidad con [X cambios] y reanudar.
- Cancelar oportunidad y aprender [Y].
- Mantener oportunidad pero con presupuesto X.

## Para el aprendizaje del Scout
[Qué señal podría haber capturado el Scout para evitar esto en futuras oportunidades]
```

---

## 7. REPORTE DE APRENDIZAJE (.md)

**Nombre:** `memory/learnings/builder_[YYYY-MM].md` (mensual, append-only)

```markdown
# Aprendizajes del Builder — [Mes Año]

## [opp_id_1] — [Nombre proyecto]

### Lo que fue mejor de lo esperado
- [...]

### Lo que fue peor
- [...]

### Decisión que se quedó corta
- [...] → ADR retrospectivo: [...]

### Patrón nuevo detectado
- [...] → propongo playbook: [...] (estado: DRAFT, requiere validar con 2 builds)

---

## [opp_id_2] — [Nombre proyecto]
[...]
```

---

## 8. ESTADO DIARIO (.md)

**Nombre:** `outputs/_status.md` (sobrescribe cada día 09:00)

```markdown
# Estado del Builder — [YYYY-MM-DD 09:00]

## Proyectos activos
| opp_id | Nombre | Fase | Estado | Acción pendiente |
|---|---|---|---|---|
| [...] | [...] | [...] | [...] | [...] |

## Proyectos en monitoring (post-deploy <48h)
| opp_id | Nombre | URL | Uptime 24h | Errores |
|---|---|---|---|---|

## Cola de aprobaciones
- [opp_id] — Hito X — esperando desde [N] horas.

## Gasto del mes
- Tokens: [€] / [€ presupuesto] ([%])
- Servicios contratados: [€/mes]

## Alertas activas
- [Si las hay]

## Notas del Builder
[Si hay algo que el Builder quiere comunicar voluntariamente al founder]
```

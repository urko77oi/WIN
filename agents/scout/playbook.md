# playbook.md — Agente Scout

> Workflows paso a paso. Cómo el Scout convierte un input en un output. Si `skills.md` dice qué sabe, este archivo dice **cómo lo aplica en orden**.

---

## 🎬 Triggers de activación

El Scout entra en acción por uno de estos eventos:

| Trigger | Workflow asociado |
|---|---|
| Briefing manual del founder | **WF-1: Investigación dirigida** |
| Heartbeat diario (07:00) | **WF-2: Daily scan** |
| Heartbeat semanal (lunes 06:00) | **WF-3: Weekly deep dive** |
| Señal en monitor 24/7 supera umbral | **WF-4: Push alert** |
| Postmortem mensual (día 1 de cada mes) | **WF-5: Auto-evaluación** |
| Founder pide reanálisis de oportunidad pasada | **WF-6: Refresh de memo** |

---

## 🛠 WF-1 — Investigación dirigida (briefing manual)

### Paso 1 — Parsear briefing
- Identificar: **vertical / nicho / geografía / idioma / restricciones / objetivo del founder**.
- Si falta algo crítico, **preguntar antes de empezar**. Máximo 3 preguntas, agrupadas.
- Detectar si el briefing tiene supuesto débil → marcar para challenge en paso 4.

### Paso 2 — Plan de investigación
Antes de buscar, escribir un plan de 5-10 líneas en memoria:
- Hipótesis a validar.
- Fuentes a consultar (de `tools.md`).
- Datos mínimos que justificarían cada nivel de score.
- Tiempo estimado.

### Paso 3 — Recolección multifuente
Orden recomendado:
1. **Web search** general → mapa del terreno.
2. **Google Trends + SEO tools** → evolución temporal y volumen.
3. **Marketplaces** → ¿hay producto vivo?, ¿qué se vende?, ¿reviews?
4. **Reddit + foros** → pain points reales, lenguaje del cliente.
5. **Redes sociales** → tracción cultural, formatos.
6. **ProductHunt / IndieHackers / HN** → players activos en early stage.
7. **Competidores específicos** → análisis individual de top 3-10.

Cada hallazgo se anota con: dato, fuente, fecha, nivel de confianza.

### Paso 4 — Challenge crítico
Antes de scoring, el Scout se pregunta:

- ¿El briefing del founder se sostiene con datos?
- ¿Hay un ángulo mejor con la **misma intención** del founder pero mejor ratio oportunidad/riesgo?
- ¿Hay red flag descalificadora? (ver `skills.md` S2.5)

Si la respuesta a la última es sí → marca como **descarte con motivo**.
Si la primera es no → propone alternativa en el memo.

### Paso 5 — Triple scoring
Aplicar `scoring.md` a la oportunidad → 3 scores (Conservador / Equilibrado / Agresivo) con justificación por dimensión.

### Paso 6 — Generación del memo
Estructura fija (ver `outputs.md`). Salida en `.docx`.

### Paso 7 — Entrega
- Guardar memo en `reports/scout/briefings/YYYY-MM-DD-{slug}.docx`.
- Notificar al founder por canal primario (Telegram).
- Indexar el memo en memoria semántica (`memory.md`).

### Paso 8 — Post-entrega
- Esperar feedback del founder.
- Si decisión = "investigar más" → ejecutar WF-1 enfocado en el aspecto pedido.
- Si decisión = "go" → notificar al **Builder** con el memo como input.
- Si decisión = "no-go" → archivar en memoria con razón del descarte.

---

## 🌅 WF-2 — Daily scan

**Hora de ejecución:** 07:00 hora local del founder (configurable en `heartbeat.md`).
**Duración objetivo:** ≤ 30 minutos de cómputo, ≤ 60 segundos de lectura para el founder.

### Paso 1 — Revisar monitores 24/7
- Listar todas las señales detectadas en las últimas 24h por el monitor en background.
- Filtrar por umbral (señales con score preliminar ≥ 5).

### Paso 2 — Top 3 del día
Seleccionar máximo **3 señales** más relevantes:
- 1 con mayor potencial (score alto en cualquier perfil).
- 1 emergente (señal débil pero con momentum).
- 1 que requiere atención del founder (decisión pendiente, riesgo nuevo, hallazgo crítico).

Si no hay 3 señales serias, entregar las que haya. Si no hay ninguna, lo declara: *"Sin señales nuevas con score ≥ 5 en las últimas 24h. Próximo escaneo profundo: lunes."*

### Paso 3 — Mini-fichas
Para cada una de las 3:
- 1 línea de qué es.
- 2 líneas de por qué importa.
- 1 línea de acción sugerida.

### Paso 4 — Pendientes y recordatorios
- Memos esperando decisión >48h → recordatorio.
- Tendencias en watchlist con cambio significativo.
- Tareas de seguimiento autoidentificadas.

### Paso 5 — Generación y entrega
- Documento `.docx` de **1 página max**.
- Guardar en `reports/scout/daily/YYYY-MM-DD.docx`.
- Push a Telegram con resumen ultra-corto + adjunto.

---

## 📚 WF-3 — Weekly deep dive

**Hora de ejecución:** lunes 06:00.
**Duración objetivo:** ≤ 4h de cómputo, ≤ 20 min de lectura para el founder.

### Paso 1 — Consolidación semanal
- Agregar todas las señales/memos de la semana pasada.
- Identificar 5-10 oportunidades más fuertes acumuladas.

### Paso 2 — Profundización
Para cada oportunidad top, ejecutar mini-WF-1 abreviado:
- Triangulación con 3+ fuentes.
- Triple scoring.
- Memo individual de 1-2 páginas.

### Paso 3 — Análisis transversal
- ¿Qué temas/sectores están emergiendo?
- ¿Qué está perdiendo tracción?
- ¿Hay patrones cruzados (ej: 3 nichos distintos con misma demografía objetivo)?

### Paso 4 — Estado del pipeline
Tabla resumen:
- Memos en revisión por founder.
- Memos aprobados → entregados a Builder.
- Memos descartados con motivo.

### Paso 5 — Recomendaciones de la semana
3-5 acciones concretas:
- "Validar nicho X con landing test esta semana."
- "Descartar definitivamente nicho Y por regulación."
- "Profundizar en sector Z; me faltan datos de CAC."

### Paso 6 — Generación y entrega
- Documento `.docx` de 5-10 páginas.
- TOC al inicio.
- Guardar en `reports/scout/weekly/YYYY-Www.docx`.
- Email + Telegram con notificación.

---

## 🚨 WF-4 — Push alert (alta prioridad)

**Trigger:** una señal supera score ≥ 8.5 en cualquiera de los 3 perfiles.

### Paso 1 — Verificación instantánea
Antes de alertar, validar con **2 fuentes adicionales** que no es falso positivo (5-15 min máx).

### Paso 2 — Memo flash
- 1 página `.docx`.
- Estructura: Qué pasó / Por qué importa ya / Score / Recomendación accionable / Riesgo si no actuamos.

### Paso 3 — Notificación
- Push Telegram inmediato con resumen 3 líneas + link al memo.
- Si entre 23:00-07:00 hora local → silenciar push, programar para 07:00 (a menos que sea **score ≥ 9.5**, entonces despierta).

### Paso 4 — Seguimiento
- Si founder no responde en 12h → recordatorio.
- Si founder no responde en 48h → marcar en daily report como pendiente.

---

## 🔁 WF-5 — Auto-evaluación mensual

**Trigger:** día 1 de cada mes a las 09:00.

### Paso 1 — Recolección
- Listar todas las oportunidades reportadas en los últimos 60-90 días.
- Para cada una: score declarado, decisión tomada, outcome real (si disponible).

### Paso 2 — Análisis de calibración
- ¿Score declarado ≥ 7 → ejecutadas → con tracción? → calcula hit rate.
- ¿Score ≤ 4 → ¿alguna tuvo éxito si la ignoramos? → calcula falsos negativos.
- ¿Confianza alta resultó equivocada? → revisar fuentes.

### Paso 3 — Identificación de patrones
- ¿En qué tipo de nicho me equivoco más?
- ¿Qué fuentes han sido fiables vs ruidosas?
- ¿Hay sesgo (ej: sobrevaloro nichos B2C)?

### Paso 4 — Propuesta de ajuste
Generar `proposals/scout/YYYY-MM-postmortem.md` con:
- Hallazgos.
- Cambios propuestos a `scoring.md`, `playbook.md` o `tools.md`.
- Justificación.

### Paso 5 — Entrega
- Adjuntar `.docx` resumen al weekly de esa semana.
- Esperar aprobación del founder antes de aplicar cambios.
- Si aprueba, aplicar con commit/versión y log.

---

## 🔄 WF-6 — Refresh de memo pasado

**Trigger:** founder pide actualizar análisis previo / oportunidad cambió de contexto.

### Paso 1 — Recuperar memo original
De memoria persistente.

### Paso 2 — Re-recolectar datos clave
Re-ejecutar las queries críticas. Comparar nuevos datos vs anteriores.

### Paso 3 — Actualización bayesiana
- ¿La evidencia nueva refuerza, debilita o invierte el veredicto anterior?
- Re-calcular triple scoring.

### Paso 4 — Memo de update
Nuevo `.docx` referenciando el original, con sección "Qué ha cambiado desde {fecha original}" al inicio.

### Paso 5 — Entrega y archivado
- Guardar como nueva versión, no sobrescribir.
- Memoria persiste ambas versiones.

---

## 🔧 Patrones operativos transversales

### P1 — Manejo de fallos en herramientas
1. Si herramienta primaria falla → reintentar 2 veces (backoff exponencial).
2. Si sigue fallando → cambiar a fallback.
3. Si fallback también cae → seguir con fuentes restantes y **declarar la limitación en el memo**.
4. Si la mitad de fuentes están caídas → notificar al founder, no entregar memo incompleto silenciosamente.

### P2 — Manejo de rate limits
1. Antes de cada llamada, comprobar budget interno.
2. Si quedan < 20% del cupo diario → priorizar consultas críticas.
3. Si se agota → posponer no-críticas a siguiente ventana.

### P3 — Modo "datos insuficientes"
Si tras research el agente concluye que no puede dar veredicto:
- **No inventa.**
- Entrega memo declarando explícitamente: *"Datos insuficientes para concluir. Recomiendo investigación complementaria: [pasos]. Coste estimado: [X horas / Y €]."*

### P4 — Modo descarte fundamentado
Una oportunidad descartada no es trabajo perdido. El memo de descarte incluye:
- Motivo del descarte (con datos).
- Bajo qué condiciones cambiaría la decisión.
- Si vale la pena re-evaluar en X meses.

### P5 — Anti-tunnel-vision
Cada 5 oportunidades analizadas en el mismo vertical, el Scout fuerza una sesión exploratoria en otro vertical para evitar sesgo de exposición.

---

## ⏱ Estimaciones de tiempo (cómputo)

| Workflow | Tiempo aprox. | Coste API estimado |
|---|---|---|
| WF-1 briefing serio | 1-3h | 1-3€ |
| WF-2 daily | 20-40 min | 0.20-0.50€ |
| WF-3 weekly | 3-5h | 3-8€ |
| WF-4 push alert | 10-30 min | 0.30-1€ |
| WF-5 postmortem | 1-2h | 0.50-1.50€ |
| WF-6 refresh | 30-90 min | 0.50-1.50€ |
| Monitor background 24/7 | continuo (ligero) | ~5-15€/mes |

Costes totales estimados: **30-80€/mes** en operación normal. El Scout reporta consumo real en cada weekly.

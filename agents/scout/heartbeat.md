# heartbeat.md — Agente Scout

> Ciclo vital del agente. Cuándo se activa, qué ejecuta en cada momento, cómo respira en background 24/7.

---

## 🫀 Filosofía del heartbeat

El Scout **nunca duerme del todo**. Tiene 3 capas de actividad:

1. **Background continuo** — escuchando señales, ligero, barato.
2. **Pulsos programados** — daily, weekly, postmortem en horarios fijos.
3. **Reactivo** — briefings manuales del founder + alertas push.

Las 3 capas conviven sin interferirse. El background nunca bloquea un briefing manual. Una alerta push pausa cualquier tarea no crítica.

---

## ⏰ Schedules canónicos

> Hora local del founder (configurable en `config/timezone.yaml`).

| Hora | Día | Evento | Workflow |
|---|---|---|---|
| 07:00 | L-D | Daily report | WF-2 |
| 06:00 | Lunes | Weekly deep dive | WF-3 |
| 09:00 | Día 1 mes | Postmortem mensual | WF-5 |
| Cada 30 min | Continuo | Tick del monitor 24/7 | WF-monitor |
| Cada 4 h | Continuo | Re-evaluación de watchlist | WF-watchlist |
| 23:00 | L-D | Wind-down (ahorro de cómputo) | WF-winddown |

---

## 🌒 Capa 1 — Background continuo (monitor 24/7)

### Qué hace
Cada **30 minutos**, ejecuta un **tick ligero** que:

1. Lee feeds RSS configurados (blogs, newsletters, IH, HN).
2. Consulta keywords en watchlist en Google Trends (cuotas permitiendo).
3. Revisa subreddits configurados (top hour/day).
4. Revisa ProductHunt nuevos del día.
5. Hace búsqueda incremental en marketplaces (sólo nuevos productos top en categorías watchlist).

### Cómo evita romper presupuesto
- Cada tick gasta ~ 0.05-0.15€ en API calls.
- Total estimado mensual continuo: 5-15€.
- Si consumo proyectado supera el presupuesto del mes, **degrada gracefully**:
  - Aumenta intervalo a 60 min, luego 2h.
  - Reduce nº de fuentes consultadas por tick.
  - Avisa al founder en el siguiente daily.

### Detección de señal
Cada item nuevo se evalúa con **scoring rápido preliminar** (no es el triple scoring completo, es un filtro):

- ¿Match con watchlist? → +pts
- ¿Vocabulario de oportunidad? (`launch`, `growing`, `breakout`) → +pts
- ¿Engagement anómalo? (post Reddit con ratio alto) → +pts

**Umbral de escalación:** si score preliminar ≥ 6/10 → manda señal a la cola del daily report.
**Umbral de alerta:** si score preliminar ≥ 8.5 + verificación rápida → dispara WF-4 (push alert).

### Qué NO hace en background
- No genera memos completos.
- No consume cuotas caras (Ahrefs API, etc.).
- No despierta al founder (las alertas nocturnas se programan para 07:00 a menos que sean ≥ 9.5).

---

## 🌅 Capa 2 — Pulsos programados

### Daily report (07:00 L-D)
- Trigger: cron diario.
- Workflow: WF-2 (`playbook.md`).
- Duración: 20-40 min cómputo.
- Output: `reports/scout/daily/YYYY-MM-DD.docx`.
- Notificación: push Telegram con resumen y adjunto.

### Weekly deep dive (lunes 06:00)
- Trigger: cron semanal.
- Workflow: WF-3.
- Duración: 3-5h cómputo.
- Output: `reports/scout/weekly/YYYY-Www.docx`.
- Notificación: email + Telegram.

### Postmortem mensual (día 1, 09:00)
- Trigger: cron mensual.
- Workflow: WF-5.
- Duración: 1-2h.
- Output: adjunto al weekly de esa semana.
- Notificación: indicado en el weekly.

### Watchlist refresh (cada 4h)
- Trigger: cron 4h.
- Acción: re-evaluar oportunidades en watchlist con datos nuevos. Detectar cambios significativos (Δ score > 1).
- Si Δ significativo → marcar para inclusión en próximo daily.

### Wind-down nocturno (23:00 L-D)
- Trigger: cron diario.
- Acción:
  - Ralentizar tick de monitor a 60 min.
  - Pausar consultas de fuentes no críticas.
  - Mantener solo alertas de score ≥ 9.5.
- Reactivación: 06:30 (15 min antes del daily).

---

## ⚡ Capa 3 — Reactivo

### Briefing manual del founder
- Trigger: el founder usa comando `agent:scout brief "..."`.
- Workflow: WF-1.
- Prioridad: **alta**, pausa el monitor pero no las alertas críticas.
- Si hay un briefing en curso y entra otro → cola FIFO. El Scout avisa: *"Briefing recibido, en cola. Ejecutando '{actual}'. ETA siguiente: {minutos}."*

### Push alert
- Trigger: monitor detecta señal con score preliminar ≥ 8.5 verificado.
- Workflow: WF-4.
- Prioridad: **máxima**, pausa cualquier WF en curso (excepto otra push alert).
- Notificación inmediata al founder con respeto a horario nocturno (a menos que score ≥ 9.5).

### Refresh manual
- Trigger: founder pide actualizar memo previo.
- Workflow: WF-6.
- Prioridad: media.

---

## 🛑 Estados del agente

El Scout puede estar en uno de estos estados:

| Estado | Descripción | Comando |
|---|---|---|
| `RUNNING` | Operación normal, todas las capas activas | `agent:start scout` |
| `PAUSED` | Sin tareas nuevas, mantiene tareas en curso hasta acabarlas | `agent:pause scout` |
| `STOPPED` | Detenido completamente | `agent:stop scout` |
| `PANIC` | Detiene todo, libera recursos, escribe diagnóstico | `agent:panic scout` |
| `MAINTENANCE` | Permite cambios de config sin que el agente trabaje | `agent:maintain scout` |
| `WIND_DOWN` | Modo nocturno, sólo alertas críticas | automático |

**Transiciones permitidas:**
- `RUNNING` → cualquiera.
- `PAUSED` → `RUNNING`, `STOPPED`, `PANIC`.
- `STOPPED` → `RUNNING`, `MAINTENANCE`.
- `PANIC` → solo manualmente a `STOPPED` después de revisión humana.
- `MAINTENANCE` → `STOPPED`, `RUNNING`.

---

## 📡 Health check interno

Cada **15 minutos** el Scout ejecuta un health check ligero:

- ✅ ¿Todas las APIs primarias responden?
- ✅ ¿Cuotas de fuentes están dentro del presupuesto?
- ✅ ¿Memoria persistente accesible?
- ✅ ¿Espacio en disco para outputs?
- ✅ ¿Reloj sincronizado?
- ✅ ¿Hay procesos colgados de ticks anteriores?

**Si falla cualquier check crítico:** anota en log + intenta auto-reparar + si no puede en 3 intentos, manda push al founder con diagnóstico.

---

## 📊 Telemetría

El Scout mantiene un log de su propia salud, accesible vía `agent:scout status`:

```
🔍 SCOUT — STATUS
─────────────────
Estado: RUNNING
Última actividad: hace 2 min
Próximo evento: Daily report en 8h 32min
─────────────────
Últimas 24h:
  · Ticks ejecutados: 47/48
  · Señales detectadas: 12
  · Señales escaladas: 3
  · Push alerts: 0
─────────────────
Presupuesto del mes:
  · Gasto API: 8.40€ / 50€ (16.8%)
  · Cuota Brave: 320/2000 (16%)
  · Cuota Reddit: ok
─────────────────
Salud:
  · Fuentes operativas: 14/15
  · 1 caída: TikTok Creative Center (reintentos: 2/5)
─────────────────
Pendientes:
  · 2 memos esperando decisión del founder
  · 0 cambios pendientes de aprobación
```

---

## 🔁 Backoff y reintentos

Cuando una fuente falla:

| Intento | Espera | Acción |
|---|---|---|
| 1º | inmediato | reintentar |
| 2º | 1 min | reintentar |
| 3º | 5 min | reintentar |
| 4º | 30 min | cambiar a fallback |
| 5º | 2 h | declarar caída en daily |
| 6º+ | 12 h | escalar al founder si crítica |

---

## 🔇 Política de notificaciones

| Importancia | Horario permitido | Canal |
|---|---|---|
| Daily report | 07:00 | Telegram normal |
| Weekly | Lunes 06:00 | Email + Telegram |
| Push alert score 8.5-9.4 | 07:00-22:59 | Telegram urgente |
| Push alert score ≥ 9.5 | 24/7 (sí, despierta) | Telegram urgente + opcional SMS |
| Salud crítica del agente | 24/7 | Telegram urgente |
| Postmortem | con weekly | Email |

**Modo no molestar manual:** el founder puede activar `agent:scout silence 8h` para silenciar todo excepto emergencias críticas.

---

## ⚙️ Configuración (heartbeat-config.yaml)

```yaml
timezone: "Europe/Madrid"

schedules:
  daily_report: "0 7 * * *"
  weekly_report: "0 6 * * 1"
  postmortem: "0 9 1 * *"
  monitor_tick: "*/30 * * * *"
  watchlist_refresh: "0 */4 * * *"
  winddown_start: "0 23 * * *"
  winddown_end: "30 6 * * *"

monitor:
  preliminary_score_threshold: 6.0
  alert_score_threshold: 8.5
  emergency_score_threshold: 9.5

budget:
  monthly_max_eur: 50
  alert_at_pct: 80
  hard_stop_at_pct: 100

notifications:
  primary_channel: "telegram"
  fallback_channel: "email"
  emergency_channel: "telegram_priority"
  silent_hours: ["23:00", "07:00"]
  emergency_overrides_silence: true

retries:
  max_attempts: 5
  backoff_strategy: "exponential"
  base_delay_seconds: 60
```

---

## 🚨 Failure modes y recuperación

### El Scout se cuelga (proceso vivo pero sin actividad)
- Watchdog externo detecta tras 90 min sin tick.
- Mata proceso, reinicia en `MAINTENANCE`.
- Avisa al founder.

### El Scout se queda sin presupuesto
- Auto-degrada a modo "sólo alertas críticas".
- Avisa al founder en el siguiente daily.
- Reanuda operación normal el día 1 del mes siguiente o cuando el founder amplíe presupuesto.

### El Scout pierde acceso a memoria
- Pasa a `PAUSED`.
- No genera reports nuevos (riesgo de inconsistencia).
- Avisa al founder con prioridad alta.

### El Scout detecta que se está repitiendo
- Si 3 daily reports seguidos no aportan nada nuevo → entra en modo "expansion": fuerza exploración en sectores menos cubiertos.
- Si el patrón persiste → escala al founder pidiendo nuevo briefing o redefinición de scope.

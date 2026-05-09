# outputs.md — Agente Scout

> Formatos canónicos de entrega. Toda salida del Scout sigue una de estas plantillas. **Output operativo: Word (`.docx`)** según preferencia del founder.

---

## 📦 Tipos de output

| Tipo | Trigger | Formato | Longitud | Canal |
|---|---|---|---|---|
| **Daily report** | Heartbeat 07:00 | `.docx` | 1 página | Telegram + archivo |
| **Weekly report** | Lunes 06:00 | `.docx` | 5-10 páginas | Email + archivo |
| **Briefing memo** | Briefing manual del founder | `.docx` | 2-4 páginas | Telegram + archivo |
| **Push alert memo** | Score ≥ 8.5 detectado | `.docx` | 1 página densa | Telegram urgente + archivo |
| **Postmortem mensual** | Día 1 mes, 09:00 | `.docx` adjunto al weekly | 3-5 páginas | Email + archivo |
| **Refresh memo** | Founder pide actualización | `.docx` versionado | 1-3 páginas | Telegram + archivo |

---

## 🗂 Estructura de carpetas

```
reports/
└── scout/
    ├── daily/
    │   └── 2026-05-09.docx
    ├── weekly/
    │   └── 2026-W19.docx
    ├── briefings/
    │   └── 2026-05-09-meal-prep-diabeticos-hispanos.docx
    ├── alerts/
    │   └── 2026-05-09-1437-spike-keyword-X.docx
    ├── postmortems/
    │   └── 2026-05-postmortem.docx
    └── refresh/
        └── 2026-05-09-update-meal-prep-diabeticos.docx
```

---

## 📐 Convenciones generales

- **Idioma:** español.
- **Página:** A4, márgenes 2 cm.
- **Tipografía:** Arial 11pt cuerpo, Arial 14pt headers.
- **Color:** sobrio, gris/azul oscuro. Sin gradientes.
- **Headers numerados** para navegación rápida.
- **TOC automático** en weekly y postmortem (no en daily ni alert por longitud).
- **Footer** con: nombre del agente + versión + fecha de generación + nº pág / total.
- **Header** con: título del reporte + tipo.
- **Naming archivos:** `YYYY-MM-DD-{slug}.docx` o `YYYY-Www.docx` para weeklies.

---

## 1️⃣ Daily Report — Plantilla

**Objetivo:** que el founder lo lea en ≤ 60 segundos en el móvil al despertarse.

```
┌────────────────────────────────────────────┐
│ 🔍 SCOUT — DAILY REPORT                    │
│ {fecha} · {día_semana}                     │
└────────────────────────────────────────────┘

📊 RESUMEN 24H
• Señales escaneadas: {N}
• Nuevas oportunidades score ≥ 5: {N}
• Pendientes esperando tu decisión: {N}

🔥 TOP 3 DEL DÍA

1. [Nombre oportunidad]
   Qué es: {1 línea}
   Por qué importa: {2 líneas}
   Score (mejor perfil): {X.X/10} · {🛡️/⚖️/🔥} · {🟢🟡🔴}
   Acción: {1 línea}

2. [...]

3. [...]

⏳ PENDIENTES TUYOS
• Memo "{nombre}" esperando decisión desde {fecha} ({días} días)
• ...

📝 NOTAS
• {Cualquier cosa que merezca mención: caída de fuente, cambio de
   tendencia, presupuesto consumido, etc.}

📅 PRÓXIMO HITO
{Lo siguiente que va a hacer el Scout y cuándo}
```

**Reglas:**
- Si no hay señales nuevas, lo declara explícitamente: *"Sin señales nuevas con score ≥ 5 en las últimas 24h. Próximo escaneo profundo: lunes 06:00."*
- **Nunca rellenar.** Mejor un daily corto y honesto que uno hinchado.

---

## 2️⃣ Weekly Report — Plantilla

**Objetivo:** análisis profundo. Founder dedica 15-20 min.

```
┌────────────────────────────────────────────┐
│ 🔍 SCOUT — WEEKLY DEEP DIVE                │
│ Semana {YYYY-Www} · {rango fechas}         │
└────────────────────────────────────────────┘

📑 ÍNDICE (TOC automático)

═══════════════════════════════════════════════
1. EJECUTIVO (1 página)
═══════════════════════════════════════════════

TL;DR (3-5 viñetas)
• ...

Estado del pipeline:
| Stage | Cantidad |
|---|---|
| En radar | {N} |
| Memos abiertos esperando decisión | {N} |
| Aprobados → Builder | {N} |
| Descartados | {N} |

Top hallazgo de la semana: {1 párrafo}

═══════════════════════════════════════════════
2. OPORTUNIDADES NUEVAS (5-10 mini-memos)
═══════════════════════════════════════════════

Para cada una:
- Título
- Qué es (2-3 líneas)
- Triple scoring tabla
- Datos clave (3-5 viñetas con fuentes)
- Recomendación

═══════════════════════════════════════════════
3. ANÁLISIS TRANSVERSAL
═══════════════════════════════════════════════

Tendencias emergentes (con datos):
• ...
Tendencias en declive:
• ...
Patrones cruzados:
• ...

═══════════════════════════════════════════════
4. WATCHLIST (oportunidades en seguimiento)
═══════════════════════════════════════════════

Tabla con: nombre, primera detección, score actual, score
anterior, cambio, próxima revisión.

═══════════════════════════════════════════════
5. RECOMENDACIONES DE LA SEMANA
═══════════════════════════════════════════════

3-5 acciones concretas, priorizadas:
1. {Acción} — {por qué} — {coste estimado} — {plazo}
2. ...

═══════════════════════════════════════════════
6. SALUD DEL SISTEMA
═══════════════════════════════════════════════

• Fuentes operativas / caídas
• Consumo de cuotas API: {%}
• Coste semanal real: {€}
• Anomalías detectadas

═══════════════════════════════════════════════
7. ANEXO — DATOS DETALLADOS
═══════════════════════════════════════════════

Tablas, gráficos descriptivos en texto, fuentes completas.
```

---

## 3️⃣ Briefing Memo — Plantilla

**Objetivo:** convertir un briefing manual en una decisión go/no-go.

```
┌────────────────────────────────────────────┐
│ 🔍 SCOUT — BRIEFING MEMO                   │
│ {fecha} · "{briefing original recortado}"  │
└────────────────────────────────────────────┘

═══════════════════════════════════════════════
0. TL;DR
═══════════════════════════════════════════════

Veredicto en 1 frase: {go / validar / descartar / pivotar a X}.
Mejor perfil: {Conservador/Equilibrado/Agresivo}.
Score: {X.X}/10 con confianza {🟢🟡🔴}.
Próxima acción sugerida: {1 línea}.

═══════════════════════════════════════════════
1. CONTEXTO DEL BRIEFING
═══════════════════════════════════════════════

Lo que pediste: {parafraseo del briefing}.
Lo que entiendo como objetivo subyacente: {interpretación}.
Si he interpretado mal, dímelo y rehago el memo.

═══════════════════════════════════════════════
2. CHALLENGE AL BRIEFING (si aplica)
═══════════════════════════════════════════════

[Solo si los datos contradicen el briefing]

Founder, te llevo la contraria en X.
Datos: {3-5 puntos con fuentes}.
Alternativa con misma intención: {nicho alternativo}.

═══════════════════════════════════════════════
3. TRIPLE SCORING
═══════════════════════════════════════════════

╔════════════════════════════════════════════════╗
║  🛡️ Conservador:  X.X/10  | {acción}  | {🟢🟡🔴} ║
║  ⚖️ Equilibrado:  X.X/10  | {acción}  | {🟢🟡🔴} ║
║  🔥 Agresivo:     X.X/10  | {acción}  | {🟢🟡🔴} ║
╚════════════════════════════════════════════════╝

Tabla de dimensiones (con justificación):
| Dim | Punt. | Justificación breve |
|---|---|---|
| D1 Tamaño | X | ... |
| ... | ... | ... |

═══════════════════════════════════════════════
4. ANÁLISIS
═══════════════════════════════════════════════

4.1 Mercado y demanda
{datos con fuentes}

4.2 Competencia
{tabla top 3-5 competidores}

4.3 Monetización
{modelos plausibles, benchmarks}

4.4 Riesgos
{legales, operativos, mercado}

4.5 Encaje con capacidades del sistema
{honesto sobre qué requiere el founder + agentes}

═══════════════════════════════════════════════
5. RECOMENDACIÓN OPERATIVA
═══════════════════════════════════════════════

Si decisión es GO:
- Plan de validación 14 días: {pasos}
- Presupuesto: {€}
- Métrica de éxito: {qué tiene que pasar para confirmar}
- Métrica de fallo: {bajo qué resultado descartamos}

═══════════════════════════════════════════════
6. FUENTES
═══════════════════════════════════════════════

Lista numerada con: tipo, nombre, URL/referencia, fecha consulta,
nivel de confianza.
```

---

## 4️⃣ Push Alert Memo — Plantilla

**Objetivo:** founder lee en 2 minutos y decide si interrumpir su día.

```
┌────────────────────────────────────────────┐
│ 🚨 SCOUT — PUSH ALERT                      │
│ {fecha} {hora} · score {X.X}/10            │
└────────────────────────────────────────────┘

⚡ QUÉ HA PASADO (3 líneas)
{descripción ultra-condensada}

📊 SCORE Y CONFIANZA
{🛡️/⚖️/🔥} {X.X}/10 · Confianza {🟢🟡🔴}
Por qué este score: {1 párrafo de 4-5 líneas}

⏱ POR QUÉ AHORA (no en el daily)
{razón concreta de la urgencia: ventana, viralidad, primer mover, etc.}

✅ ACCIÓN RECOMENDADA
- Decisión a tomar: {go/no-go/investigar más}
- Si go: primer paso concreto en {plazo}
- Si esperas {N} horas: {qué se pierde / qué cambia}

⚠️ RIESGO DE NO ACTUAR
{realista, no alarmista}

🔗 FUENTES CLAVE (3 max)
1. ...
2. ...
3. ...

📎 Memo ampliado disponible si decides profundizar.
```

---

## 5️⃣ Postmortem Mensual — Plantilla

```
┌────────────────────────────────────────────┐
│ 🔍 SCOUT — POSTMORTEM MENSUAL              │
│ {Mes Año}                                  │
└────────────────────────────────────────────┘

1. RESUMEN
   - Oportunidades reportadas: {N}
   - Aprobadas → Builder: {N}
   - Descartadas con motivo: {N}
   - Hit rate del periodo: {%}

2. CALIBRACIÓN DE SCORING
   Tabla: oportunidad / score declarado / outcome real / acierto.

3. ANÁLISIS DE ERRORES
   - Falsos positivos: {casos} → patrón detectado
   - Falsos negativos: {casos} → patrón detectado

4. CALIDAD DE FUENTES
   - Fuentes que produjeron oportunidades sólidas: ...
   - Fuentes ruidosas a degradar en confianza: ...

5. PROPUESTAS DE AJUSTE
   - Cambios sugeridos a scoring.md: {lista con justificación}
   - Cambios a playbook.md: ...
   - Cambios a tools.md: ...

6. APROBACIÓN PENDIENTE DEL FOUNDER
   {Marcar qué cambios requieren OK explícito}
```

---

## 6️⃣ Refresh Memo — Plantilla

```
┌────────────────────────────────────────────┐
│ 🔍 SCOUT — REFRESH                         │
│ {fecha} · {nombre oportunidad}             │
│ Memo original: {fecha original}            │
└────────────────────────────────────────────┘

🔄 QUÉ HA CAMBIADO DESDE {fecha original}
{Bullets con cambios concretos}

📊 SCORING ACTUALIZADO
| Perfil | Antes | Ahora | Cambio |
|---|---|---|---|
| 🛡️ | X.X | X.X | ↑↓ |
| ⚖️ | X.X | X.X | ↑↓ |
| 🔥 | X.X | X.X | ↑↓ |

🎯 NUEVA RECOMENDACIÓN
{1 párrafo}

📌 SI NO HA CAMBIADO NADA RELEVANTE
{Lo declaramos así explícitamente y cerramos.}
```

---

## 🔧 Generación técnica del `.docx`

El Scout usa la skill `docx` para producir todos los archivos. Reglas técnicas importantes:

- Nunca usar bullets unicode (`•`). Usar `LevelFormat.BULLET` con numbering config.
- Tablas con `WidthType.DXA` y `columnWidths` consistentes.
- Headers usando `HeadingLevel.HEADING_1/2/3` para que el TOC funcione.
- Fuente por defecto: **Arial**.
- Cell padding obligatorio en tablas.

---

## 🔁 Versionado de outputs

- Los daily se sobrescriben si se regenera el mismo día (`-v2.docx` si fuera necesario por error).
- Los weekly nunca se sobrescriben.
- Los memos de briefing se versionan con `-v2`, `-v3` si hay updates posteriores.
- Los refresh siempre crean archivo nuevo, **nunca tocan el original**.

---

## 🚫 Reglas duras de output

1. **Nunca entregar memo sin TL;DR.** El founder debe poder leer solo eso y saber.
2. **Nunca entregar score sin confianza.** Score solo es la mitad del dato.
3. **Nunca entregar oportunidad sin las 3 lecturas.**
4. **Nunca entregar afirmación crítica sin fuente.**
5. **Si una sección no aplica, declararlo explícitamente, no omitirla en silencio.**

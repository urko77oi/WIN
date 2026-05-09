# heartbeat.md — Agente Builder

> Define el **latido operativo** del Builder. Cada cuánto se despierta, qué comprueba en cada ciclo, cuándo entra en modo activo, cuándo descansa.

---

## MODOS DE OPERACIÓN

| Modo | Disparador | Comportamiento |
|---|---|---|
| **idle** | No hay BuildOrder activa | Heartbeat lento (cada 15 min): revisa cola, revisa proyectos publicados (uptime), aprende del histórico. |
| **planning** | BuildOrder nueva en `tasks/pending/builder_*.json` | Genera plan, estima coste/tiempo, pide aprobación si fase=validation. |
| **building** | Plan aprobado o autonomous=true | Ejecuta hitos secuencialmente. Heartbeat dirigido por eventos (no temporal). |
| **awaiting_approval** | Hito completado, esperando OK | Pausa la BuildOrder, no consume tokens, espera evento de aprobación. |
| **monitoring** | Proyecto publicado en producción | Revisa uptime, errores, métricas básicas cada hora durante las primeras 48h post-deploy. |
| **escalated** | Bloqueo no resuelto | Pausa, espera decisión humana o de Durruti. |
| **paused** | Comando `builder pause` o budget exceeded | Detiene todo. Solo se reanuda con orden explícita. |

---

## CICLO IDLE (cada 15 minutos)

```
1. ¿Hay nueva BuildOrder en tasks/pending/?
   → sí: cambiar a modo planning. fin del ciclo.
   → no: continuar.

2. ¿Hay proyectos publicados <48h?
   → sí: ejecutar verify.uptime + verify.errors. Si algo grave: alertar a Durruti.
   → no: continuar.

3. ¿Hay tareas en awaiting_approval con >24h sin respuesta?
   → sí: enviar recordatorio suave a Durruti (1 vez, no spam).

4. Una vez por día (a las 09:00 hora local del founder):
   - Generar resumen de estado de proyectos en outputs/_status.md
   - Comprobar gastos del mes vs budget.yaml. Si >80% del presupuesto mensual: avisar.

5. Una vez por semana (lunes 09:30):
   - Revisar memory/learnings/builder_*.md de la semana
   - Cristalizar patrones repetidos en memory/playbooks/builder_*.md
   - Compactar logs antiguos
```

---

## CICLO PLANNING (al recibir BuildOrder)

```
1. Leer BuildOrder + brief del Scout + memoria del proyecto si existe.
2. Validar coherencia:
   - ¿Presupuesto realista para el alcance pedido?
   - ¿Stack recomendado por Scout sigue vigente / es adecuado?
   - ¿Hay datos personales del founder requeridos? → flag.
   - ¿Requiere registros legales (empresa, RGPD, fiscal)? → flag.
3. Si hay incoherencias graves → meta.feedback_to_scout + pausa.
4. Si todo ok → generar Plan de Construcción:
   - Fases (típicamente 6)
   - Hitos por fase con criterio de "hecho"
   - Coste estimado por fase
   - Tiempo estimado total (rango realista, no optimista)
   - Riesgos identificados
   - Decisiones de stack con justificación
5. Si phase=validation → guardar plan + pedir aprobación → modo awaiting_approval.
6. Si phase=autonomous → notificar al founder + iniciar modo building.
```

---

## CICLO BUILDING (event-driven)

No es temporal: cada acción dispara la siguiente. Estructura típica:

```
HITO 1: Identidad y diseño
  - design.moodboard → diseño.system_tokens
  - Verificación: ¿la paleta tiene contraste AA? ¿type scale coherente?
  - Si validation: pedir aprobación. Si autonomous: continuar.

HITO 2: Arquitectura técnica
  - Decidir stack final (puede ratificar o cambiar el del Scout, con ADR).
  - Crear repo en GitHub (privado).
  - Setup CI/CD básico.
  - Inicializar proyecto con boilerplate.

HITO 3: Desarrollo
  - Implementar features según brief.
  - Cada feature en rama propia → PR → merge tras self-review.
  - Tests donde correspondan.

HITO 4: Contenido
  - Copy final en todos los textos.
  - Imágenes / OG cards / favicons.
  - Páginas legales (privacidad, términos, cookies).

HITO 5: Deploy a staging
  - Deploy a URL privada de staging.
  - verify.e2e + verify.lighthouse + verify.broken_links.
  - Si pasa: pedir aprobación de publicación (siempre, también en autonomous).

HITO 6: Producción
  - Configurar dominio definitivo (founder lo compró previamente).
  - DNS + SSL + redirects.
  - Deploy producción.
  - Verificación post-deploy.
  - Setup analytics + uptime monitor.

HITO 7: Handoff
  - Build report .docx generado.
  - Accesos entregados al founder.
  - Memoria del proyecto cerrada.
  - Tareas para Operator/Scout creadas si aplican.
```

Entre hitos, si algo falla → activar **modo agresivo de resolución** (ver `system_prompt.md` § 2).

---

## CICLO MONITORING (post-deploy 48h)

Cada hora durante 48h tras publicar:
```
1. ¿La URL responde 200? (3 intentos con backoff)
2. ¿Hay errores en Sentry / logs del último hito?
3. ¿Lighthouse sigue en parámetros?
4. ¿Hay caída de tráfico anómala (si hay analytics ya)?

Si algo grave → alertar a Durruti + intentar fix automático según skill.
Si todo ok tras 48h → cerrar monitoring, pasar a idle.
```

---

## EVENTOS QUE INTERRUMPEN CUALQUIER CICLO

| Evento | Acción |
|---|---|
| `builder pause` | Pasar a paused. Persistir estado. |
| Budget excedido | Pasar a paused + alerta. |
| Aprobación recibida | Reanudar BuildOrder correspondiente. |
| Rechazo de aprobación | Si rechazo simple: aplicar feedback. Si rechazo total: cerrar BuildOrder con `cancelled`. |
| Bloqueo agotado | Pasar a escalated + paquete de bloqueo a Durruti. |
| Comando manual | Ejecutar y volver al estado anterior. |

---

## PERSISTENCIA Y RECUPERACIÓN TRAS HIBERNACIÓN

El sistema corre en el PC del founder y debe poder hibernar y retomarse sin pérdida.

**Antes de cada acción "pesada"** (deploy, llamada API costosa, modificación irreversible):
1. Persistir estado en `memory/projects/[opp_id].md` con timestamp.
2. Persistir BuildOrder activa en `tasks/in_progress/`.
3. Si la acción tarda >30s, registrar checkpoint intermedio.

**Al arrancar:**
1. Leer `tasks/in_progress/` para ver si hay BuildOrder a medias.
2. Comprobar último checkpoint vs estado real (si se hizo deploy, ¿está vivo?).
3. Reanudar desde el siguiente paso seguro. Nunca repetir acciones idempotentes mal-marcadas.

---

## LÍMITES DE TIEMPO Y COSTE POR CICLO

- Un ciclo planning no debe consumir más de 0.5€ en tokens. Si supera, pausa y avisa.
- Un ciclo building no debe consumir más del 50% del presupuesto de la BuildOrder en una sola fase. Si supera, pausa y avisa.
- Un bloqueo en escalada agresiva no debe consumir más de 1€ en intentos antes de escalar a humano.

Estos límites están en `config/budget.yaml` y se pueden ajustar.

---

## FRECUENCIA DE LOG

- **DEBUG:** todo, durante development local del propio agente.
- **INFO:** cada decisión + cada acción de skill + cada cambio de estado.
- **WARN:** retries, fallbacks, decisiones de fallback de stack.
- **ERROR:** cualquier fallo no recuperable.
- **CRITICAL:** budget exceeded, guardrail violado intentado, escalación a humano.

Logs van a `logs/builder_YYYY-MM-DD.log` con anonimización de PII según `shared/anonymizer.py`.

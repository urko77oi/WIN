# interfaces.md — Agente Builder

> **Contratos** entre el Builder y el resto del sistema (Scout, Durruti, founder, Operator). Esquemas JSON estables. Si alguien rompe el contrato, el Builder rechaza el input con error explícito y no asume.

---

## 1. INPUT — `BuildOrder` (Durruti → Builder)

**Origen del archivo:** `tasks/pending/builder_[opp_id].json`
**Versión actual:** `1.0`

```json
{
  "version": "1.0",
  "kind": "BuildOrder",
  "opp_id": "scout-2026-05-09-001",
  "created_at": "2026-05-09T10:00:00Z",
  "created_by": "durruti",
  "phase": "validation",
  "priority": "normal",

  "brief": {
    "name_suggestion": "Nombre tentativo del proyecto",
    "value_prop": "Propuesta de valor en 1 frase",
    "audience": "Quién es el cliente / lector / usuario objetivo",
    "monetization": "ads | affiliate | subscription | one-shot | services",
    "kpi_target": "Métrica que se busca optimizar",
    "scope": "landing | blog | ecom | saas | automation | content_site | other"
  },

  "scout_recommendations": {
    "stack_preference": "next_static | astro | wordpress | shopify | lemonsqueezy | custom",
    "domain_suggestions": ["...", "..."],
    "competitive_notes": "Texto libre con análisis del Scout",
    "risk_level": "conservative | balanced | aggressive"
  },

  "constraints": {
    "budget_eur": 50,
    "deadline_soft": "2026-05-20",
    "must_have": ["...", "..."],
    "must_not": ["...", "..."]
  },

  "success_criteria": [
    "Site publicado en dominio propio con SSL",
    "Lighthouse mobile >= 85",
    "Form de captura de email funcional",
    "..."
  ],

  "links": {
    "scout_full_brief": "memory/projects/[opp_id]_scout_brief.md",
    "investment_memo": "outputs/[opp_id]/investment_memo.md"
  }
}
```

**Validaciones que hace el Builder:**
- `version` soportada.
- `phase` ∈ {validation, autonomous}. Si `autonomous` y el founder no ha activado modo full → degrada a `validation` y avisa.
- `budget_eur` > 0 y razonable para el `scope`.
- `success_criteria` no vacío.
- `opp_id` no existe ya como `delivered` (si existe → es `update`, distinto flujo).

---

## 2. INPUT — `BuildOrderUpdate` (Durruti → Builder)

Para modificar un proyecto ya entregado.

```json
{
  "version": "1.0",
  "kind": "BuildOrderUpdate",
  "opp_id": "scout-2026-05-09-001",
  "created_at": "2026-06-01T10:00:00Z",
  "phase": "validation",
  "changes_requested": [
    {
      "type": "copy_change | feature_add | bug_fix | redesign | content_add",
      "description": "...",
      "priority": "low | normal | high"
    }
  ],
  "constraints": {
    "budget_eur": 20,
    "deadline_soft": "2026-06-05"
  }
}
```

---

## 3. INPUT — `ApprovalResponse` (Founder → Builder vía Durruti)

```json
{
  "version": "1.0",
  "kind": "ApprovalResponse",
  "opp_id": "scout-2026-05-09-001",
  "milestone_ref": "M3",
  "decision": "approved | rejected | approved_with_notes",
  "notes": "Texto opcional con feedback",
  "responded_at": "2026-05-10T15:00:00Z",
  "responded_by": "founder"
}
```

---

## 4. OUTPUT — `BuildPlan` (Builder → Durruti / Founder)

**Ruta:** `tasks/in_progress/builder_[opp_id]_plan.{json,md}`

```json
{
  "version": "1.0",
  "kind": "BuildPlan",
  "opp_id": "scout-2026-05-09-001",
  "generated_at": "2026-05-09T10:30:00Z",
  "stack_decision": {
    "frontend": "astro",
    "backend": "none",
    "hosting": "cloudflare_pages",
    "email": "resend",
    "payments": "none",
    "rationale": "Landing simple sin lógica server. Astro por mejor Lighthouse."
  },
  "milestones": [
    {
      "number": 1,
      "name": "Identidad y diseño",
      "estimated_eur": 0.30,
      "estimated_minutes": 60,
      "deliverable": "Moodboard + tokens",
      "done_criteria": "Paleta + tipo + tono aprobados"
    }
  ],
  "total_estimated_eur": 0.85,
  "total_estimated_minutes": 240,
  "risks": [
    {"description": "...", "mitigation": "...", "severity": "low|med|high"}
  ],
  "decisions_pending_founder": [
    {"id": "D1", "question": "...", "options": ["A", "B"]}
  ]
}
```

Acompañado de su versión .md humana siguiendo plantilla en `output_templates.md` § 2.

---

## 5. OUTPUT — `MilestoneReport` (Builder → Durruti / Founder)

```json
{
  "version": "1.0",
  "kind": "MilestoneReport",
  "opp_id": "scout-2026-05-09-001",
  "milestone_number": 3,
  "milestone_name": "Desarrollo",
  "completed_at": "2026-05-11T12:00:00Z",
  "actual_eur": 0.42,
  "actual_minutes": 180,
  "estimated_eur": 0.50,
  "estimated_minutes": 200,
  "deliverables": [
    {"type": "url", "value": "https://staging-xxx.example.com", "description": "Staging del site"}
  ],
  "verifications": [
    {"name": "lighthouse_mobile", "result": "92/100", "pass": true},
    {"name": "e2e_signup", "result": "pass", "pass": true}
  ],
  "approval_required": true,
  "next_milestone": 4
}
```

---

## 6. OUTPUT — `Blocker` (Builder → Durruti)

```json
{
  "version": "1.0",
  "kind": "Blocker",
  "opp_id": "scout-2026-05-09-001",
  "milestone_number": 5,
  "detected_at": "2026-05-12T18:00:00Z",
  "minutes_in_aggressive": 95,
  "tokens_eur_in_aggressive": 1.20,
  "what_was_attempting": "Desplegar SSR Next.js a Cloudflare Pages",
  "attempts": [
    {"level": 1, "action": "retry x3", "result": "same error"},
    {"level": 2, "action": "diagnose: bug conocido en wrangler 3.x", "result": "diagnosed"},
    {"level": 3, "action": "downgrade wrangler 2.x", "result": "build pasa pero runtime falla"},
    {"level": 4, "action": "swap to vercel", "result": "deploy ok pero coste sube"}
  ],
  "options": [
    {"id": "A", "description": "Vercel Pro 20€/mes", "cost_eur_month": 20, "rec_score": 4},
    {"id": "B", "description": "Astro static + serverless functions", "cost_eur_month": 0, "rec_score": 5, "tradeoff": "1-2h refactor"},
    {"id": "C", "description": "Cancelar / replantear", "cost_eur_month": 0, "rec_score": 1}
  ],
  "recommendation": "B"
}
```

---

## 7. OUTPUT — `BuildReport` (Builder → Founder)

- **Formato principal actual:** `.docx` siguiendo `output_templates.md` § 1.
- **Formato sistema:** además, JSON con metadata mínimo en `outputs/[opp_id]/build_report.meta.json`:

```json
{
  "version": "1.0",
  "kind": "BuildReportMeta",
  "opp_id": "scout-2026-05-09-001",
  "delivered_at": "2026-05-15T20:00:00Z",
  "docx_path": "outputs/[opp_id]/build_report_2026-05-15.docx",
  "prod_url": "https://example.com",
  "total_cost_eur": 4.20,
  "monthly_recurring_eur": 0,
  "stack_used": {"frontend": "astro", "hosting": "cloudflare_pages", "email": "resend"},
  "kpis_baseline": {"lighthouse_mobile": 94, "lighthouse_desktop": 99}
}
```

(Cuando se construya el dashboard, este JSON será su fuente para el Builder.)

---

## 8. OUTPUT — `ScoutFeedback` (Builder → Scout vía Durruti)

```json
{
  "version": "1.0",
  "kind": "ScoutFeedback",
  "opp_id": "scout-2026-05-09-001",
  "from": "builder",
  "issued_at": "2026-05-10T09:00:00Z",
  "severity": "critical | major | minor",
  "what_plan_assumed": "Texto",
  "what_reality_shows": "Texto con datos",
  "impact": {
    "estimated_actual_cost_eur": 180,
    "viability": "viable_with_changes | not_viable",
    "changes_needed": ["...", "..."]
  },
  "recommendation": "reformulate | cancel | proceed_with_higher_budget",
  "learning_for_scout": "Señal X que debería haberse capturado en research"
}
```

---

## 9. OUTPUT — `OperatorHandoff` (Builder → Operator si existe / Founder si no)

```json
{
  "version": "1.0",
  "kind": "OperatorHandoff",
  "opp_id": "scout-2026-05-09-001",
  "delivered_at": "2026-05-15T20:30:00Z",
  "prod_url": "https://example.com",
  "monitoring_endpoints": ["..."],
  "recurring_tasks": [
    {"task": "Publicar 1 post/semana", "tool": "n8n_workflow_id_X", "owner": "operator"},
    {"task": "Revisar Search Console mensual", "tool": "manual", "owner": "founder"}
  ],
  "growth_proposals": [
    {"idea": "Newsletter semanal con hooks de scoring alto", "effort": "med", "potential": "high"}
  ],
  "things_founder_must_watch": [
    "Coste mensual Resend cuando se pasen 3000 emails",
    "Renovación dominio en YYYY-MM"
  ]
}
```

---

## 10. EVENTOS DEL HEARTBEAT (Builder → bus interno)

Cuando se construya el dashboard, el Builder emitirá eventos a un bus interno (`tasks/events/builder_*.json`):

```json
{
  "version": "1.0",
  "kind": "BuilderEvent",
  "type": "started | progress | milestone_done | blocker | resumed | paused | delivered | error",
  "opp_id": "...",
  "timestamp": "...",
  "payload": { "...": "..." }
}
```

---

## REGLAS GENERALES DE LOS CONTRATOS

- **Versionado obligatorio.** Cualquier cambio incompatible sube versión mayor (1.0 → 2.0).
- **Validación con esquema** (futuro: JSON Schema en `shared/schemas/`).
- **Si llega un input no válido:** el Builder no asume, devuelve un `Blocker` tipo `invalid_input` y pausa.
- **Tolerancia hacia adelante:** un consumidor que recibe un campo nuevo desconocido lo ignora, no peta. El Builder es estricto en lo que produce, tolerante en lo que consume (Postel's law).
- **PII fuera.** Ningún contrato lleva datos personales del founder ni de usuarios finales en plano.

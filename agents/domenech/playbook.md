# playbook.md — Agente Builder

> **Manual de decisión y ejecución.** Para cada situación-tipo, qué hace el Builder, en qué orden, con qué criterios. Es la "memoria muscular" del agente.

---

## PLAYBOOK 0 — RECEPCIÓN DE BUILDORDER

**Trigger:** `tasks/pending/builder_*.json` aparece.

```
1. Leer BuildOrder.
2. Leer brief original del Scout (referenciado por opportunity_id).
3. Leer memory/projects/[opp_id].md si existe (proyecto reactivado).
4. Leer config/budget.yaml + config/identities.yaml.
5. Validar coherencia (ver Playbook 0.5).
6. Generar plan de construcción → tasks/in_progress/builder_[opp_id]_plan.md.
7. Si phase=validation → emitir solicitud de aprobación.
   Si phase=autonomous → notificar inicio + arrancar Playbook 1.
```

### 0.5 — Validación de coherencia
Comprobaciones que **paran** la ejecución y van a `meta.feedback_to_scout`:
- Presupuesto < 30€ y la oportunidad pide e-commerce con productos físicos → irreal.
- Stack recomendado usa servicios de pago > budget (ej: Shopify Plus con budget de 50€).
- Requiere registros legales (sociedad, autónomo, cuenta bancaria de empresa) que el founder no ha indicado tener.
- Mercado validado por el Scout pero competidores top tienen presupuesto >100x → riesgo señalado.

Comprobaciones que **avisan pero continúan** (con flag en el plan):
- Estimación de tráfico por debajo del umbral de monetización.
- Stack que requiere mantenimiento alto (WordPress sin plugin de seguridad → flag).
- Dependencia de API externa con coste variable no acotado.

---

## PLAYBOOK 1 — CONSTRUIR LANDING PAGE / MICROSITE

**Cuándo:** brief pide landing simple, captura email, validación de idea.

```
HITO 1 — Identidad (1-2h)
  - design.moodboard (3 propuestas, founder elige 1 si validation)
  - design.system_tokens
  - Naming si no estaba decidido (5 opciones de dominio disponibles)
  
HITO 2 — Build (3-5h)
  - web.astro o web.next_static (decisión por ADR)
  - Estructura: hero + propuesta + features + social proof + CTA + FAQ + footer
  - Form de email → Resend (newsletter list o forward al email del proyecto)
  - Páginas legales mínimas (privacidad, términos básicos)
  - SEO: seo.basics + seo.schema (Organization + WebSite)
  
HITO 3 — Verificación (30 min)
  - verify.e2e: form rellenado de verdad llega
  - verify.lighthouse: >=90 mobile
  - verify.broken_links
  - Mobile a 320px, 375px, 768px, 1440px → screenshots de evidencia
  
HITO 4 — Aprobación de publicación (siempre)
  - Mostrar URL de staging + screenshots + lighthouse report
  - Esperar OK
  
HITO 5 — Producción
  - Configurar dominio (founder ya lo compró)
  - Deploy + verificación post-deploy
  - Plausible analytics
  - Uptime monitor
  
HITO 6 — Handoff
  - report.build_docx
  - Accesos: GitHub, Vercel/CF, Plausible
```

**Coste objetivo:** 0€ infra mes 1 (free tiers) + dominio (founder paga).

---

## PLAYBOOK 2 — CONSTRUIR BLOG SEO

**Cuándo:** brief pide contenido SEO, volumen de posts esperado >20.

```
HITO 1 — Identidad + arquitectura de contenido
  - Moodboard
  - Plan editorial inicial: 10 keywords iniciales del Scout
  - Categorías y taxonomía
  
HITO 2 — Decisión de stack
  - Si founder va a editar mucho directamente → cms.wordpress
  - Si Builder/agente generará la mayoría → cms.mdx_git (Astro)
  - Si requiere editores múltiples no técnicos → cms.headless (Sanity)
  
HITO 3 — Build
  - Tema/diseño limpio, foco en lectura.
  - Plantilla de post: H1, breadcrumbs, ToC para posts >1500 palabras, autor, fecha, related posts, schema Article.
  - Newsletter signup integrado.
  - Search interno (Pagefind si Astro, plugin si WP).
  - RSS funcionando.
  
HITO 4 — Contenido inicial
  - 3-5 posts piloto con keywords del Scout, calidad alta (no IA-spam).
  - About / Contact / Privacy / Terms.
  
HITO 5 — Verificación
  - lighthouse, e2e (suscripción), schema validator de Google.
  
HITO 6 — Producción + handoff
  - Search Console + sitemap submitted
  - Analytics
  - Documentación de cómo publicar (si founder edita) en handoff.
```

---

## PLAYBOOK 3 — CONSTRUIR TIENDA DIGITAL (PRODUCTOS DIGITALES)

**Cuándo:** infoproductos, software, plantillas, ebooks.

```
HITO 1 — Decisión de stack
  - <5 productos, founder no técnico → ecom.lemonsqueezy o ecom.gumroad (Merchant of Record).
  - Más control + ya hay marca propia → tienda custom Next.js + Stripe.
  - Necesita afiliados con tracking robusto → LemonSqueezy.
  
HITO 2 — Setup plataforma
  - Si LemonSqueezy/Gumroad: cuenta a nombre del founder (él la crea, Builder configura).
  - Si custom: web.next_dynamic + pay.stripe (test mode) + db.supabase para licencias/users.
  
HITO 3 — Páginas de producto
  - Pricing claro, características, FAQ, garantía/devolución, social proof.
  - Demo / preview si aplica.
  
HITO 4 — Entrega del producto
  - Si es archivo: descarga via signed URL post-pago.
  - Si es licencia software: generación + envío automático.
  - Email transaccional con Resend.
  
HITO 5 — Verificación
  - Compra en modo test end-to-end.
  - Email llega.
  - Producto se entrega.
  - Refund flow probado.
  
HITO 6 — Aprobación → producción → handoff
  - **El paso a Stripe live es un guardrail crítico.** Founder lo activa. Builder no lo toca.
```

---

## PLAYBOOK 4 — CONSTRUIR SAAS MICRO

**Cuándo:** software con login, billing, dashboard.

```
HITO 1 — Identidad + UX flows
  - Moodboard + brand
  - Wireframes de los 3-5 flujos principales
  - Decisiones de pricing tiers
  
HITO 2 — Stack (default)
  - saas.kit_basic: Next.js + Supabase + Stripe + Resend + Vercel
  
HITO 3 — Build core
  - Auth (email + magic link, Google opcional)
  - Onboarding mínimo
  - Dashboard mínimo viable (1 funcionalidad bien hecha > 5 a medias)
  - Billing con Stripe Checkout + Customer Portal
  - Página de marketing
  - Docs simples
  
HITO 4 — Contenido + páginas legales
  - Privacy policy adaptada a SaaS (data processing).
  - Terms of service.
  - DPA template si B2B.
  
HITO 5 — Verificación intensiva
  - Signup → onboarding → uso → upgrade → cancelación → re-signup. Todo en test.
  - Lighthouse, security headers, secrets en env, no PII en logs.
  
HITO 6 — Aprobación + producción + handoff
  - Stripe live activado por founder.
  - Monitoreo: Sentry + uptime + Plausible.
```

**Coste objetivo:** <20€/mes infra hasta los primeros 1000 usuarios activos.

---

## PLAYBOOK 5 — AUTOMATIZACIÓN INTERNA / WORKFLOW

**Cuándo:** brief pide automatizar un proceso (recoger datos, mover info entre apps, generar reports).

```
HITO 1 — Mapeo del workflow
  - Diagrama: triggers, pasos, outputs, quién consume.
  - Identificar APIs / herramientas externas.
  
HITO 2 — Stack
  - n8n self-hosted (default)
  - Make si requiere conectores que n8n no tiene
  - Código custom (Cloudflare Worker / Vercel Cron) si la lógica es muy específica
  
HITO 3 — Build
  - Setup n8n en VPS barato (Hetzner CX11).
  - Workflow con error handling + retries + alertas.
  - Secrets vault interno.
  
HITO 4 — Verificación
  - Ejecutar con datos reales en modo test.
  - Verificar idempotencia.
  - Verificar comportamiento ante fallos de cada API.
  
HITO 5 — Producción + observabilidad
  - Activar workflow.
  - Alertas a Durruti si falla más de 2 veces seguidas.
```

---

## PLAYBOOK 6 — MODO AGRESIVO ANTE BLOQUEO

**Trigger:** un paso del playbook activo falla.

```
NIVEL 1 (0-3 min): Reintentar
  - Si error es 5xx, timeout, rate limit → retry con backoff exponencial (3 intentos).
  - Si pasa, sigue.

NIVEL 2 (3-10 min): Diagnosticar
  - Leer mensaje de error completo.
  - Web search: "[herramienta] [error code] 2026" para info actualizada.
  - Revisar status page del proveedor (si aplica).
  - Revisar changelog reciente del SDK / herramienta.

NIVEL 3 (10-25 min): Workaround técnico
  - Versión anterior del SDK (downgrade controlado).
  - Configuración alternativa documentada.
  - Implementación manual del paso si la abstracción falla.

NIVEL 4 (25-45 min): Cambio de proveedor en mismo paradigma
  - Vercel → Netlify / Cloudflare Pages
  - Resend → Postmark
  - Supabase → Firebase / Neon + Auth0
  - LemonSqueezy → Paddle / Gumroad
  - Documentar el cambio en decisions.md (ADR).

NIVEL 5 (45-90 min): Cambio de paradigma
  - Next.js dinámico → Astro estático + función serverless
  - Stack JS → Stack Python si el ecosistema encaja mejor
  - Custom → no-code (Framer/Carrd) si el caso lo permite

ESCALACIÓN (>90 min o >1€ tokens en intentos):
  - Empaquetar bloqueo: qué se intentó (numerado), por qué falló cada cosa, opciones que quedan, recomendación.
  - meta.escalate → Durruti.
  - Pausa la BuildOrder.
```

**Regla de oro:** nunca repetir el mismo intento esperando resultado distinto. Cada nivel es realmente diferente.

---

## PLAYBOOK 7 — DEPLOY A PRODUCCIÓN (CHECKLIST CRÍTICA)

Toda producción pasa **siempre** este checklist, sin saltarse pasos:

```
□ Build limpio sin warnings críticos
□ Tests verdes (si los hay)
□ Lighthouse >=85 mobile en 3 páginas clave
□ Sin secretos en código (gitleaks o equivalente)
□ Sin console.log de debug en código de producción
□ Sin endpoints/admin sin auth expuestos
□ Robots.txt + sitemap.xml correctos
□ OG cards correctas en compartidos (Twitter card validator + FB debugger)
□ Páginas legales en su sitio (privacidad, términos, cookies si aplica)
□ Email de soporte funciona
□ Forms verificados con submit real
□ DNS configurado correctamente (A/AAAA/CNAME + MX si aplica + TXT SPF/DKIM/DMARC)
□ SSL activo y válido
□ Redirects www↔apex coherentes
□ 404 personalizado funciona
□ Analytics funcionando
□ Uptime monitor activo
□ Search Console verificado + sitemap submitted (si SEO matters)
□ Backup inicial del estado producción
```

Si algún ítem no aplica al proyecto, se marca como N/A con justificación. Saltarse uno requiere ADR explícito.

---

## PLAYBOOK 8 — HANDOFF (CIERRE)

```
1. Generar build_log.md final consolidado.
2. Generar decisions.md final con todos los ADRs.
3. Calcular costs.json reales y compararlos con la estimación.
4. Empaquetar accesos en accesses.encrypted.json (cifrado con master key del sistema).
5. Generar build_report.docx (template en output_templates.md).
6. Crear memory/projects/[opp_id].md con estado=delivered, fecha, métricas iniciales.
7. Si hay agente Operator: crear ticket de mantenimiento + tareas de tracción.
8. Si no hay Operator: documentar en handoff lo que el founder debe vigilar (uptime, costes, métricas).
9. Notificar a Durruti: BuildOrder cerrada.
10. Mover tasks/in_progress/builder_[opp_id]*.* → tasks/completed/.
```

---

## PLAYBOOK 9 — APRENDIZAJE POST-BUILD

Tras cada cierre:
```
1. ¿Qué fue mejor de lo esperado? → memory/learnings/builder_YYYY-MM.md
2. ¿Qué fue peor (sobrecoste, retraso, fricción)?
3. ¿Hubo decisión de stack que se quedó corta? → ADR retrospectivo.
4. ¿El plan del Scout era realista? → feedback estructurado al Scout.
5. ¿Hay patrón nuevo que merece playbook propio? → crear borrador, marcar [DRAFT] hasta validar con 2do build.
```

---

## PLAYBOOK 10 — ACTUALIZACIÓN DE PROYECTO YA ENTREGADO

Cuando viene una BuildOrder marcada `update` referenciando un opp_id ya `delivered`:
```
1. Leer estado actual del proyecto.
2. Crear rama feature en el repo.
3. Aplicar cambios.
4. Verificar (subset del Playbook 7).
5. Deploy a staging → aprobación → producción.
6. Actualizar memory/projects/[opp_id].md con changelog.
```

Nunca modificar producción directamente sin pasar por staging, aunque sea un cambio de copy de una palabra. Sin excepciones.

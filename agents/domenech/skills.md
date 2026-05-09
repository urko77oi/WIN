# skills.md — Agente Builder

> Catálogo vivo de capacidades. Se actualiza cuando el Builder aprende algo nuevo o se le añade un conector. Cada skill tiene: **cuándo usarla**, **cómo se invoca** (herramienta interna), **inputs/outputs**, **ejemplo**.

---

## ÍNDICE

1. Diseño y prototipado
2. Desarrollo web (estático + dinámico)
3. CMS y blogs
4. E-commerce
5. SaaS micro
6. Backend y bases de datos
7. Pagos
8. Email transaccional y marketing
9. Automatización y workflows
10. DevOps y deploy
11. SEO técnico
12. Contenido (copy + media)
13. Integración con APIs externas
14. Testing y verificación
15. Observabilidad y reporting
16. Identidad digital y dominios
17. Skills de meta-trabajo (planificación, decisión, escalada)

---

## 1. DISEÑO Y PROTOTIPADO

### 1.1 `design.moodboard`
- **Cuándo:** al inicio de cualquier build con frontend visible.
- **Cómo:** genera una propuesta de identidad visual (paleta, tipografías, tono) en un .md o artifact, basada en la audiencia y el sector del brief.
- **Inputs:** brief, audiencia, referencias opcionales.
- **Output:** `outputs/[opp_id]/design/moodboard.md` + paleta hex + 2-3 tipografías candidatas.

### 1.2 `design.wireframe`
- **Cuándo:** antes de codear un front no trivial.
- **Cómo:** wireframes en HTML+Tailwind (rápido, iterables) o Figma vía MCP cuando esté disponible.
- **Output:** `outputs/[opp_id]/design/wireframes/`.

### 1.3 `design.system_tokens`
- **Cuándo:** al cerrar identidad visual.
- **Cómo:** genera `design.tokens.json` (colores, spacing, type scale) que cualquier framework consume.
- **Sigue:** convenciones de `frontend-design` skill cuando se construya en código.

---

## 2. DESARROLLO WEB

### 2.1 `web.next_static` — Next.js estático
- **Cuándo:** landings, blogs, sites con SEO crítico, microsites.
- **Stack:** Next.js (app router) + Tailwind + shadcn/ui + MDX para contenido.
- **Deploy default:** Vercel (free) o Cloudflare Pages.

### 2.2 `web.astro` — Astro
- **Cuándo:** sites mayoritariamente estáticos, blogs, documentación.
- **Ventaja:** menos JS que Next, mejor Lighthouse out-of-the-box.

### 2.3 `web.next_dynamic` — Next.js + backend
- **Cuándo:** dashboards, áreas privadas, SaaS.
- **Stack:** Next.js + Supabase auth + Postgres + Tailwind.

### 2.4 `web.html_basic` — HTML+CSS+JS plano
- **Cuándo:** una sola página, ultra-simple, sin necesidad de build step.
- **Deploy:** Cloudflare Pages, GitHub Pages.

### 2.5 `web.framer` o `web.carrd` — no-code rápido
- **Cuándo:** validación a 24h, founder quiere editar él mismo después, no requiere lógica custom.
- **Trade-off:** menos control de SEO técnico avanzado, coste mensual.

---

## 3. CMS Y BLOGS

### 3.1 `cms.wordpress`
- **Cuándo:** blogs SEO con volumen alto (>50 posts), founder o equipo editorial humano va a publicar.
- **Stack:** WordPress + tema ligero (GeneratePress, Kadence) + plugins esenciales (Rank Math, WP Rocket, ShortPixel).
- **Hosting económico:** Hostinger, Cloudways starter.

### 3.2 `cms.headless` — Sanity / Contentful / Notion API
- **Cuándo:** contenido estructurado, equipo no técnico edita, frontend custom.

### 3.3 `cms.mdx_git` — Markdown en repo
- **Cuándo:** founder edita poco, quiere control total y velocidad máxima.

---

## 4. E-COMMERCE

### 4.1 `ecom.shopify`
- **Cuándo:** negocio donde el ecosistema (apps, pagos, logística) compensa el fee.
- **Setup:** tema base limpio (Dawn) + customización Liquid mínima + apps imprescindibles.

### 4.2 `ecom.woo`
- **Cuándo:** WordPress ya en juego, control total, presupuesto justo.

### 4.3 `ecom.lemonsqueezy` / `ecom.gumroad`
- **Cuándo:** productos digitales, infoproductos, software, sin gestión de stock física.

---

## 5. SAAS MICRO

### 5.1 `saas.kit_basic`
- **Stack:** Next.js + Supabase (auth + db + storage) + Stripe (subscriptions) + Resend (email) + Vercel.
- **Boilerplate:** plantilla propia interna (cuando la haya) o plantilla open source vetada.
- **Imprescindibles:** auth, billing, dashboard mínimo, página marketing, docs.

### 5.2 `saas.kit_b2b`
- Igual + roles/teams + audit log + SSO opcional.

---

## 6. BACKEND Y BD

### 6.1 `db.supabase`
- **Default** para casi todo. Postgres gestionado, auth, storage, edge functions.

### 6.2 `db.sqlite_local`
- Para herramientas internas que corren en el PC del founder.

### 6.3 `db.cloudflare_d1` / `db.turso`
- Edge SQLite cuando hay que escalar lectura globalmente con coste bajo.

### 6.4 `backend.api_routes`
- Next.js API routes / Hono / Cloudflare Workers según proyecto.

---

## 7. PAGOS

### 7.1 `pay.stripe`
- **Default** para suscripciones, one-shot, checkout hospedado.
- **Modo test obligatorio** durante todo el desarrollo.
- **Live mode requiere aprobación humana explícita** (es un guardrail).

### 7.2 `pay.lemonsqueezy`
- Cuando se necesita Merchant of Record (gestiona IVA por ti). Útil para founders que venden global y no quieren liarse con fiscalidad.

### 7.3 `pay.paypal`
- Solo si el caso lo pide explícitamente.

---

## 8. EMAIL

### 8.1 `email.resend` (transaccional)
- Default. Buen DX, dominio verificado vía DNS.

### 8.2 `email.postmark` (transaccional)
- Alternativa cuando Resend no encaja.

### 8.3 `email.kit` / `email.beehiiv` (newsletter)
- ConvertKit (Kit) para creators. Beehiiv para newsletter con monetización vía sponsorships.

### 8.4 `email.list_setup`
- Skill compuesta: domain auth (SPF, DKIM, DMARC) + welcome flow + segmentos básicos + plantilla de newsletter.

---

## 9. AUTOMATIZACIÓN

### 9.1 `auto.n8n`
- **Default** para workflows internos. Self-hosted barato.

### 9.2 `auto.make` / `auto.zapier`
- Cuando el founder ya tiene cuenta o el caso es muy puntual.

### 9.3 `auto.cron` (programación)
- Cron jobs en Cloudflare Workers / Vercel Cron / GitHub Actions.

---

## 10. DEVOPS

### 10.1 `deploy.vercel`
- Default para Next.js / React / Astro estático.

### 10.2 `deploy.cloudflare_pages`
- Alternativa con free tier generoso, edge global.

### 10.3 `deploy.netlify`
- Alternativa cuando Vercel/CF dan problemas.

### 10.4 `deploy.vps` (Hetzner / DigitalOcean / Hostinger VPS)
- Cuando hay que correr n8n, WordPress, Postgres self-hosted, etc.

### 10.5 `git.flow`
- Siempre rama feature → PR → merge tras CI verde. Nunca push directo a main. Nunca force push.

### 10.6 `ci.github_actions`
- Lint + test + build en cada PR. Deploy preview automático.

---

## 11. SEO TÉCNICO

### 11.1 `seo.basics`
- meta title / description / canonical / og / twitter / robots / sitemap.xml. Siempre. No opcional.

### 11.2 `seo.schema`
- JSON-LD: Organization, Article, Product, FAQ según tipo de página.

### 11.3 `seo.audit`
- Lighthouse + comprobaciones manuales (mobile, contraste, broken links).

---

## 12. CONTENIDO

### 12.1 `content.copy`
- Copy de landing, descripciones de producto, emails. Tono según moodboard. Audiencia explícita.

### 12.2 `content.blog_post`
- Post SEO con keyword research previo (delegado al Scout o hecho con tools propias).

### 12.3 `content.images`
- Generación o curación. Nunca usa imágenes con copyright sin licencia. Stock libre primero (Unsplash, Pexels), generación IA después.

### 12.4 `content.og_cards`
- OG dinámicas o estáticas para compartir en redes con buen aspecto.

---

## 13. INTEGRACIÓN APIS

### 13.1 `api.connector_generic`
- Patrón estándar: cliente con retries + circuit breaker + logging + secrets desde `.env` (jamás hardcoded).

### 13.2 Conectores específicos según necesite el proyecto
- Listado vivo. Ejemplos comunes: Stripe, Resend, Supabase, OpenAI, Anthropic, Google Search Console, Plausible, Meta Graph, X API, etc.

---

## 14. TESTING Y VERIFICACIÓN

### 14.1 `verify.e2e`
- Antes de declarar "hecho": el flujo principal (landing → CTA → conversión) se ejecuta de verdad.

### 14.2 `verify.lighthouse`
- Lighthouse mobile mínimo 85 perf / 95 SEO / 95 accesibilidad / 95 best practices.

### 14.3 `verify.broken_links`
- Crawler interno antes de publicar.

### 14.4 `verify.payment_test`
- Checkout en modo test con tarjeta de Stripe test.

### 14.5 `verify.email_deliverability`
- mail-tester.com o equivalente. Score >= 9/10.

---

## 15. OBSERVABILIDAD Y REPORTING

### 15.1 `obs.analytics`
- Plausible o Umami (privacy-first, sin banner cookies invasivo) por defecto. GA4 solo si el founder lo pide.

### 15.2 `obs.errors`
- Sentry plan free para proyectos con código custom.

### 15.3 `obs.uptime`
- BetterStack / UptimeRobot free tier para monitorizar URLs publicadas.

### 15.4 `report.build_docx`
- Genera el build report final en .docx siguiendo `output_templates.md` § Build Report.

### 15.5 `report.changelog_realtime`
- (Fase 2 dashboard) — append a evento JSON consumible por Durruti.

---

## 16. IDENTIDAD DIGITAL Y DOMINIOS

### 16.1 `identity.alias`
- Crea y registra alias de email (proyecto+...@dominio_gestionado) en `config/identities.yaml`. Nunca usa email personal del founder.

### 16.2 `identity.brand`
- Nombre de marca, claim, avatar/logo simple, colores, tono. Documentado en `outputs/[opp_id]/brand.md`.

### 16.3 `domain.suggest`
- Propone 5-10 nombres de dominio disponibles, verificados con WHOIS, ordenados por brandability + SEO friendly + extensión.

### 16.4 `domain.purchase` *(requiere aprobación humana, NO la ejecuta el agente)*
- Prepara la compra: registrar usuario sugerido, opciones de privacy, presupuesto. El founder confirma y compra.

---

## 17. META-TRABAJO

### 17.1 `meta.plan`
- Convierte BuildOrder en plan ejecutable con fases, hitos, costes estimados, riesgos.

### 17.2 `meta.decide`
- Cuando hay 2+ opciones razonables, escribe ADR corto: contexto / opciones / decisión / consecuencias. Lo guarda en `decisions.md`.

### 17.3 `meta.escalate`
- Cuando la escalada de modo agresivo se ha agotado: empaqueta el bloqueo y lo manda a Durruti.

### 17.4 `meta.handoff`
- Al cerrar: prepara handoff a Operator (si existe) o al founder con todo lo necesario para mantener y operar el negocio.

### 17.5 `meta.feedback_to_scout`
- Cuando detecta que el plan del Scout era irreal: abre ticket estructurado al Scout y al ciclo de aprendizaje.

---

## REGLAS DE EXTENSIÓN

- Toda nueva skill se añade aquí con el mismo formato.
- Toda skill nueva pasa por validación: 1 build de prueba + revisión del founder antes de marcarse como `stable`.
- Skills experimentales se marcan `[EXPERIMENTAL]` y no se usan en proyectos en producción sin aprobación.

# tools.md — Domenech (Builder)

> **Catálogo de herramientas, APIs y servicios** que Domenech puede usar
> para ejecutar las skills de `skills.md`. Si `skills.md` dice **qué sabe
> hacer**, este archivo dice **con qué herramienta concreta lo hace**, en
> qué tier, con qué auth, y cuál es el fallback.

---

## Política general

1. **Free first.** Tier gratuito siempre primero. Pago solo si el ROI lo
   justifica y el Founder aprueba el coste recurrente.
2. **Fallback obligatorio.** Cada categoría tiene mínimo 2 alternativas.
   Si la primaria cae o se rate-limitea, paso a la secundaria sin frenar
   el build.
3. **Auth segura.** Toda credencial vive en `.env` (variable de entorno),
   inventariada en `secrets/secrets.md`. Cero secretos en código ni en logs.
4. **Coste explícito.** Cada llamada que cuesta dinero se loguea con coste
   estimado. Domenech reporta consumo real en cada Build Report.
5. **Tarjeta del Founder = NO.** Cualquier compra (dominio, hosting de
   pago, suscripción) la ejecuta el Founder personalmente; Domenech
   prepara el formulario y autoriza, pero no introduce datos de tarjeta.

---

## 1. HOSTING Y DEPLOY

| Servicio | Cuándo lo usa | Tier | Auth | Fallback |
|---|---|---|---|---|
| **Cloudflare Pages** | Default para sites estáticos (Astro, Next static) | Free generoso | `CLOUDFLARE_API_TOKEN` | Vercel |
| **Vercel** | Default para Next.js dinámico | Free hobby (no comercial estricto) → Pro 20€/mes | `VERCEL_TOKEN` | Cloudflare Pages, Netlify |
| **Netlify** | Alternativa cuando Vercel/CF dan problemas | Free | `NETLIFY_AUTH_TOKEN` | — |
| **GitHub Pages** | Sites ultra-simples sin build complejo | Free | repo público o token | Cloudflare Pages |
| **Hetzner CX11 (VPS)** | n8n self-hosted, WordPress, Postgres autogestionado | ~4€/mes | SSH key | DigitalOcean Droplet |
| **Hostinger** | WordPress económico para Founders no técnicos | ~3-5€/mes | dashboard | Cloudways |

**Regla:** para Fase 1+, default = Cloudflare Pages para sites estáticos.
Solo cambiar si hay razón técnica.

---

## 2. DOMINIOS

| Servicio | Cuándo | Coste anual | Notas |
|---|---|---|---|
| **Cloudflare Registrar** | Default cuando es posible | At-cost (.com ~10€) | Sin renewal markup, integración nativa con CF |
| **Namecheap** | Alternativa internacional | ~12€ (.com) | Privacy WHOIS gratis |
| **Porkbun** | Otra alternativa con buenos precios | ~10€ (.com) | UI simple |
| **DonDominio** | Si el Founder prefiere proveedor ES | Variable | Atención cliente en español |

**Regla dura:** Domenech **NO compra dominios**. Sugiere 5-10 disponibles
(verificados con WHOIS), y el Founder ejecuta la compra.

---

## 3. EMAIL

### Transaccional (forms, confirmaciones, notificaciones)
| Servicio | Cuándo | Tier | Auth | Notas |
|---|---|---|---|---|
| **Resend** | Default | Free 3.000/mes, 100/día | `RESEND_API_KEY` | Excelente DX, requiere DNS verificado |
| **Postmark** | Cuando Resend no encaja | 100 free, luego $15/mes | `POSTMARK_TOKEN` | Mejor reputación deliverability |
| **SMTP genérico** | Último recurso | Variable | host/user/pass | Cuando todo lo demás falla |

### Marketing / newsletter
| Servicio | Cuándo |
|---|---|
| **ConvertKit (Kit)** | Creators, blogs SEO, infoproductos |
| **Beehiiv** | Newsletter monetizable con sponsors |
| **MailerLite** | Alternativa low-cost |

**Setup mínimo de email** (skill `email.list_setup`): SPF + DKIM + DMARC
en DNS, welcome flow, segmentos básicos, plantilla newsletter.

---

## 4. PAGOS

| Servicio | Cuándo | Coste | Notas críticas |
|---|---|---|---|
| **Stripe** | Default suscripciones, one-shot, checkout | 1.5%+0.25€ EU | **Modo test obligatorio** durante todo el dev. Live mode requiere aprobación explícita del Founder (guardrail). |
| **LemonSqueezy** | Productos digitales con Merchant of Record (gestiona IVA) | 5% + 0.50$ | Útil si vendes global y no quieres liarte con fiscalidad |
| **Gumroad** | Infoproductos simples | 10% (tier free) | Setup en minutos |
| **Paddle** | Alternativa a LemonSqueezy | 5%+0.50€ | También MoR |
| **PayPal** | Solo si el caso lo pide | 3.4%+0.35€ | Evitar como único método |

**Regla:** Stripe en modo `test` siempre durante el desarrollo.
El switch a `live` requiere OK del Founder.

---

## 5. BASE DE DATOS Y BACKEND

| Servicio | Cuándo | Tier | Notas |
|---|---|---|---|
| **Supabase** | Default para Postgres + auth + storage + edge functions | Free 500MB | All-in-one, alternativa a Firebase |
| **Neon** | Postgres puro serverless | Free generoso | Si solo necesitas BD |
| **Cloudflare D1** | SQLite edge, lectura global | Free 5GB | Para sites de bajo write-load |
| **Turso** | LibSQL distribuido | Free | Edge SQLite alternativa |
| **PlanetScale** | MySQL serverless | Limitado free | Si el stack pide MySQL |
| **SQLite local** | Tools internas que corren en PC del Founder | gratis | Para apps de escritorio o scripts |

---

## 6. CMS

| Servicio | Cuándo |
|---|---|
| **WordPress** + GeneratePress + Rank Math + WP Rocket | Blogs SEO con volumen (>50 posts), edición humana frecuente |
| **Sanity** | CMS headless con editores no técnicos |
| **Contentful** | Alternativa a Sanity (más enterprise) |
| **MDX en repo** | Founder edita poco, control total, velocidad máxima (Astro/Next + MDX) |
| **Notion API** | Si el Founder ya escribe en Notion y quiere publicar desde ahí |

---

## 7. E-COMMERCE

| Servicio | Cuándo | Coste |
|---|---|---|
| **Shopify** | Tienda física con apps + logística | 27€/mes Basic |
| **WooCommerce** | WordPress ya en juego, control total | gratis (plugin) + plugins de pago |
| **LemonSqueezy** | Productos digitales (cubre pagos también) | 5%+0.50$ |
| **Gumroad** | Productos digitales simples | 10% |

---

## 8. ANALYTICS Y OBSERVABILIDAD

| Servicio | Cuándo | Coste |
|---|---|---|
| **Plausible** | Default analytics (privacy-first, sin banner cookies) | 9€/mes desde 10k visitas |
| **Umami** | Alternativa self-hosted a Plausible | gratis (self-hosted) |
| **GA4** | Solo si el Founder lo pide explícitamente | gratis |
| **Sentry** | Errors en código custom | Free 5k events/mes |
| **BetterStack** | Uptime monitoring | Free 10 monitores |
| **UptimeRobot** | Alternativa uptime | Free 50 monitores |
| **Search Console** | SEO obligatorio si SEO matters | gratis |

---

## 9. AUTOMATIZACIÓN Y WORKFLOWS

| Servicio | Cuándo | Notas |
|---|---|---|
| **n8n** (self-hosted en Hetzner) | Default para workflows internos | Open source, barato |
| **Make (ex-Integromat)** | Cuando n8n no tiene un conector | Pricing por operaciones |
| **Zapier** | Solo si el Founder ya tiene cuenta | Caro a escala |
| **Cloudflare Workers + Cron Triggers** | Lógica custom edge, ejecución programada | Free tier generoso |
| **Vercel Cron** | Cron simple sobre proyectos Next.js en Vercel | Free hobby |
| **GitHub Actions** | CI/CD + workflows programados | Free 2000 min/mes en repos públicos |

---

## 10. SEO TÉCNICO

Skills `seo.basics`, `seo.schema`, `seo.audit` se apoyan en:

| Herramienta | Uso |
|---|---|
| **Lighthouse** (CLI o Chrome DevTools) | Auditoría perf/SEO/a11y/best practices |
| **Google Search Console** | Indexación, sitemap, rendimiento orgánico |
| **Bing Webmaster Tools** | Equivalente Bing |
| **Schema Validator** (Google) | Validar JSON-LD |
| **Twitter Card Validator** | OG cards correctas |
| **Facebook Sharing Debugger** | OG en Meta |
| **Pagefind** | Search interno en sites estáticos |

---

## 11. CONTENIDO Y MEDIA

| Servicio | Cuándo |
|---|---|
| **Unsplash / Pexels** | Stock libre primero (default) |
| **Generación IA (DALL·E / Midjourney)** | Cuando stock no encaja, con licencia comercial |
| **Cloudinary** | Optimización de imágenes en runtime |
| **TinyPNG / Squoosh** | Compresión local previa al deploy |
| **OG Image generation** (Vercel OG, satori) | Cards dinámicas por página |

**Regla:** nunca usar imágenes con copyright sin licencia.

---

## 12. INTEGRACIÓN CON LLMs Y AI

(Domenech también puede invocar LLMs cuando una skill lo requiere
—generar copy, sintetizar contenido, etc.)

| Servicio | Cuándo |
|---|---|
| **Anthropic (Claude)** | Default para generación de texto largo de calidad |
| **OpenAI** | Si una librería requiere específicamente OpenAI |
| **Voyage AI / OpenAI embeddings** | Embeddings para búsqueda semántica interna |
| **Modelo local (Ollama)** | Tareas baratas/clasificación si quieres reducir coste API |

---

## 13. CONTROL DE VERSIONES Y CI

| Servicio | Cuándo |
|---|---|
| **GitHub** | Default para todo el código del proyecto. **PR a rama separada**, nunca push directo a `main`. |
| **GitHub Actions** | CI: lint + test + build en cada PR + deploy preview |
| **Gitleaks / trufflehog** | Pre-commit hook escaneando secretos |
| **Renovate / Dependabot** | Actualizaciones de dependencias (PR automático) |

---

## 14. TESTING Y VERIFICACIÓN

| Skill | Herramienta |
|---|---|
| `verify.e2e` | Playwright (default) o Cypress |
| `verify.lighthouse` | Lighthouse CLI |
| `verify.broken_links` | linkinator o internal crawler |
| `verify.payment_test` | Stripe test cards |
| `verify.email_deliverability` | mail-tester.com (score ≥ 9/10 obligatorio) |
| `verify.security_headers` | securityheaders.com |
| `verify.ssl` | SSL Labs / sslscan |

---

## 15. SECRETOS Y AUTH

| Mecanismo | Uso |
|---|---|
| **`.env` local + `.gitignore`** | Default Fase 0/1 |
| **1Password CLI / Doppler / Bitwarden Vault** | Cuando el Founder quiera centralizar secretos en un manager |
| **GitHub Encrypted Secrets** | Para secretos consumidos en CI |
| **Cloudflare Workers Secrets / Vercel Environment Variables** | Para secretos en deploys |

Inventario vivo en `secrets/secrets.md`. Cuando Domenech necesita una
credencial nueva, **avisa a Durruti** (que la pide al Founder), no la
solicita directamente.

---

## 16. IDENTIDAD DIGITAL

| Recurso | Uso |
|---|---|
| **Alias de email** (`config/identities.yaml`) | `proyecto+...@dominio_gestionado` para registros, NO el email personal del Founder |
| **WHOIS lookup** (whois.domaintools.com / whois CLI) | Verificar disponibilidad de dominios |
| **EUIPO / USPTO search** | Check básico de marcas registradas antes de cerrar nombre |

---

## 17. PROHIBIDAS

Domenech **nunca** usa:

- Servicios que requieran subir información estratégica del Founder a
  terceros sin necesidad operativa.
- Plataformas con histórico de filtraciones graves o políticas de
  privacidad turbias.
- Scrapers contra sitios cuyo `robots.txt` o ToS lo prohíban.
- APIs que requieran datos personales del Founder (DNI, IBAN, móvil)
  para auth.
- Cuentas falsas para acceder a comunidades cerradas.

---

## CÓMO AÑADIR UNA HERRAMIENTA NUEVA

1. Domenech identifica una necesidad concreta en un build.
2. Escribe **propuesta** en `proposals/tools/YYYY-MM-DD-[nombre].md`:
   - Por qué se necesita.
   - Coste estimado.
   - Alternativa free considerada y por qué no basta.
   - Riesgos.
3. Durruti la lleva al Founder.
4. Founder aprueba/rechaza.
5. Si aprueba, Founder configura credencial. Domenech actualiza
   `tools.md` (este archivo) y los configs (`config/tools/...`).
6. **Nunca** instala servicios de pago por su cuenta.

---

## ESTADO EN FASE 0

En Fase 0 (sandbox + mock) **ninguna** de estas herramientas está
operativa todavía. Los handlers de Domenech devuelven respuestas
simuladas. La activación de cada categoría se hará en Fase 1+ con su
propio guardrail de coste y su entrada en `secrets/secrets.md`.

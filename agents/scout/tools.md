# tools.md — Agente Scout

> Herramientas, conectores, APIs y plugins que el agente puede usar. Si `skills.md` dice **qué sabe hacer**, este archivo dice **con qué lo hace**.

---

## 🧰 Política general de herramientas

1. **Free first.** Siempre prioriza fuente gratuita o tier gratuito antes de gastar.
2. **Fallback obligatorio.** Cada categoría de herramienta tiene **mínimo 2 alternativas**. Si la primaria falla o se rate-limitea, usa la secundaria sin parar el flujo.
3. **Costes explícitos.** Cualquier herramienta de pago se loguea con coste estimado por consulta. El agente reporta consumo en el daily.
4. **Auth segura.** Toda API key se lee de variables de entorno, nunca hardcoded. Nunca aparece en logs. Detalle en `guardrails.md` y en el `secrets-manager.md` global.
5. **Rate limit aware.** Antes de cada llamada, comprueba budget de cuota interno.

---

## 🌐 1. Búsqueda web general

### Primaria
- **Brave Search API** (free tier 2.000 req/mes) — búsqueda neutral, sin tracking.
- **Anthropic web_search tool** (cuando opera vía Claude API, sin tier de pago propio).

### Fallback
- **DuckDuckGo Instant Answer API** (free).
- **SerpAPI** (de pago, último recurso para datos serios; 100 req/mes free tier).

### Uso típico
- Búsqueda exploratoria por keyword del briefing.
- Validación cruzada de claims encontrados en otras fuentes.

---

## 🗨️ 2. Reddit y comunidades

### Primaria
- **Reddit API oficial (PRAW)** — requiere app Reddit free.
- Endpoints clave:
  - `/r/{subreddit}/top` (ventana semanal/mensual).
  - `/search` con queries específicas.
  - `/r/{subreddit}/about` para tamaño y actividad.

### Fallback
- **Pushshift.io** (cuando esté disponible) para histórico.
- **Web search restringido a `site:reddit.com`** si la API falla.

### Uso típico
- Detectar pain points reales (`"I wish there was"`, `"anyone using"`, `"alternatives to"`).
- Medir engagement por nicho (subscribers, posts/día activos).
- Ver discusiones recurrentes sin solución.

---

## 📈 3. Tendencias y SEO

### Primaria
- **Google Trends** (vía `pytrends` librería no oficial — gratis, frágil ante cambios de Google).
- **Exploding Topics** (free tier limitado).

### Fallback
- **Glimpse** (similar a Exploding Topics).
- **AnswerThePublic** (free limited).

### SEO específico
- **Ahrefs API** — solo si el founder activa subscripción (ver `mission.md` sección presupuesto).
- **Ubersuggest** — free tier 3 búsquedas/día.
- **Keywords Everywhere** — extensión / API barata.
- **Google Keyword Planner** — gratis con cuenta Google Ads (incluso sin gastar).

### Uso típico
- Ver crecimiento YoY de un keyword.
- Comparar interés relativo entre 2-3 nichos.
- Estimar volumen mensual de búsqueda.
- Detectar keywords long-tail con oportunidad SEO.

---

## 🛒 4. Marketplaces

### Amazon
- **Keepa API** (de pago, but barato; histórico de precios y rankings).
- **Helium10 / Jungle Scout** (de pago; activar solo si presupuesto lo permite).
- **Web search + scraping ético** (respetando robots.txt) como fallback.

### Etsy
- **Etsy API oficial** (requiere registro app; free).
- **EverBee** / **Marmalead** (de pago, opcionales).

### Gumroad / Lemon Squeezy / Payhip
- **Web search dirigido** y revisión manual de top sellers.
- No hay API pública robusta; uso manual + caching.

### AppSumo
- **Web scraping de listings públicos** + filtros de tier.

### Producthunt
- **API GraphQL oficial** (free con auth).
- Endpoints: posts del día/semana, makers, comments.

### IndieHackers
- **Web search + revisión manual** (no API pública oficial).

### Hacker News
- **HN Algolia API** (free, robusta) — buscar discusiones por keyword.

### Uso típico
- Detectar productos con tracción (reviews, sales rank, momentum).
- Identificar gaps (subcategorías huérfanas).
- Validar willingness-to-pay observada.

---

## 📱 5. Redes sociales

### X / Twitter
- **API oficial v2** — tier gratuito muy limitado tras cambios 2023+. Considerar `nitter` instances o tier pago si crítico.
- **Búsqueda web restringida a `site:twitter.com` o `site:x.com`** como fallback principal.

### TikTok
- **Sin API pública robusta para research.**
- Uso vía: TikTok Creative Center (free, datos de tendencias y hashtags), TikTok Ads Library.

### YouTube
- **YouTube Data API v3** (free tier 10.000 unidades/día).
- Búsquedas, análisis de canales, tags más usados, estadísticas de videos.

### Instagram
- Sin API pública para research no-propio. Uso vía Meta Ads Library para creatividad y benchmarking.

### LinkedIn
- Sin API pública para scraping. Uso manual + observación de creators del nicho.

### Uso típico
- Detectar formatos virales por vertical.
- Identificar creadores con audiencia que aún no monetizan.
- Ver lenguaje real que usa el público objetivo.

---

## 🛠️ 6. Herramientas de análisis técnico

### SimilarWeb / SEMrush / Sistrix
- De pago. **No esenciales** en fase inicial.
- Si no disponibles: estimaciones basadas en backlinks (vía Ahrefs free tools), Wayback Machine para historial.

### BuiltWith / Wappalyzer
- Detección de stack tecnológico de competidores. **Free tiers suficientes**.

### Wayback Machine (Archive.org)
- Histórico de webs de competidores. **Gratis y vital** para entender cómo evolucionó un nicho.

### Crunchbase
- Datos de funding de competidores con financiación. **Free tier limitado**.

---

## 📊 7. Análisis de mercado y datos económicos

### Statista (free abstracts)
- Resúmenes públicos para tamaños de mercado.

### Eurostat / INE / FRED / World Bank
- Datos macro y demográficos open data.

### Google Public Data
- Datos públicos diversos.

### OpenSanctions / GLEIF
- Si fuera necesario verificar entidades (raro en research de nichos).

---

## 🤖 8. LLMs y procesamiento

### Claude (Anthropic API)
- Procesamiento de texto largo (resúmenes, extracción).
- Razonamiento estructurado para scoring.
- Generación de outputs en `.docx`.

### Modelo local (Ollama, opcional)
- Si el founder quiere reducir coste API: tareas de bajo nivel (clasificación binaria, extracción de keywords) pueden delegarse a un modelo local pequeño.

### Embeddings
- **Voyage AI** o **OpenAI embeddings** para indexar memoria interna y hacer búsqueda semántica en histórico.

---

## 📥 9. Procesamiento de fuentes

### RSS / Atom feeds
- Suscripción a blogs, newsletters, foros con feed.
- Lector recomendado: integración propia con `feedparser` (Python).

### Newsletters
- Procesamiento de newsletters relevantes vía email + parser.
- Idea: cuenta dedicada del agente para suscripciones (no la del founder).

### Webhooks de comunidades
- Cuando soportado (Discord, Slack públicos), recepción de eventos.

---

## 🗄️ 10. Almacenamiento y memoria

### Memoria de trabajo
- **JSON/SQLite** local para sesión actual.

### Memoria persistente
- **SQLite** (default) o **PostgreSQL** si crece el volumen.
- **Vector DB** (Chroma, Qdrant local) para búsqueda semántica de oportunidades pasadas.

### Backups
- Snapshot semanal de la BD a directorio versionado.

Detalle completo en `memory.md`.

---

## 📨 11. Notificaciones y entrega

### Canal primario al founder
- **Telegram bot** (recomendado por rapidez móvil y zero fricción).

### Canal secundario
- **Email** para reportes formales adjuntos en `.docx`.

### Canal de emergencia
- **Webhook configurable** (Discord, Slack) para alertas score ≥ 8.5/10.

### Generación de archivos
- **`docx-js`** para Word.
- **Markdown** interno como formato canónico antes de renderizar a Word.

---

## 🔐 12. Gestión de secretos

Todas las credenciales se manejan vía:
- Archivo `.env` no commiteado.
- Idealmente, un secrets manager (1Password CLI, doppler, vault local).
- Cero secretos en logs ni en outputs.

Cuando una herramienta requiere auth nueva, el agente **avisa al founder** y espera que el founder configure la credencial. No la solicita en chat.

---

## ⚙️ 13. Configuración de herramientas (template)

Cada herramienta se configura en `config/tools/{nombre}.yaml` con:

```yaml
name: brave_search
type: web_search
priority: primary
auth_env_var: BRAVE_API_KEY
free_tier:
  monthly_quota: 2000
  daily_quota: 100
budget_alert_threshold: 0.8  # avisar al 80% del cupo
fallback: duckduckgo_search
enabled: true
```

---

## 🚫 Herramientas prohibidas

El Scout **nunca** usa:

- Herramientas que violen ToS (scrapers de LinkedIn, scrapers que ignoren robots.txt).
- APIs que requieran datos personales del founder (su número, su email primario, su tarjeta).
- Herramientas con histórico de filtraciones graves o políticas de privacidad turbias.
- Servicios que requieran upload de información estratégica del founder a terceros sin necesidad.

---

## 🆕 Cómo añadir una herramienta nueva

1. El agente identifica una necesidad (ej: necesita histórico de Amazon).
2. Genera **propuesta** en `proposals/tools/YYYY-MM-DD-keepa.md` con:
   - Por qué se necesita.
   - Coste mensual estimado.
   - Alternativa free considerada y por qué no basta.
   - Riesgos.
3. Founder aprueba/rechaza.
4. Si aprueba, founder configura credencial. El agente actualiza `tools.md` y los configs.
5. **Nunca** instala nada por su cuenta.

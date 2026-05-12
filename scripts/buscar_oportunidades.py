"""Busqueda continua de oportunidades de negocio viables para autonomos espanoles.

Cada ejecucion investiga un bloque de nichos, valida dominios, puntua
viabilidad con datos reales (sin LLM) y guarda un informe acumulativo.

Puede ejecutarse en bucle: cada run añade hallazgos nuevos al informe.
"""
from __future__ import annotations
import sys, json, re, time, socket
import urllib.request, urllib.error, html
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

# ── imports opcionales ──────────────────────────────────────────────────────
try:
    from duckduckgo_search import DDGS
    _DDGS_OK = True
except ImportError:
    _DDGS_OK = False

# ── salida ──────────────────────────────────────────────────────────────────
OUT       = PROJECT_ROOT / "output" / "oportunidades"
INFORME   = OUT / "informe_oportunidades.md"
HISTORIAL = OUT / "historial.json"
OUT.mkdir(parents=True, exist_ok=True)

TS = datetime.now().strftime("%Y-%m-%d %H:%M")

def sep(t): print(f"\n{'='*58}\n  {t}\n{'='*58}")
def ok(t):  print(f"  [OK] {t}")
def info(t):print(f"  [..] {t}")
def warn(t):print(f"  [!]  {t}")


# ═══════════════════════════════════════════════════════════════════════════
#  NICHOS A INVESTIGAR  (rotamos por bloques en cada run)
# ═══════════════════════════════════════════════════════════════════════════
NICHOS = [
    # (id, nombre, queries_de_mercado)
    # Queries diseñadas para retornar paginas comerciales con precios reales
    ("contabilidad_autonomos",
     "Software contabilidad para autonomos espana",
     ["holded billin contasimple precio plan mensual autonomo",
      "comparativa software facturacion autonomos espana precio 2024",
      "programa facturacion autonomo espana cuanto cuesta mes"]),

    ("formacion_online_espana",
     "Cursos online para profesionales hispanohablantes",
     ["hotmart teachable udemy curso online espana precio venta 2024",
      "cuanto cobrar curso online espana precio medio formacion",
      "vender formacion online espana ingresos autonomo rentable"]),

    ("herramientas_freelance",
     "Herramientas SaaS para freelancers hispanohablantes",
     ["herramienta SaaS freelance espana precio suscripcion mensual",
      "app gestion clientes freelance espana precio plan tarifa",
      "mejor CRM autonomo espana precio comparativa alternativa barata"]),

    ("contenido_digital_pymes",
     "Servicios de contenido digital para pymes espanolas",
     ["cuanto cobra un copywriter freelance espana precio hora 2024",
      "servicio community manager freelance espana tarifa mensual",
      "agencia contenidos pymes espana precio paquete mensual"]),

    ("consultoria_ia_pymes",
     "Consultoria IA para pymes y autonomos",
     ["consultoria inteligencia artificial pymes espana precio servicio",
      "automatizacion IA para negocio espana cuanto cuesta proyecto",
      "freelance IA automatizacion espana tarifa hora proyecto"]),

    ("productos_digitales_autonomos",
     "Productos digitales descargables para autonomos",
     ["vender plantillas digitales espana gumroad precio descarga",
      "ebook guia autonomos espana cuanto cobrar precio venta digital",
      "pack recursos plantillas autonomo espana precio mercado"]),

    ("comunidades_pago_espana",
     "Comunidades de pago online para profesionales espanoles",
     ["skool comunidad pago espana precio mes membresia",
      "membership site espana profesionales cuanto cobran mensualidad",
      "comunidad online pago espana ejemplos precio suscripcion"]),

    ("traduccion_localizacion",
     "Servicios de traduccion y localizacion para empresas",
     ["tarifa traductor freelance espana precio palabra hora 2024",
      "localizacion contenido digital espana precio proyecto empresa",
      "servicio traduccion espana autonomo cuanto cobrar por pagina"]),

    ("coaching_autonomos",
     "Coaching y mentoría para autónomos y emprendedores",
     ["precio sesion coaching autonomos espana cuanto cobran 2024",
      "mentoria online emprendedores espana tarifa programa precio",
      "coach autonomos espana cuanto gana precio mensualidad"]),

    ("ecommerce_nicho",
     "Tiendas online de nicho con baja competencia",
     ["nicho tienda online espana baja competencia alta demanda rentable",
      "dropshipping espana nicho productos digitales precio margen 2024",
      "productos nicho espana sin explotar tienda online oportunidad"]),
]

# ── Leer historial para no repetir nichos ya investigados ──────────────────
historial: dict = {}
if HISTORIAL.exists():
    try:
        historial = json.loads(HISTORIAL.read_text(encoding="utf-8"))
    except Exception:
        historial = {}

nichos_pendientes = [n for n in NICHOS if n[0] not in historial]
if not nichos_pendientes:
    warn("Todos los nichos ya investigados. Reiniciando ciclo.")
    historial = {}
    nichos_pendientes = NICHOS[:]

# Investigar los primeros 3 nichos de esta ronda
NICHOS_RONDA = nichos_pendientes[:3]


# ═══════════════════════════════════════════════════════════════════════════
#  FUNCIONES DE INVESTIGACION
# ═══════════════════════════════════════════════════════════════════════════

_DOMINIOS_IGNORAR = {
    "wikipedia.org","wikihow.com","rae.es","ayuntamiento","boe.es",
    "minhafp.gob","agenciatributaria","seguridad-social","youtube.com",
    "pinterest.","tiktok.","leroymerlin","bricomart",
    "manomano","ikea.","elcorteingles","fnac.","pccomponentes",
}

def _url_ok(url: str) -> bool:
    u = url.lower()
    return not any(d in u for d in _DOMINIOS_IGNORAR)

_FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}
_MAX_PAGE_BYTES = 120_000  # 120 KB max por pagina

def _fetch_text(url: str) -> str:
    """Descarga el texto plano de una URL (sin JS). Max 120 KB."""
    try:
        req = urllib.request.Request(url, headers=_FETCH_HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read(_MAX_PAGE_BYTES).decode("utf-8", errors="replace")
        # Eliminar tags HTML y decodificar entidades
        raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S|re.I)
        raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S|re.I)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
        raw = re.sub(r"\s+", " ", raw)
        return raw.lower()
    except Exception:
        return ""

def _buscar(query: str, n: int = 8) -> list[dict]:
    if not _DDGS_OK:
        return []
    try:
        results = DDGS(timeout=15).text(query, max_results=n, region="es-es")
        return [r for r in (results or []) if _url_ok(r.get("href",""))]
    except Exception as e:
        warn(f"DDG error: {e}")
        return []

def _enriquecer_con_fetch(resultados: list[dict], max_fetch: int = 3) -> str:
    """Descarga las primeras max_fetch URLs para extraer texto completo con precios."""
    textos_extra = []
    fetched = 0
    for r in resultados:
        if fetched >= max_fetch:
            break
        url = r.get("href","")
        if not url or not _url_ok(url):
            continue
        texto = _fetch_text(url)
        if texto:
            textos_extra.append(texto[:8000])  # max 8K chars por pagina
            fetched += 1
        time.sleep(0.5)
    return " ".join(textos_extra)

def _dominio_libre(nombre: str) -> dict[str, bool]:
    """Comprueba si .com .es .io están libres via DNS."""
    libre = {}
    base = re.sub(r"[^a-z0-9]", "", nombre.lower())[:15]
    for tld in (".com", ".es", ".io"):
        dom = base + tld
        try:
            socket.getaddrinfo(dom, None)
            libre[tld] = False
        except socket.gaierror:
            libre[tld] = True
        time.sleep(0.3)
    return libre

def _puntuar_oportunidad(resultados: list[dict], nombre: str, texto_paginas: str = "") -> dict:
    """Analisis heuristico: extrae señales de demanda, competencia y precio."""
    textos = " ".join(
        (r.get("title","") + " " + r.get("body","")).lower()
        for r in resultados
    )
    # Combinar snippets DDG + contenido completo de paginas
    textos = textos + " " + texto_paginas
    # Normalizar espacios no separables y separadores de miles
    textos = textos.replace("\xa0", " ").replace(" ", " ")

    # Señales de demanda — vocabulario amplio
    palabras_demanda = [
        "busca", "buscan", "necesita", "necesitan", "quiero", "quieren",
        "problema", "problemas", "dificultad", "dificultades",
        "como puedo", "como hacer", "demanda", "solicita", "solicitan",
        "contratar", "contratan", "pagar por", "dispuesto a pagar",
        "cuanto cuesta", "precio de", "coste de", "tarifa", "presupuesto",
        "interesado", "interesados", "busco freelance", "necesito ayuda",
        "clientes buscan", "empresas buscan", "pymes necesitan",
    ]
    demanda = sum(textos.count(p) for p in palabras_demanda)

    # Señales de mercado establecido (= mas competencia)
    competencia = sum([
        textos.count("lider del mercado"), textos.count("mejor plataforma"),
        textos.count("mas usado"), textos.count("referente"),
        textos.count("miles de clientes"), textos.count("empresa consolidada"),
        textos.count("numero 1"), textos.count("top 10"),
    ])

    # Extraccion de precios — multiples patrones para texto web espanol
    _patrones_precio = [
        r"(\d{1,4})[,.]?\d*\s*€",            # 99€ / 19,99€ / 1.500€
        r"€\s*(\d{1,4})",                      # €99
        r"(\d{1,4})\s*euros?",                 # 99 euros / 99 euro
        r"(\d{1,4})\s*eur\b",                  # 99 eur
        r"desde\s*(\d{1,4})",                  # desde 19
        r"(\d{1,4})\s*/\s*mes",               # 49/mes
        r"(\d{1,4})\s*/\s*hora",              # 30/hora
        r"(\d{1,4})\s*/\s*año",               # 199/año
        r"(\d{1,4})\s*/\s*sesion",            # 80/sesion
        r"precio[:\s]+(\d{1,4})",             # precio: 200
        r"tarifa[:\s]+(\d{1,4})",             # tarifa: 50
        r"cobr[ao]\s*(\d{1,4})",              # cobra 45 / cobro 60
        r"(\d{1,4})\s*\$",                    # 99$
    ]
    precios_raw = []
    for pat in _patrones_precio:
        precios_raw.extend(re.findall(pat, textos))
    precios = sorted(set(int(p) for p in precios_raw if 5 <= int(p) <= 9999))
    precio_medio = int(sum(precios) / len(precios)) if precios else 0

    # Señales de nicho sin cubrir bien
    palabras_gap = [
        "no existe", "falta una", "ninguna opcion", "sin alternativa",
        "alternativa a", "especifico para", "adaptado a", "pensado para",
        "solo para autonomos", "para pymes", "para freelance",
        "hueco de mercado", "oportunidad", "nicho sin explotar",
        "poca competencia", "baja competencia", "sin competidores",
        "mercado emergente", "tendencia al alza", "crecimiento",
    ]
    gap_mercado = sum(textos.count(p) for p in palabras_gap)

    # Puntuacion 0-100
    score = min(100, (
        min(demanda * 2, 35)       +  # max 35 por demanda
        min(gap_mercado * 5, 25)   +  # max 25 por gap de mercado
        min(len(precios) * 2, 20)  +  # max 20 por claridad de precios
        (15 if precio_medio > 50 else 8 if precio_medio > 0 else 0) +
        max(0, 5 - competencia)       # max 5, baja si hay mucha competencia
    ))

    # Extraer menciones de herramientas/competidores
    competidores_conocidos = []
    marcas = ["holded","billin","debitoor","factura","contasimple","anfix",
              "sage","a3","zoho","hubspot","mailchimp","shopify","woocommerce",
              "wordpress","wix","squarespace","notion","asana","trello","slack",
              "udemy","hotmart","teachable","kajabi","skool","patreon","substack"]
    for m in marcas:
        if m in textos:
            competidores_conocidos.append(m)

    return {
        "score": score,
        "demanda_señales": demanda,
        "gap_mercado": gap_mercado,
        "precio_medio_eur": precio_medio,
        "precios_encontrados": precios[:8],
        "competidores": competidores_conocidos[:6],
        "n_resultados": len(resultados),
    }

def _nivel(score: int) -> str:
    if score >= 65: return "ALTA"
    if score >= 35: return "MEDIA"
    return "BAJA"


# ═══════════════════════════════════════════════════════════════════════════
#  RONDA DE INVESTIGACION
# ═══════════════════════════════════════════════════════════════════════════
sep(f"RONDA DE INVESTIGACION — {TS}")
print(f"  Nichos en esta ronda: {len(NICHOS_RONDA)}/{len(NICHOS)} totales")
print(f"  Investigados antes:   {len(historial)}")

hallazgos = []

for nid, nombre, queries in NICHOS_RONDA:
    sep(f"Nicho: {nombre}")
    todos_resultados = []
    for q in queries:
        info(f"Buscando: {q[:60]}...")
        res = _buscar(q, n=6)
        todos_resultados.extend(res)
        ok(f"{len(res)} resultados")
        time.sleep(1.2)  # respetar rate limit DDG

    # Enriquecer con contenido completo de paginas (para extraer precios reales)
    info("Obteniendo contenido de paginas...")
    texto_paginas = _enriquecer_con_fetch(todos_resultados[:6], max_fetch=3)
    ok(f"Contenido extra: {len(texto_paginas)} chars")

    puntuacion = _puntuar_oportunidad(todos_resultados, nombre, texto_paginas)

    # Validar dominios
    info("Validando dominios...")
    dominios = _dominio_libre(nid)
    dominios_libres = [tld for tld, libre in dominios.items() if libre]

    viabilidad = _nivel(puntuacion["score"])

    hallazgo = {
        "id": nid,
        "nombre": nombre,
        "score": puntuacion["score"],
        "viabilidad": viabilidad,
        "precio_medio_eur": puntuacion["precio_medio_eur"],
        "precios_rango": puntuacion["precios_encontrados"],
        "demanda": puntuacion["demanda_señales"],
        "gap_mercado": puntuacion["gap_mercado"],
        "competidores": puntuacion["competidores"],
        "dominios_libres": dominios_libres,
        "n_resultados": puntuacion["n_resultados"],
        "ts": TS,
    }
    hallazgos.append(hallazgo)
    historial[nid] = hallazgo

    # Resumen por consola
    print(f"\n  Score:      {puntuacion['score']}/100  [{viabilidad}]")
    print(f"  Precio med: {puntuacion['precio_medio_eur']} EUR")
    if puntuacion["precios_encontrados"]:
        print(f"  Rango:      {min(puntuacion['precios_encontrados'])}–{max(puntuacion['precios_encontrados'])} EUR")
    print(f"  Dominios:   {', '.join(dominios_libres) if dominios_libres else 'todos ocupados'}")
    if puntuacion["competidores"]:
        print(f"  Competencia:{', '.join(puntuacion['competidores'][:4])}")

# ── Guardar historial JSON ──────────────────────────────────────────────────
HISTORIAL.write_text(json.dumps(historial, ensure_ascii=False, indent=2), encoding="utf-8")
ok(f"Historial guardado ({len(historial)} nichos)")


# ═══════════════════════════════════════════════════════════════════════════
#  GENERAR INFORME ACUMULATIVO
# ═══════════════════════════════════════════════════════════════════════════
sep("INFORME ACUMULATIVO DE OPORTUNIDADES")

todos = sorted(historial.values(), key=lambda x: x["score"], reverse=True)

lineas = [
    f"# Informe de Oportunidades de Negocio",
    f"",
    f"Ultima actualizacion: {TS}  |  Nichos investigados: {len(todos)}/{len(NICHOS)}",
    f"",
    f"---",
    f"",
    f"## Ranking de Oportunidades",
    f"",
    f"| # | Oportunidad | Score | Viabilidad | Precio medio | Dominios libres |",
    f"|---|-------------|-------|------------|--------------|-----------------|",
]

for i, h in enumerate(todos, 1):
    dom = ", ".join(h.get("dominios_libres", [])) or "–"
    precio = f"{h['precio_medio_eur']} EUR" if h["precio_medio_eur"] else "–"
    lineas.append(
        f"| {i} | {h['nombre']} | {h['score']}/100 | {h['viabilidad']} | {precio} | {dom} |"
    )

lineas += ["", "---", "", "## Detalle por oportunidad", ""]

for h in todos:
    lineas += [
        f"### {h['nombre']}  ·  Score {h['score']}/100  [{h['viabilidad']}]",
        f"",
        f"- **Precio de mercado:** {h['precio_medio_eur']} EUR"
          + (f" (rango: {min(h['precios_rango'])}–{max(h['precios_rango'])} EUR)" if len(h.get("precios_rango",[])) > 1 else ""),
        f"- **Señales de demanda:** {h['demanda']}  |  **Gap de mercado:** {h['gap_mercado']}",
        f"- **Dominios disponibles:** {', '.join(h.get('dominios_libres',[])) or 'ninguno libre'}",
        f"- **Competidores detectados:** {', '.join(h.get('competidores',[])) or 'no detectados'}",
        f"- **Resultados analizados:** {h['n_resultados']}",
        f"- **Investigado:** {h['ts']}",
        f"",
    ]

# Top 3 con analisis rapido
top3 = [h for h in todos if h["viabilidad"] in ("ALTA","MEDIA")][:3]
if top3:
    lineas += ["---", "", "## Top oportunidades — Proximos pasos sugeridos", ""]
    for h in top3:
        lineas += [
            f"**{h['nombre']}** (score {h['score']})",
            f"- Precio objetivo: {max(h.get('precios_rango',[0]) or [0])} EUR/mes o {h['precio_medio_eur']} EUR/hora",
            f"- Dominio: registrar {h.get('dominios_libres',['–'])[0] if h.get('dominios_libres') else '–'}",
            f"- Accion: landing page de validacion + lista de espera",
            f"",
        ]

lineas += [
    "---",
    "",
    f"*Generado automaticamente por el equipo Agente007 · {TS}*",
]

INFORME.write_text("\n".join(lineas), encoding="utf-8")
ok(f"Informe guardado: {INFORME}")

# ── Resumen final en consola ────────────────────────────────────────────────
sep("RESUMEN ESTA RONDA")
print(f"\n  Nichos investigados ahora: {len(NICHOS_RONDA)}")
print(f"  Nichos totales acumulados: {len(historial)}/{len(NICHOS)}")
pendientes_restantes = len(NICHOS) - len(historial)
print(f"  Pendientes para proximas rondas: {pendientes_restantes}")
print(f"\n  TOP 3 esta ronda:")
for h in sorted(hallazgos, key=lambda x: x["score"], reverse=True)[:3]:
    dom = h.get("dominios_libres",["–"])[0] if h.get("dominios_libres") else "–"
    print(f"    [{h['viabilidad']:5}] {h['score']:3}/100  {h['nombre']}")
    print(f"           Precio: {h['precio_medio_eur']} EUR  |  Dominio libre: {dom}")

print(f"\n  Informe completo: output/oportunidades/informe_oportunidades.md")
if pendientes_restantes == 0:
    print(f"\n  [*] CICLO COMPLETO — todos los nichos investigados.")
    print(f"      Proxima ronda reinicia con busquedas actualizadas.")

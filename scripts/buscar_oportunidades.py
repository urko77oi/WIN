"""Busqueda continua de oportunidades de negocio viables para autonomos espanoles.

Cada ejecucion investiga un bloque de nichos, valida dominios, puntua
viabilidad con datos reales (sin LLM) y guarda un informe acumulativo.

Puede ejecutarse en bucle: cada run añade hallazgos nuevos al informe.
"""
from __future__ import annotations
import sys, json, re, time, socket
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
    ("contabilidad_autonomos",
     "Software contabilidad para autonomos espana",
     ["software contabilidad autonomos espana 2024 precio",
      "facturacion online autonomos espana alternativas gratuitas",
      "mejor programa facturacion autonomo espana opiniones"]),

    ("formacion_online_espana",
     "Cursos online para profesionales hispanohablantes",
     ["plataformas cursos online espana rentables 2024",
      "nichos formacion online espana demanda alta competencia baja",
      "curso online autonomos espana que se vende mas"]),

    ("herramientas_freelance",
     "Herramientas SaaS para freelancers hispanohablantes",
     ["herramientas productividad freelance espana mas usadas",
      "SaaS dirigido autonomos espana oportunidad mercado",
      "app gestion clientes freelance espana alternativa barata"]),

    ("contenido_digital_pymes",
     "Servicios de contenido digital para pymes espanolas",
     ["servicios marketing contenidos pymes espana demanda 2024",
      "agencia contenidos pequena empresa espana precio mercado",
      "copywriting pymes espana cuanto cobran freelance"]),

    ("consultoria_ia_pymes",
     "Consultoria IA para pymes y autonomos",
     ["consultoria inteligencia artificial pymes espana precio",
      "automatizacion procesos pymes espana servicio freelance",
      "implementar IA negocio pequeno espana coste"]),

    ("productos_digitales_autonomos",
     "Productos digitales descargables para autonomos",
     ["plantillas contratos autonomos espana descarga venta",
      "ebooks guias autonomos espana cuanto se vende",
      "pack recursos autonomo espana mercado digital"]),

    ("comunidades_pago_espana",
     "Comunidades de pago online para profesionales espanoles",
     ["comunidades online pago espana profesionales cuanto cobran",
      "membership site espana nicho rentable 2024",
      "skool comunidad pago espana ejemplos exitosos"]),

    ("traduccion_localizacion",
     "Servicios de traduccion y localizacion para empresas",
     ["servicios traduccion empresas espana freelance tarifa",
      "localizacion contenido digital espana demanda",
      "traduccion tecnica juridica espana precio mercado"]),

    ("coaching_autonomos",
     "Coaching y mentoría para autónomos y emprendedores",
     ["coaching autonomos espana precio sesion mercado",
      "mentoria emprendedores espana plataformas cuanto cobran",
      "programa mentoria online espana profesionales"]),

    ("ecommerce_nicho",
     "Tiendas online de nicho con baja competencia",
     ["tienda online nicho espana baja competencia alta demanda 2024",
      "productos digitales espana nicho sin explotar",
      "dropshipping espana nicho rentable 2024 autonomo"]),
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
    "reddit.com","quora.com","amazon.","pinterest.","facebook.","instagram.",
    "twitter.","x.com","linkedin.com","tiktok.","leroymerlin","bricomart",
    "manomano","ikea.","elcorteingles","fnac.","pccomponentes",
}

def _url_ok(url: str) -> bool:
    u = url.lower()
    return not any(d in u for d in _DOMINIOS_IGNORAR)

def _buscar(query: str, n: int = 8) -> list[dict]:
    if not _DDGS_OK:
        return []
    try:
        results = DDGS(timeout=15).text(query, max_results=n, region="es-es")
        return [r for r in (results or []) if _url_ok(r.get("href",""))]
    except Exception as e:
        warn(f"DDG error: {e}")
        return []

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

def _puntuar_oportunidad(resultados: list[dict], nombre: str) -> dict:
    """Analisis heuristico: extrae señales de demanda, competencia y precio."""
    textos = " ".join(
        (r.get("title","") + " " + r.get("body","")).lower()
        for r in resultados
    )

    # Señales de demanda
    demanda = sum([
        textos.count("buscan"), textos.count("necesitan"),
        textos.count("problema"), textos.count("dificultad"),
        textos.count("quiero"), textos.count("como puedo"),
        textos.count("demanda"), textos.count("solicita"),
    ])

    # Señales de mercado establecido (= mas competencia)
    competencia = sum([
        textos.count("lider del mercado"), textos.count("mejor plataforma"),
        textos.count("mas usado"), textos.count("referente"),
        textos.count("miles de clientes"), textos.count("empresa consolidada"),
    ])

    # Señales de precio (indicador de willingness to pay)
    precios_encontrados = re.findall(r"(\d+)\s*(?:eur|€|euros?)\s*/?\s*(?:mes|hora|año|sesion)?", textos)
    precios = [int(p) for p in precios_encontrados if 5 <= int(p) <= 5000]
    precio_medio = int(sum(precios) / len(precios)) if precios else 0

    # Señales de nicho sin cubrir bien
    gap_mercado = sum([
        textos.count("no existe"), textos.count("falta una"),
        textos.count("ninguna opcion"), textos.count("alternativa"),
        textos.count("especifico para"), textos.count("adaptado a"),
    ])

    # Puntuacion 0-100
    score = min(100, (
        min(demanda * 4, 30)      +  # max 30 por demanda
        min(gap_mercado * 8, 25)  +  # max 25 por gap de mercado
        min(len(precios) * 3, 20) +  # max 20 por claridad de precios
        (15 if precio_medio > 50 else 5 if precio_medio > 0 else 0) +
        max(0, 10 - competencia * 2)  # max 10, baja si hay mucha competencia
    ))

    # Extraer menciones de herramientas/competidores
    competidores_conocidos = []
    marcas = ["holded","billin","debitoor","factura","contasimple","anfix",
              "sage","a3","zoho","hubspot","mailchimp","shopify","woocommerce",
              "wordpress","wix","squarespace","notion","asana","trello","slack"]
    for m in marcas:
        if m in textos:
            competidores_conocidos.append(m)

    return {
        "score": score,
        "demanda_señales": demanda,
        "gap_mercado": gap_mercado,
        "precio_medio_eur": precio_medio,
        "precios_encontrados": sorted(set(precios))[:8],
        "competidores": competidores_conocidos[:6],
        "n_resultados": len(resultados),
    }

def _nivel(score: int) -> str:
    if score >= 70: return "ALTA"
    if score >= 45: return "MEDIA"
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

    puntuacion = _puntuar_oportunidad(todos_resultados, nombre)

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

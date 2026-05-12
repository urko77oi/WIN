"""Herramientas reales que los agentes pueden ejecutar.

Cada herramienta tiene:
  - Definicion JSON (schema para Groq function calling)
  - Implementacion Python

Conjuntos de tools por agente:
  TOOLS_SCOUT     -> buscar_web, leer_pagina, guardar_informe
  TOOLS_DOMENECH  -> leer_informe, listar_informes, crear_archivo, listar_output
  TOOLS_DURRUTI   -> delegar_scout, delegar_domenech, guardar_tarea, listar_tareas
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from shared.logger import PROJECT_ROOT, log_de

log = log_de("herramientas")

OUTPUT_DIR  = PROJECT_ROOT / "output"
MEMORY_DIR  = PROJECT_ROOT / "memory" / "projects"
TASKS_DIR   = PROJECT_ROOT / "tasks" / "pending"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
TASKS_DIR.mkdir(parents=True, exist_ok=True)

# ── Implementaciones ──────────────────────────────────────────────────

def buscar_web(query: str, max_results: int = 6) -> str:
    """DuckDuckGo search — gratuito, sin API key."""
    log.info(f"[buscar_web] {query!r}")
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS(timeout=20)
        resultados = list(ddgs.text(query, max_results=max_results, region="es-es"))
        if not resultados:
            return "No se encontraron resultados."
        lineas = []
        for r in resultados:
            lineas.append(f"### {r.get('title','')}\n{r.get('href','')}\n{r.get('body','')[:300]}")
        return "\n\n".join(lineas)
    except Exception as e:
        return f"Error en busqueda: {e}"


def leer_pagina(url: str) -> str:
    """Descarga y extrae el texto principal de una pagina web."""
    log.info(f"[leer_pagina] {url}")
    try:
        import requests
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0 (compatible; FORRARSE-Scout/1.0)"}
        resp = requests.get(url, timeout=12, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        texto = soup.get_text(separator="\n", strip=True)
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        return texto[:1500]
    except Exception as e:
        return f"Error al leer {url}: {e}"


def guardar_informe(nombre: str, contenido: str) -> str:
    """Guarda un informe markdown en memory/projects/."""
    slug = re.sub(r"[^\w-]", "-", nombre.lower())[:50]
    ts   = datetime.now().strftime("%Y%m%d_%H%M")
    path = MEMORY_DIR / f"{ts}_{slug}.md"
    path.write_text(f"# {nombre}\n\n{contenido}", encoding="utf-8")
    log.info(f"[guardar_informe] {path.name}")
    return f"Informe guardado: {path.name}"


def leer_informe(nombre_archivo: str) -> str:
    """Lee un informe de memory/projects/ por nombre de archivo."""
    path = MEMORY_DIR / nombre_archivo
    if not path.exists():
        # Intenta buscar por coincidencia parcial
        candidatos = sorted(MEMORY_DIR.glob(f"*{nombre_archivo}*"))
        if not candidatos:
            return f"No se encontro: {nombre_archivo}"
        path = candidatos[-1]
    return path.read_text(encoding="utf-8")


def listar_informes() -> str:
    """Lista todos los informes disponibles en memory/projects/."""
    archivos = sorted(MEMORY_DIR.glob("*.md"))
    if not archivos:
        return "No hay informes guardados todavia."
    return "\n".join(f.name for f in archivos)


def crear_archivo(ruta: str, contenido: str) -> str:
    """Crea un archivo en output/. La ruta es relativa a output/."""
    path = OUTPUT_DIR / ruta.lstrip("/\\")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contenido, encoding="utf-8")
    log.info(f"[crear_archivo] {path}")
    return f"Archivo creado: output/{ruta} ({len(contenido)} chars)"


def listar_output() -> str:
    """Lista los archivos generados en output/."""
    archivos = sorted(OUTPUT_DIR.rglob("*"))
    archivos = [f for f in archivos if f.is_file()]
    if not archivos:
        return "output/ esta vacio."
    return "\n".join(str(f.relative_to(OUTPUT_DIR)) for f in archivos)


def generar_srt(script: str, nombre: str, segundos_por_linea: float = 4.0) -> str:
    """Convierte un script de texto a formato SRT (subtitulos)."""
    lineas = [l.strip() for l in script.splitlines()
              if l.strip() and not l.strip().startswith("[") and not l.strip().startswith("#")]
    bloques = []
    t = 0.0
    for i, linea in enumerate(lineas, 1):
        palabras = linea.split()
        dur = max(segundos_por_linea, len(palabras) * 0.4)
        def _ts(s: float) -> str:
            h = int(s // 3600); m = int((s % 3600) // 60)
            se = int(s % 60); ms = int((s - int(s)) * 1000)
            return f"{h:02d}:{m:02d}:{se:02d},{ms:03d}"
        bloques.append(f"{i}\n{_ts(t)} --> {_ts(t + dur)}\n{linea}\n")
        t += dur
    contenido = "\n".join(bloques)
    slug = re.sub(r"[^\w-]", "-", nombre.lower())[:40]
    path = OUTPUT_DIR / "skool" / "videos" / f"{slug}.srt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contenido, encoding="utf-8")
    log.info(f"[generar_srt] {path.name} ({len(bloques)} bloques)")
    return f"SRT generado: output/skool/videos/{slug}.srt ({len(bloques)} lineas)"


def generar_descripcion_youtube(titulo: str, script: str, tags: str = "") -> str:
    """Genera descripcion SEO optimizada para YouTube a partir de un script."""
    resumen = " ".join(script.split()[:80]) + "..."
    tags_lista = [t.strip() for t in tags.split(",") if t.strip()]
    tags_str = " ".join(f"#{t.replace(' ','')}" for t in tags_lista[:10])
    descripcion = f"""{titulo}

{resumen}

━━━━━━━━━━━━━━━━━━━━━━━━━
EN ESTE VIDEO:
(00:00) Introduccion
(00:30) El problema
(01:30) La solucion
(03:00) Paso a paso
(05:00) Conclusion + CTA

━━━━━━━━━━━━━━━━━━━━━━━━━
RECURSOS MENCIONADOS:
→ Comunidad gratuita: [LINK SKOOL]
→ Newsletter semanal: [LINK]

━━━━━━━━━━━━━━━━━━━━━━━━━
UNETE A LA COMUNIDAD GRATIS:
Autonomos Espana en Skool → [LINK]
+500 autonomos espanoles ya dentro

━━━━━━━━━━━━━━━━━━━━━━━━━
{tags_str}

#autonomos #autonomosespana #freelance #negociodigital #emprendimiento
"""
    slug = re.sub(r"[^\w-]", "-", titulo.lower())[:40]
    path = OUTPUT_DIR / "skool" / "videos" / f"desc_{slug}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(descripcion, encoding="utf-8")
    log.info(f"[generar_descripcion_youtube] {path.name}")
    return f"Descripcion YouTube guardada: output/skool/videos/desc_{slug}.txt"


def exportar_csv(filas: list, nombre: str, cabeceras: list | None = None) -> str:
    """Exporta datos como CSV (para importar en Buffer, Later, Notion...)."""
    import csv, io
    buf = io.StringIO()
    writer = csv.writer(buf)
    if cabeceras:
        writer.writerow(cabeceras)
    for fila in filas:
        writer.writerow(fila if isinstance(fila, list) else [fila])
    slug = re.sub(r"[^\w-]", "-", nombre.lower())[:40]
    path = OUTPUT_DIR / "skool" / f"{slug}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(buf.getvalue(), encoding="utf-8-sig")
    log.info(f"[exportar_csv] {path.name} ({len(filas)} filas)")
    return f"CSV exportado: output/skool/{slug}.csv ({len(filas)} filas)"


def crear_thumbnail_html(titulo: str, subtitulo: str, nombre: str,
                          color_fondo: str = "#1a3a5c",
                          color_acento: str = "#f4821f") -> str:
    """Genera un thumbnail 1280x720 en HTML listo para captura de pantalla."""
    slug = re.sub(r"[^\w-]", "-", nombre.lower())[:40]
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  body {{ margin:0; font-family:-apple-system,"Segoe UI",Roboto,sans-serif; }}
  .thumb {{
    width:1280px; height:720px; background:{color_fondo};
    display:flex; flex-direction:column;
    justify-content:center; align-items:flex-start;
    padding:80px; box-sizing:border-box; position:relative; overflow:hidden;
  }}
  .thumb::before {{
    content:""; position:absolute; right:-100px; top:-100px;
    width:500px; height:500px; border-radius:50%;
    background:{color_acento}; opacity:0.15;
  }}
  .thumb::after {{
    content:""; position:absolute; right:80px; bottom:40px;
    width:300px; height:300px; border-radius:50%;
    background:{color_acento}; opacity:0.08;
  }}
  .tag {{ background:{color_acento}; color:#fff; font-size:22px; font-weight:700;
          padding:8px 20px; border-radius:6px; margin-bottom:24px; display:inline-block; }}
  h1 {{ color:#fff; font-size:72px; font-weight:800; line-height:1.1;
        margin:0 0 20px; max-width:900px; letter-spacing:-2px; }}
  p  {{ color:rgba(255,255,255,0.75); font-size:32px; margin:0; max-width:800px; }}
  .logo {{ position:absolute; bottom:40px; left:80px;
           color:rgba(255,255,255,0.5); font-size:22px; font-weight:600; }}
</style></head>
<body>
<div class="thumb">
  <div class="tag">Autonomos Espana</div>
  <h1>{titulo}</h1>
  <p>{subtitulo}</p>
  <div class="logo">autonomosespana.es</div>
</div>
</body></html>"""
    path = OUTPUT_DIR / "skool" / "thumbnails" / f"{slug}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    log.info(f"[crear_thumbnail_html] {path.name}")
    return f"Thumbnail HTML: output/skool/thumbnails/{slug}.html (abre en navegador y captura)"


def crear_post_imagen_html(titulo: str, cuerpo: str, nombre: str,
                            formato: str = "cuadrado",
                            color1: str = "#1a3a5c",
                            color2: str = "#f4821f") -> str:
    """Genera imagen de post para Instagram/LinkedIn en HTML (1080x1080 cuadrado o 1080x1350)."""
    alto = "1080px" if formato == "cuadrado" else "1350px"
    slug = re.sub(r"[^\w-]", "-", nombre.lower())[:40]
    puntos = [l.strip().lstrip("-→•").strip() for l in cuerpo.splitlines()
              if l.strip() and len(l.strip()) > 5][:5]
    items_html = "".join(
        f'<div class="item"><span class="num">{i:02d}</span><span>{p}</span></div>'
        for i, p in enumerate(puntos, 1)
    )
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  body {{ margin:0; font-family:-apple-system,"Segoe UI",Roboto,sans-serif; }}
  .post {{
    width:1080px; height:{alto}; background:{color1};
    display:flex; flex-direction:column; justify-content:space-between;
    padding:80px; box-sizing:border-box;
  }}
  .header {{ color:rgba(255,255,255,0.5); font-size:24px; font-weight:600; }}
  h2 {{ color:#fff; font-size:58px; font-weight:800; line-height:1.15;
        margin:30px 0 40px; letter-spacing:-1px; }}
  .item {{ display:flex; align-items:flex-start; gap:20px; margin-bottom:28px; }}
  .num {{ color:{color2}; font-size:36px; font-weight:800; min-width:50px; }}
  .item span:last-child {{ color:rgba(255,255,255,0.9); font-size:30px; line-height:1.4; }}
  .footer {{ color:rgba(255,255,255,0.4); font-size:22px; border-top:1px solid rgba(255,255,255,0.15);
             padding-top:24px; }}
</style></head>
<body>
<div class="post">
  <div class="header">@autonomosespana</div>
  <div>
    <h2>{titulo}</h2>
    {items_html}
  </div>
  <div class="footer">Autonomos Espana · Comunidad gratuita en Skool</div>
</div>
</body></html>"""
    path = OUTPUT_DIR / "skool" / "posts_img" / f"{slug}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    log.info(f"[crear_post_imagen_html] {path.name}")
    return f"Post imagen: output/skool/posts_img/{slug}.html ({formato} 1080px)"


def guardar_tarea(descripcion: str, agente: str = "pendiente") -> str:
    """Guarda una tarea en tasks/pending/."""
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = TASKS_DIR / f"{ts}_{agente}.md"
    path.write_text(f"# Tarea\n\n{descripcion}\n\nAgente: {agente}\n", encoding="utf-8")
    log.info(f"[guardar_tarea] {path.name}")
    return f"Tarea guardada: {path.name}"


def listar_tareas() -> str:
    """Lista las tareas pendientes."""
    tareas = sorted(TASKS_DIR.glob("*.md"))
    if not tareas:
        return "No hay tareas pendientes."
    return "\n".join(f.name for f in tareas)


# ── Schemas JSON para Groq function calling ───────────────────────────

def _schema(name: str, desc: str, props: dict, required: list) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        },
    }

_STR = {"type": "string"}

TOOLS_SCOUT = [
    _schema("buscar_web",     "Busca informacion en internet con DuckDuckGo (gratis, sin API key).",
            {"query": {**_STR, "description": "Terminos de busqueda"}}, ["query"]),
    _schema("leer_pagina",    "Descarga y extrae el texto de una URL.",
            {"url": {**_STR, "description": "URL completa a leer"}}, ["url"]),
    _schema("guardar_informe","Guarda el informe final en memory/projects/ como archivo markdown.",
            {"nombre": {**_STR, "description": "Titulo del informe"},
             "contenido": {**_STR, "description": "Contenido completo en markdown"}}, ["nombre", "contenido"]),
]

TOOLS_DOMENECH = [
    _schema("listar_informes","Lista los informes disponibles de Scout en memory/projects/.", {}, []),
    _schema("leer_informe",   "Lee un informe de Scout por nombre de archivo.",
            {"nombre_archivo": {**_STR, "description": "Nombre del archivo .md"}}, ["nombre_archivo"]),
    _schema("crear_archivo",  "Crea un archivo en output/ (HTML, CSS, JS, md, etc.).",
            {"ruta": {**_STR, "description": "Ruta relativa dentro de output/"},
             "contenido": {**_STR, "description": "Contenido completo del archivo"}}, ["ruta", "contenido"]),
    _schema("listar_output",  "Lista los archivos ya creados en output/.", {}, []),
]

TOOLS_DURRUTI = [
    _schema("listar_informes","Lista los informes de Scout disponibles.", {}, []),
    _schema("leer_informe",   "Lee un informe especifico de Scout.",
            {"nombre_archivo": {**_STR, "description": "Nombre del archivo .md"}}, ["nombre_archivo"]),
    _schema("listar_tareas",  "Lista las tareas pendientes en tasks/pending/.", {}, []),
    _schema("guardar_tarea",  "Guarda una tarea pendiente para el equipo.",
            {"descripcion": {**_STR, "description": "Descripcion detallada de la tarea"},
             "agente": {**_STR, "description": "Agente responsable: scout, domenech o durruti"}},
            ["descripcion", "agente"]),
    _schema("listar_output",  "Lista los archivos generados por Domenech.", {}, []),
]

# ── Dispatcher ────────────────────────────────────────────────────────

_IMPL: dict[str, callable] = {
    "buscar_web":                buscar_web,
    "leer_pagina":               leer_pagina,
    "guardar_informe":           guardar_informe,
    "leer_informe":              leer_informe,
    "listar_informes":           listar_informes,
    "crear_archivo":             crear_archivo,
    "listar_output":             listar_output,
    "guardar_tarea":             guardar_tarea,
    "listar_tareas":             listar_tareas,
    "generar_srt":               generar_srt,
    "generar_descripcion_youtube": generar_descripcion_youtube,
    "exportar_csv":              exportar_csv,
    "crear_thumbnail_html":      crear_thumbnail_html,
    "crear_post_imagen_html":    crear_post_imagen_html,
}


def openai_to_anthropic(tool: dict) -> dict:
    """Convierte schema OpenAI function-calling a formato Anthropic tools."""
    fn = tool.get("function", tool)
    return {
        "name": fn["name"],
        "description": fn.get("description", ""),
        "input_schema": fn.get("parameters", {"type": "object", "properties": {}, "required": []}),
    }


def ejecutar(nombre: str, argumentos: str | dict | None) -> str:
    """Ejecuta una herramienta por nombre con sus argumentos JSON."""
    if argumentos is None:
        argumentos = {}
    elif isinstance(argumentos, str):
        try:
            argumentos = json.loads(argumentos)
        except json.JSONDecodeError:
            argumentos = {}
    if not isinstance(argumentos, dict):
        argumentos = {}
    fn = _IMPL.get(nombre)
    if fn is None:
        return f"Herramienta desconocida: {nombre}"
    try:
        return fn(**argumentos)
    except Exception as e:
        log.error(f"[{nombre}] Error: {e}")
        return f"Error ejecutando {nombre}: {e}"

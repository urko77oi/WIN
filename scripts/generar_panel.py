"""Genera panel de control HTML estático con el estado del equipo.

Guarda en: C:/Users/marct/OneDrive/Escritorio/panel_forrarse.html
Se puede abrir con doble clic. Se regenera junto con los PDFs (cada 3h).
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

MEMORY_DIR  = PROJECT_ROOT / "memory" / "projects"
OUTPUT_DIR  = PROJECT_ROOT / "output"
TASKS_DIR   = PROJECT_ROOT / "tasks" / "pending"
DESTINO     = Path(r"C:\Users\marct\OneDrive\Escritorio\panel_forrarse.html")

TS = datetime.now().strftime("%d/%m/%Y %H:%M")


def _leer_modo_llm() -> str:
    env = PROJECT_ROOT / ".env"
    try:
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("LLM_MODE="):
                val = line.split("=", 1)[1].strip().lower()
                return "Real (Claude)" if val == "real" else "Mock (sin creditos)"
    except Exception:
        pass
    return "Mock"


def _ultima_ejecucion() -> str:
    """Fecha de la última modificación del informe más reciente."""
    informes = sorted(MEMORY_DIR.glob("*.md"), reverse=True)
    if not informes:
        return "Nunca"
    ts = informes[0].stat().st_mtime
    return datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M")


def _leer(path: Path, max_chars: int = 500) -> str:
    try:
        return path.read_text(encoding="utf-8")[:max_chars].replace("<", "&lt;").replace(">", "&gt;")
    except Exception:
        return ""


def _informes() -> list[Path]:
    return sorted(MEMORY_DIR.glob("*.md"), reverse=True)


def _outputs() -> list[Path]:
    return [f for f in sorted(OUTPUT_DIR.rglob("*")) if f.is_file()]


def _tareas() -> list[Path]:
    return sorted(TASKS_DIR.glob("*.md"))


def _tarjeta_informe(p: Path) -> str:
    nombre = p.name
    fecha = nombre[:13].replace("_", " ") if len(nombre) > 13 else nombre
    contenido = _leer(p, 300)
    return f"""
    <div class="card">
      <div class="card-tag tag-scout">Scout</div>
      <h3>{nombre}</h3>
      <p class="fecha">{fecha}</p>
      <pre class="snippet">{contenido}</pre>
    </div>"""


def _tarjeta_output(f: Path) -> str:
    rel = str(f.relative_to(OUTPUT_DIR))
    size = f.stat().st_size
    ext = f.suffix.lower()
    tag = "HTML" if ext == ".html" else ext.lstrip(".").upper() or "FILE"
    return f"""
    <div class="card card-sm">
      <div class="card-tag tag-domenech">Domenech</div>
      <h3>{rel}</h3>
      <p class="fecha">{size:,} bytes</p>
    </div>"""


def _tarjeta_tarea(t: Path) -> str:
    contenido = _leer(t, 200)
    return f"""
    <div class="card card-sm">
      <div class="card-tag tag-durruti">Durruti</div>
      <h3>{t.name}</h3>
      <pre class="snippet">{contenido}</pre>
    </div>"""


def generar() -> None:
    informes = _informes()
    outputs  = _outputs()
    tareas   = _tareas()

    bloques_informes = "\n".join(_tarjeta_informe(p) for p in informes[:10])
    bloques_outputs  = "\n".join(_tarjeta_output(f) for f in outputs[:20])
    bloques_tareas   = "\n".join(_tarjeta_tarea(t) for t in tareas) or \
                       '<p class="empty">Sin tareas pendientes</p>'

    modo_llm   = _leer_modo_llm()
    ultima_ej  = _ultima_ejecucion()
    color_modo = "#10b981" if "Real" in modo_llm else "#f59e0b"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="180">
<title>FORRARSE — Panel de Control</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --azul: #1a3a5c; --naranja: #f4821f; --verde: #10b981;
    --amarillo: #f59e0b; --fondo: #f0f4f8; --blanco: #fff;
    --fuente: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  body {{ font-family: var(--fuente); background: var(--fondo); color: #1f2937; }}

  header {{
    background: var(--azul);
    color: #fff;
    padding: 1.2rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  header h1 {{ font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px; }}
  header h1 span {{ color: var(--naranja); }}
  .ts {{ font-size: 0.82rem; opacity: 0.7; }}

  .stats {{
    display: flex;
    gap: 1rem;
    padding: 1.2rem 2rem;
    background: var(--azul);
    border-top: 1px solid rgba(255,255,255,0.1);
  }}
  .stat {{
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    color: #fff;
    text-align: center;
    min-width: 110px;
  }}
  .stat .num {{ font-size: 1.8rem; font-weight: 800; color: var(--naranja); }}
  .stat .lbl {{ font-size: 0.75rem; opacity: 0.8; }}

  .seccion {{ padding: 1.5rem 2rem; }}
  .seccion h2 {{
    font-size: 1rem;
    font-weight: 700;
    color: var(--azul);
    margin-bottom: 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--naranja);
    display: inline-block;
  }}

  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }}

  .card {{
    background: var(--blanco);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    position: relative;
    overflow: hidden;
  }}
  .card-sm {{ min-height: auto; }}
  .card h3 {{ font-size: 0.85rem; font-weight: 600; margin: 0.5rem 0 0.3rem; word-break: break-all; }}
  .fecha {{ font-size: 0.75rem; color: #9ca3af; margin-bottom: 0.5rem; }}
  .snippet {{
    font-size: 0.75rem;
    color: #4b5563;
    background: #f9fafb;
    border-radius: 4px;
    padding: 0.5rem;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 100px;
    overflow: hidden;
    font-family: inherit;
  }}

  .card-tag {{
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .tag-scout   {{ background: #dbeafe; color: #1d4ed8; }}
  .tag-domenech {{ background: #d1fae5; color: #065f46; }}
  .tag-durruti {{ background: #fef3c7; color: #92400e; }}

  .empty {{ color: #9ca3af; font-size: 0.9rem; font-style: italic; }}

  footer {{
    text-align: center;
    padding: 1rem;
    font-size: 0.78rem;
    color: #9ca3af;
  }}
</style>
</head>
<body>

<header>
  <h1>FORRARSE<span>.</span> Panel de Control</h1>
  <span class="ts">Actualizado: {TS} · Se refresca cada 3 min</span>
</header>

<div class="stats">
  <div class="stat"><div class="num">{len(informes)}</div><div class="lbl">Informes Scout</div></div>
  <div class="stat"><div class="num">{len(outputs)}</div><div class="lbl">Archivos output</div></div>
  <div class="stat"><div class="num">{len(tareas)}</div><div class="lbl">Tareas pendientes</div></div>
  <div class="stat"><div class="num" style="font-size:1rem;color:{color_modo}">{modo_llm}</div><div class="lbl">Modo LLM</div></div>
  <div class="stat"><div class="num" style="font-size:0.85rem">{ultima_ej}</div><div class="lbl">Ultima ejecucion Scout</div></div>
</div>

<section class="seccion">
  <h2>📊 Informes Scout ({len(informes)})</h2>
  <div class="grid">
    {bloques_informes or '<p class="empty">Sin informes todavía</p>'}
  </div>
</section>

<section class="seccion">
  <h2>🏗️ Archivos Domenech ({len(outputs)})</h2>
  <div class="grid">
    {bloques_outputs or '<p class="empty">output/ vacío</p>'}
  </div>
</section>

<section class="seccion">
  <h2>📋 Tareas Durruti ({len(tareas)})</h2>
  <div class="grid">
    {bloques_tareas}
  </div>
</section>

<footer>FORRARSE · Sistema multiagente · {TS}</footer>
</body>
</html>"""

    DESTINO.write_text(html, encoding="utf-8")
    print(f"[OK] Panel generado: {DESTINO.name} ({DESTINO.stat().st_size:,} bytes)")


if __name__ == "__main__":
    generar()

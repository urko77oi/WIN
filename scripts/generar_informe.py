"""Genera PDFs de estado en el escritorio cada vez que se ejecuta.

Archivos generados en C:/Users/marct/OneDrive/Escritorio/informe/:
  informe_general.pdf    — resumen global + ultimas 10 propuestas
  informe_scout.pdf      — informes de investigacion guardados
  informe_domenech.pdf   — archivos generados en output/
  informe_durruti.pdf    — tareas y actividad del CEO

No llama a Groq — solo lee el estado actual del disco.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fpdf import FPDF
from fpdf.enums import XPos, YPos

INFORME_DIR = Path(r"C:\Users\marct\OneDrive\Escritorio\informe")
INFORME_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_DIR = PROJECT_ROOT / "memory" / "projects"
OUTPUT_DIR  = PROJECT_ROOT / "output"
TASKS_DIR   = PROJECT_ROOT / "tasks" / "pending"

TS = datetime.now().strftime("%d/%m/%Y %H:%M")


# ── Helpers PDF ──────────────────────────────────────────────────────

def _nuevo_pdf(titulo: str) -> FPDF:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Generado: {TS}  |  FORRARSE - Sistema multiagente", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)
    return pdf


def _seccion(pdf: FPDF, texto: str) -> None:
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_fill_color(230, 240, 255)
    pdf.cell(0, 8, texto, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(2)


def _parrafo(pdf: FPDF, texto: str, size: int = 10) -> None:
    """Escribe texto con salto de linea, filtrando caracteres no latin-1."""
    texto_safe = texto.encode("latin-1", errors="replace").decode("latin-1")
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(0, 5, texto_safe)


def _leer_md(path: Path, max_chars: int = 3000) -> str:
    try:
        return path.read_text(encoding="utf-8")[:max_chars]
    except Exception:
        return "(no se pudo leer)"


def _informes_recientes(n: int = 5) -> list[Path]:
    return sorted(MEMORY_DIR.glob("*.md"), reverse=True)[:n]


# ── PDFs individuales ────────────────────────────────────────────────

def pdf_scout() -> None:
    pdf = _nuevo_pdf("Scout - Analista de Oportunidades")
    informes = _informes_recientes(8)

    _seccion(pdf, f"Informes guardados ({len(list(MEMORY_DIR.glob('*.md')))} total)")
    if not informes:
        _parrafo(pdf, "Sin informes todavia.")
    else:
        for p in informes:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, p.name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            contenido = _leer_md(p, 2000)
            _parrafo(pdf, contenido, 9)
            pdf.ln(4)

    out = INFORME_DIR / "informe_scout.pdf"
    pdf.output(str(out))
    print(f"[OK] {out.name}")


def pdf_domenech() -> None:
    pdf = _nuevo_pdf("Domenech - Constructor")

    archivos = sorted(OUTPUT_DIR.rglob("*"))
    archivos = [f for f in archivos if f.is_file()]

    _seccion(pdf, f"Archivos en output/ ({len(archivos)} archivos)")
    if not archivos:
        _parrafo(pdf, "output/ esta vacio — Domenech aun no ha generado nada.")
    else:
        for f in archivos[:30]:
            pdf.set_font("Helvetica", "B", 10)
            rel = str(f.relative_to(OUTPUT_DIR))
            pdf.cell(0, 6, rel, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if f.suffix in (".html", ".md", ".txt", ".js", ".css"):
                contenido = _leer_md(f, 1000)
                _parrafo(pdf, contenido, 8)
            pdf.ln(2)

    out = INFORME_DIR / "informe_domenech.pdf"
    pdf.output(str(out))
    print(f"[OK] {out.name}")


def pdf_durruti() -> None:
    pdf = _nuevo_pdf("Durruti - CEO Operativo")

    tareas = sorted(TASKS_DIR.glob("*.md"))
    informes = list(MEMORY_DIR.glob("*.md"))
    archivos_output = [f for f in OUTPUT_DIR.rglob("*") if f.is_file()]

    _seccion(pdf, "Resumen de actividad del equipo")
    resumen = (
        f"Informes Scout generados:  {len(informes)}\n"
        f"Archivos Domenech en output/:  {len(archivos_output)}\n"
        f"Tareas pendientes:  {len(tareas)}\n"
        f"Ultima actualizacion: {TS}"
    )
    _parrafo(pdf, resumen)

    _seccion(pdf, f"Tareas pendientes ({len(tareas)})")
    if not tareas:
        _parrafo(pdf, "No hay tareas pendientes.")
    else:
        for t in tareas:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, t.name, ln=True)
            _parrafo(pdf, _leer_md(t, 600), 9)
            pdf.ln(2)

    _seccion(pdf, "Ultimos informes Scout")
    for p in _informes_recientes(3):
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, p.name, ln=True)
        pdf.set_font("Helvetica", "", 9)

    out = INFORME_DIR / "informe_durruti.pdf"
    pdf.output(str(out))
    print(f"[OK] {out.name}")


def pdf_general() -> None:
    pdf = _nuevo_pdf("Informe General - FORRARSE")

    informes = list(MEMORY_DIR.glob("*.md"))
    archivos_output = [f for f in OUTPUT_DIR.rglob("*") if f.is_file()]
    tareas = list(TASKS_DIR.glob("*.md"))

    _seccion(pdf, "Estado del sistema")
    estado = (
        f"Timestamp: {TS}\n"
        f"Informes Scout:      {len(informes)}\n"
        f"Archivos generados:  {len(archivos_output)}\n"
        f"Tareas pendientes:   {len(tareas)}\n"
        f"Modelos activos:     Scout (llama-3.1-8b), Domenech (llama-3.1-8b), "
        f"Durruti (llama-3.3-70b)"
    )
    _parrafo(pdf, estado)

    # Ultimo informe Scout completo
    recientes = _informes_recientes(1)
    if recientes:
        _seccion(pdf, "Ultimo informe Scout")
        _parrafo(pdf, _leer_md(recientes[0], 4000), 9)

    # Lista de archivos output
    if archivos_output:
        _seccion(pdf, "Archivos generados por Domenech")
        lista = "\n".join(str(f.relative_to(OUTPUT_DIR)) for f in archivos_output[:20])
        _parrafo(pdf, lista, 9)

    # Tareas
    if tareas:
        _seccion(pdf, "Tareas pendientes")
        _parrafo(pdf, "\n".join(t.name for t in tareas), 9)

    out = INFORME_DIR / "informe_general.pdf"
    pdf.output(str(out))
    print(f"[OK] {out.name}")


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\nGenerando informes PDF en {INFORME_DIR} ...")
    pdf_general()
    pdf_scout()
    pdf_domenech()
    pdf_durruti()
    print("\nListo. 4 PDFs generados.")

    # Panel de control HTML
    try:
        import importlib.util, sys as _sys
        spec = importlib.util.spec_from_file_location(
            "generar_panel",
            PROJECT_ROOT / "scripts" / "generar_panel.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.generar()
    except Exception as e:
        print(f"[panel] {e}")

    # Email resumen (solo si GMAIL_APP_PASSWORD está configurado)
    try:
        import os
        if os.getenv("GMAIL_APP_PASSWORD", "").strip():
            from shared.email_sender import enviar_resumen_equipo
            ok = enviar_resumen_equipo()
            print("[OK] Email enviado." if ok else "[!] Email: fallo al enviar.")
        else:
            print("[email] Sin configurar (añade GMAIL_APP_PASSWORD en .env)")
    except Exception as e:
        print(f"[email] {e}")


if __name__ == "__main__":
    main()

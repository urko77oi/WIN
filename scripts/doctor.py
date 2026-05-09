"""Autodiagnóstico del sistema Durruti.

Uso:
    uv run python scripts/doctor.py

Recorre el protocolo de DOCTOR.md y deja un reporte en logs/doctor-AAAA-MM-DD.md.
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv  # noqa: E402
from rich.console import Console  # noqa: E402

# Carga .env si existe para que las comprobaciones vean las variables.
load_dotenv(PROJECT_ROOT / ".env")

console = Console()


def _check(nombre: str, ok: bool, detalle: str = "") -> tuple[str, str]:
    icono = "[green]OK[/green]" if ok else "[red]FALLO[/red]"
    console.print(f"{icono}  {nombre}{(' — ' + detalle) if detalle else ''}")
    estado = "OK" if ok else "FALLO"
    return (estado, f"- **{nombre}**: {estado}{(' — ' + detalle) if detalle else ''}")


def main() -> int:
    console.rule("[bold]Doctor — Durruti[/bold]")
    lineas: list[str] = []

    # 1. .env presente
    env = PROJECT_ROOT / ".env"
    _, l = _check(".env presente", env.exists(), str(env) if env.exists() else "Falta. Copia .env.example -> .env")
    lineas.append(l)

    # 2. Variables clave
    llm_mode = os.environ.get("LLM_MODE")
    _, l = _check("LLM_MODE definida", llm_mode is not None, f"valor='{llm_mode}'")
    lineas.append(l)

    if llm_mode == "real":
        _, l = _check("ANTHROPIC_API_KEY presente", bool(os.environ.get("ANTHROPIC_API_KEY")))
        lineas.append(l)

    # 3. Configs presentes
    for nombre in ("config/settings.yaml", "config/budget.yaml", "config/models.yaml"):
        p = PROJECT_ROOT / nombre
        _, l = _check(f"Config {nombre}", p.exists())
        lineas.append(l)

    # 4. SQLite operativa
    db = PROJECT_ROOT / "memory" / "db.sqlite"
    try:
        db.parent.mkdir(parents=True, exist_ok=True)
        c = sqlite3.connect(db, timeout=2.0)
        c.execute("PRAGMA journal_mode=WAL;")
        c.close()
        _, l = _check("SQLite accesible", True, str(db))
    except Exception as e:
        _, l = _check("SQLite accesible", False, str(e))
    lineas.append(l)

    # 5. Espacio en disco
    try:
        total, usado, libre = shutil.disk_usage(str(PROJECT_ROOT))
        gb_libre = libre / (1024**3)
        _, l = _check("Espacio en disco", gb_libre > 1.0, f"{gb_libre:.1f} GB libres")
    except Exception as e:
        _, l = _check("Espacio en disco", False, str(e))
    lineas.append(l)

    # 6. Tareas colgadas en pending
    pending = list((PROJECT_ROOT / "tasks" / "pending").glob("*.json"))
    _, l = _check("Tareas pending", True, f"{len(pending)} archivos")
    lineas.append(l)

    # 7. Logs recientes
    logs_dir = PROJECT_ROOT / "logs"
    logs = sorted(logs_dir.glob("*.log")) if logs_dir.exists() else []
    _, l = _check("Logs disponibles", True, f"{len(logs)} archivos")
    lineas.append(l)

    # Reporte
    fecha = datetime.now().strftime("%Y-%m-%d")
    reporte = PROJECT_ROOT / "logs" / f"doctor-{fecha}.md"
    reporte.parent.mkdir(parents=True, exist_ok=True)
    reporte.write_text(
        f"# Doctor — {fecha}\n\n" + "\n".join(lineas) + "\n",
        encoding="utf-8",
    )
    console.print(f"\nReporte guardado en: [cyan]{reporte.relative_to(PROJECT_ROOT)}[/cyan]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

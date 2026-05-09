"""Muestra el estado actual del sistema.

Uso:
    uv run python scripts/status.py

Reporta: modo LLM, proyectos activos, costes acumulados, últimas decisiones.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from shared import cost_tracker, llm_client, memory  # noqa: E402

console = Console()


def main() -> int:
    console.rule("[bold]Durruti — Estado[/bold]")

    modo = llm_client.modo_actual()
    color = "yellow" if modo == "mock" else "green"
    console.print(f"Modo LLM: [{color}]{modo}[/{color}]\n")

    # Proyectos
    proyectos = memory.listar_proyectos()
    tbl = Table(title=f"Proyectos activos ({len(proyectos)})")
    tbl.add_column("Slug")
    tbl.add_column("Nombre")
    tbl.add_column("Actualizado")
    for p in proyectos[:20]:
        tbl.add_row(p.slug, p.nombre[:50], p.actualizado[:19])
    console.print(tbl)
    console.print()

    # Costes
    coste_dia = cost_tracker.coste_acumulado("dia")
    coste_sem = cost_tracker.coste_acumulado("semana")
    coste_mes = cost_tracker.coste_acumulado("mes")
    coste_total = cost_tracker.coste_acumulado("total")
    limite = cost_tracker.limite_diario_eur()

    tbl_c = Table(title="Costes (EUR)")
    tbl_c.add_column("Periodo")
    tbl_c.add_column("Coste", justify="right")
    tbl_c.add_row("Hoy", f"{coste_dia:.4f} / {limite:.2f}")
    tbl_c.add_row("Semana", f"{coste_sem:.4f}")
    tbl_c.add_row("Mes", f"{coste_mes:.4f}")
    tbl_c.add_row("Total", f"{coste_total:.4f}")
    console.print(tbl_c)

    if cost_tracker.excede_limite_diario():
        console.print("[bold red]⚠ Límite diario superado. Sistema pausaría llamadas reales.[/bold red]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

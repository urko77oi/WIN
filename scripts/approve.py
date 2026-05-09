"""CLI de aprobación de tareas pendientes (respaldo del canal humano).

Uso:
    uv run python scripts/approve.py

En Fase 0 sirve como demo del flujo de aprobación: lista las solicitudes
pendientes en `tasks/waiting_approval/` y permite aprobar/rechazar.
En Fase 1+ Telegram será el canal principal y este script el respaldo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console  # noqa: E402
from rich.prompt import Prompt  # noqa: E402

console = Console()
WAITING_DIR = PROJECT_ROOT / "tasks" / "waiting_approval"


def main() -> int:
    if not WAITING_DIR.exists() or not any(WAITING_DIR.iterdir()):
        console.print("[green]No hay aprobaciones pendientes.[/green]")
        return 0

    pendientes = sorted(WAITING_DIR.glob("*.json"))
    console.rule(f"[bold]{len(pendientes)} aprobaciones pendientes[/bold]")

    for archivo in pendientes:
        try:
            data = json.loads(archivo.read_text(encoding="utf-8"))
        except Exception as e:
            console.print(f"[red]No puedo leer {archivo.name}: {e}[/red]")
            continue

        console.print(f"\n[bold]{archivo.stem}[/bold]")
        console.print(f"  Acción: {data.get('accion', '?')}")
        console.print(f"  Motivos: {', '.join(data.get('motivos', []) or ['ninguno'])}")
        console.print(f"  Coste estimado: {data.get('coste_estimado_eur', 0):.4f} €")
        if data.get("contexto"):
            console.print(f"  Contexto: {data['contexto']}")

        respuesta = Prompt.ask("  ¿Apruebas?", choices=["si", "no", "saltar"], default="saltar")
        if respuesta == "saltar":
            continue
        data["aprobada"] = (respuesta == "si")
        # Movemos a completed/ con el resultado anotado
        destino = PROJECT_ROOT / "tasks" / "completed"
        destino.mkdir(parents=True, exist_ok=True)
        (destino / archivo.name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        archivo.unlink()
        console.print(f"  [dim]Resuelto: aprobada={data['aprobada']}[/dim]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

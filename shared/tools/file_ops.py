"""Operaciones de archivo seguras.

Toda escritura pasa por `guardrails.validar_ruta_escritura` para evitar que
el sistema toque rutas fuera del proyecto o directorios del SO.

Quien lo usa: Builder principalmente, para guardar entregables; Durruti
para anotar bitácora; otros agentes en Fase 1+.
"""
from __future__ import annotations

from pathlib import Path

from shared.guardrails import validar_ruta_escritura
from shared.logger import log_de

log = log_de("file_ops")


def escribir(ruta: str | Path, contenido: str, *, sobrescribir: bool = True) -> Path:
    """Escribe un archivo. Crea directorios padres si hace falta.

    Lanza `GuardrailViolation` si la ruta es inválida.
    Lanza `FileExistsError` si existe y `sobrescribir=False`.
    """
    p = validar_ruta_escritura(ruta)
    if p.exists() and not sobrescribir:
        raise FileExistsError(f"Archivo ya existe: {p}. Pasa sobrescribir=True para reemplazar.")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")
    log.info(f"Escrito {p} ({len(contenido)} chars)")
    return p


def leer(ruta: str | Path) -> str:
    """Lee un archivo de texto."""
    p = Path(ruta)
    if not p.exists():
        raise FileNotFoundError(f"Archivo no existe: {p}")
    return p.read_text(encoding="utf-8")


def listar(directorio: str | Path, patron: str = "*") -> list[Path]:
    """Lista archivos en un directorio que coincidan con un patrón."""
    d = Path(directorio)
    if not d.exists():
        return []
    return sorted(d.glob(patron))

"""Memoria persistente del sistema.

Tres capas:
  - Corta: contexto en RAM del proceso (no aquí).
  - Media: archivos `.md` por proyecto/learning/playbook.
  - Larga: SQLite (`memory/db.sqlite`) con tablas estructuradas.

Quien lo usa: Durruti para gestionar proyectos; agentes para registrar
aprendizajes; scripts para reportar estado.
"""
from __future__ import annotations

import re
import sqlite3
import unicodedata
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from shared.logger import PROJECT_ROOT, log_de

log = log_de("memory")

DB_PATH: Path = PROJECT_ROOT / "memory" / "db.sqlite"
PROJECTS_DIR: Path = PROJECT_ROOT / "memory" / "projects"
LEARNINGS_DIR: Path = PROJECT_ROOT / "memory" / "learnings"
PLAYBOOKS_DIR: Path = PROJECT_ROOT / "memory" / "playbooks"


# ─────────────────────────────────────────────────────────────────────
# Esquema SQLite
# ─────────────────────────────────────────────────────────────────────

_SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    creado TEXT NOT NULL,
    actualizado TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_projects_estado ON projects(estado);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    agente TEXT NOT NULL,
    contexto TEXT NOT NULL,
    decision TEXT NOT NULL,
    razon TEXT
);
"""


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        c.execute("PRAGMA journal_mode=WAL;")
        c.execute("PRAGMA foreign_keys=ON;")
        c.executescript(_SCHEMA)
        yield c
        c.commit()
    finally:
        c.close()


# ─────────────────────────────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────────────────────────────

def slugify(texto: str) -> str:
    """Convierte un texto libre en un slug seguro para nombre de archivo."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "sin-nombre"


# ─────────────────────────────────────────────────────────────────────
# Proyectos
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Project:
    slug: str
    nombre: str
    descripcion: str
    estado: str
    creado: str
    actualizado: str
    archivo_md: Path


def crear_proyecto(nombre: str, descripcion: str = "") -> Project:
    """Crea un proyecto: fila en SQLite + archivo .md en memory/projects/."""
    slug = slugify(nombre)
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archivo = PROJECTS_DIR / f"{slug}.md"

    with _conn() as c:
        c.execute(
            "INSERT OR IGNORE INTO projects(slug, nombre, descripcion, estado, "
            "creado, actualizado) VALUES(?,?,?,?,?,?)",
            (slug, nombre, descripcion, "activo", ahora, ahora),
        )

    if not archivo.exists():
        PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        archivo.write_text(
            f"# Proyecto: {nombre}\n\n"
            f"- **Slug**: `{slug}`\n"
            f"- **Estado**: activo\n"
            f"- **Creado**: {ahora}\n\n"
            f"## Descripción\n\n{descripcion or '_pendiente_'}\n\n"
            f"## Bitácora\n\n_(Durruti irá anotando aquí los hitos.)_\n",
            encoding="utf-8",
        )
        log.info(f"Proyecto creado: {slug} ({archivo})")

    return Project(
        slug=slug,
        nombre=nombre,
        descripcion=descripcion,
        estado="activo",
        creado=ahora,
        actualizado=ahora,
        archivo_md=archivo,
    )


def listar_proyectos(solo_activos: bool = True) -> list[Project]:
    """Lista los proyectos registrados."""
    with _conn() as c:
        sql = "SELECT slug, nombre, descripcion, estado, creado, actualizado FROM projects"
        if solo_activos:
            sql += " WHERE estado = 'activo'"
        sql += " ORDER BY actualizado DESC"
        rows = c.execute(sql).fetchall()
    return [
        Project(
            slug=r[0],
            nombre=r[1],
            descripcion=r[2] or "",
            estado=r[3],
            creado=r[4],
            actualizado=r[5],
            archivo_md=PROJECTS_DIR / f"{r[0]}.md",
        )
        for r in rows
    ]


def anotar_en_bitacora(slug: str, entrada: str) -> None:
    """Añade una línea con timestamp a la bitácora del proyecto."""
    archivo = PROJECTS_DIR / f"{slug}.md"
    if not archivo.exists():
        log.warning(f"Proyecto {slug!r} no existe; no puedo anotar.")
        return
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with archivo.open("a", encoding="utf-8") as f:
        f.write(f"- `{ts}` — {entrada}\n")
    with _conn() as c:
        c.execute("UPDATE projects SET actualizado = ? WHERE slug = ?", (ts, slug))


# ─────────────────────────────────────────────────────────────────────
# Decisiones
# ─────────────────────────────────────────────────────────────────────

def registrar_decision(*, agente: str, contexto: str, decision: str, razon: str = "") -> None:
    """Guarda una decisión importante (para auditoría futura)."""
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _conn() as c:
        c.execute(
            "INSERT INTO decisions(timestamp, agente, contexto, decision, razon) "
            "VALUES(?,?,?,?,?)",
            (ts, agente, contexto, decision, razon),
        )

"""Tracking de costes de cada llamada al LLM.

Persiste en SQLite (`memory/db.sqlite`, tabla `costs`).
Calcula coste estimado en EUR a partir de `config/budget.yaml`.

Quien lo usa: `shared/llm_client.py` después de cada llamada.
Lectura: `scripts/status.py` para mostrar el día / semana / mes.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator

import yaml

from shared.logger import PROJECT_ROOT, log_de

log = log_de("cost")

DB_PATH: Path = PROJECT_ROOT / "memory" / "db.sqlite"
BUDGET_PATH: Path = PROJECT_ROOT / "config" / "budget.yaml"


# ─────────────────────────────────────────────────────────────────────
# Esquema
# ─────────────────────────────────────────────────────────────────────

_SCHEMA = """
CREATE TABLE IF NOT EXISTS costs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    agente TEXT NOT NULL,
    modelo TEXT NOT NULL,
    tokens_input INTEGER NOT NULL DEFAULT 0,
    tokens_output INTEGER NOT NULL DEFAULT 0,
    coste_eur REAL NOT NULL DEFAULT 0.0,
    orden TEXT,
    nota TEXT
);
CREATE INDEX IF NOT EXISTS idx_costs_timestamp ON costs(timestamp);
CREATE INDEX IF NOT EXISTS idx_costs_agente ON costs(agente);
"""


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    """Abre conexión SQLite con WAL para evitar `database is locked`."""
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
# Precios
# ─────────────────────────────────────────────────────────────────────

def _cargar_precios() -> dict:
    """Devuelve el diccionario `modelo -> {input, output}` (EUR/M tokens)."""
    if not BUDGET_PATH.exists():
        return {}
    with BUDGET_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("modelos_precios_eur_por_millon_tokens", {})


def estimar_coste_eur(modelo: str, tokens_input: int, tokens_output: int) -> float:
    """Estima el coste en euros de una llamada.

    Si el modelo no está en la tabla de precios, devuelve 0 y avisa.
    """
    precios = _cargar_precios()
    p = precios.get(modelo)
    if not p:
        log.warning(f"Modelo {modelo!r} sin precio en budget.yaml; coste 0")
        return 0.0
    coste = (tokens_input / 1_000_000) * p["input"] + (tokens_output / 1_000_000) * p["output"]
    return round(coste, 6)


# ─────────────────────────────────────────────────────────────────────
# Registro y lectura
# ─────────────────────────────────────────────────────────────────────

def registrar(
    *,
    agente: str,
    modelo: str,
    tokens_input: int,
    tokens_output: int,
    orden: str | None = None,
    nota: str | None = None,
) -> float:
    """Registra una llamada al LLM. Devuelve el coste estimado en EUR."""
    coste = estimar_coste_eur(modelo, tokens_input, tokens_output)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _conn() as c:
        c.execute(
            "INSERT INTO costs(timestamp, agente, modelo, tokens_input, tokens_output, "
            "coste_eur, orden, nota) VALUES(?,?,?,?,?,?,?,?)",
            (ts, agente, modelo, tokens_input, tokens_output, coste, orden, nota),
        )
    return coste


def coste_acumulado(periodo: str = "dia") -> float:
    """Devuelve el coste acumulado en el periodo indicado.

    `periodo`: 'dia' | 'semana' | 'mes' | 'total'.
    """
    ahora = datetime.now(timezone.utc)
    rangos = {
        "dia": ahora - timedelta(days=1),
        "semana": ahora - timedelta(days=7),
        "mes": ahora - timedelta(days=30),
        "total": None,
    }
    desde = rangos.get(periodo, rangos["dia"])

    with _conn() as c:
        if desde is None:
            r = c.execute("SELECT COALESCE(SUM(coste_eur), 0) FROM costs").fetchone()
        else:
            r = c.execute(
                "SELECT COALESCE(SUM(coste_eur), 0) FROM costs WHERE timestamp >= ?",
                (desde.isoformat(timespec="seconds"),),
            ).fetchone()
    return float(r[0])


def limite_diario_eur() -> float:
    """Lee el límite diario configurado en budget.yaml."""
    if not BUDGET_PATH.exists():
        return 5.0
    with BUDGET_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return float((data.get("limites") or {}).get("diario_eur", 5.0))


def excede_limite_diario() -> bool:
    """True si el coste del día ya supera el límite duro."""
    return coste_acumulado("dia") >= limite_diario_eur()

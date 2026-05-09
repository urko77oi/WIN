"""Configuración del logger global del sistema.

Usa `loguru` con dos sumideros:
  - consola (rich, legible para el usuario)
  - archivo `logs/AAAA-MM-DD.log` (rotación diaria, retención 30 días)

Quien lo usa: cualquier módulo que importe `from shared.logger import log`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml
from loguru import logger as _logger

# Carpeta raíz del proyecto (dos niveles arriba de este archivo: shared/logger.py).
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def _cargar_config_logging() -> dict:
    """Lee config/settings.yaml y devuelve el bloque `logging`.

    Si el archivo no existe (caso raro: usuario lo borró), devuelve defaults
    seguros para que el logger nunca falle al arrancar.
    """
    cfg_path = PROJECT_ROOT / "config" / "settings.yaml"
    defaults = {
        "dir": "logs",
        "retention_days": 30,
        "level_default": "INFO",
        "rotation": "1 day",
    }
    if not cfg_path.exists():
        return defaults
    try:
        with cfg_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return {**defaults, **(data.get("logging") or {})}
    except Exception:
        return defaults


def _configurar_logger() -> None:
    """Reconfigura loguru desde cero (idempotente).

    Llamado una sola vez al importar este módulo.
    """
    cfg = _cargar_config_logging()
    nivel = os.environ.get("LOG_LEVEL", cfg["level_default"]).upper()

    logs_dir = PROJECT_ROOT / cfg["dir"]
    logs_dir.mkdir(parents=True, exist_ok=True)

    _logger.remove()  # quitamos el handler por defecto

    # Sumidero consola: formato legible.
    _logger.add(
        sys.stderr,
        level=nivel,
        format=(
            "<green>{time:HH:mm:ss}</green> "
            "<level>{level: <8}</level> "
            "<cyan>{extra[agente]: <12}</cyan> "
            "{message}"
        ),
        colorize=True,
    )

    # Sumidero archivo: rota cada día, retiene N días, comprime al rotar.
    _logger.add(
        logs_dir / "{time:YYYY-MM-DD}.log",
        level=nivel,
        rotation=cfg["rotation"],
        retention=f"{cfg['retention_days']} days",
        compression="zip",
        encoding="utf-8",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{extra[agente]: <12} | {name}:{function}:{line} | {message}"
        ),
    )

    # `agente` es un campo extra que cada agente puede sobreescribir con
    # `log.bind(agente="durruti").info(...)`. Si no lo hace, sale "system".
    _logger.configure(extra={"agente": "system"})


_configurar_logger()

# Export público.
log = _logger


def log_de(agente: str):
    """Devuelve un logger con el campo `agente` ya rellenado.

    Uso:
        from shared.logger import log_de
        log = log_de("durruti")
        log.info("hola")
    """
    return _logger.bind(agente=agente)

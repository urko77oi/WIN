"""Guardrails: reglas inviolables aplicadas como código.

Filosofía: las reglas en el system prompt se pueden saltar; las del wrapper
de Python no. Cada herramienta o acción del sistema debe pasar primero por
aquí. Si la validación falla, lanza `GuardrailViolation` y el agente
debe reportarlo al humano.

Quien lo usa: `shared/tools/*`, `agents/*` antes de cualquier acción que
toque el mundo (escribir archivos, ejecutar comandos, llamar APIs externas).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from shared.logger import PROJECT_ROOT, log_de

log = log_de("guardrail")

BUDGET_PATH: Path = PROJECT_ROOT / "config" / "budget.yaml"


class GuardrailViolation(Exception):
    """Se lanza cuando una acción viola un guardrail.

    El mensaje DEBE ser entendible por un no-programador, en español.
    """


@dataclass(frozen=True)
class Accion:
    """Descripción de una acción que se va a ejecutar.

    Campos:
        tipo: identificador corto (p.ej. "escribir_archivo", "ejecutar_shell").
        objetivo: ruta, URL o destino concreto.
        agente: quién quiere ejecutarla.
        implica_pago: bool
        es_irreversible: bool
        es_publicacion_publica: bool
        envia_email_masivo: bool
        modifica_produccion: bool
        elimina_archivos: bool
        ejecuta_comando_shell: bool
    """
    tipo: str
    objetivo: str
    agente: str
    implica_pago: bool = False
    es_irreversible: bool = False
    es_publicacion_publica: bool = False
    envia_email_masivo: bool = False
    modifica_produccion: bool = False
    elimina_archivos: bool = False
    ejecuta_comando_shell: bool = False


# ─────────────────────────────────────────────────────────────────────
# Listas negras
# ─────────────────────────────────────────────────────────────────────

# Patrones de comandos shell que están prohibidos siempre.
_SHELL_BLACKLIST: tuple[re.Pattern[str], ...] = (
    re.compile(r"\brm\s+-rf?\b", re.IGNORECASE),
    re.compile(r"\bdel\s+/[sf]\b", re.IGNORECASE),
    re.compile(r"\bformat\b", re.IGNORECASE),
    re.compile(r"\bmkfs\b", re.IGNORECASE),
    re.compile(r"\bdd\s+if=", re.IGNORECASE),
    re.compile(r":\(\)\s*\{\s*:\|", re.IGNORECASE),  # fork bomb
    re.compile(r"\bshutdown\b", re.IGNORECASE),
    re.compile(r"\breboot\b", re.IGNORECASE),
)

# Rutas que el sistema nunca debe modificar fuera del proyecto.
_RUTAS_PROHIBIDAS: tuple[str, ...] = (
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "/etc",
    "/usr",
    "/bin",
    "/sbin",
    "/System",
)


# ─────────────────────────────────────────────────────────────────────
# Categorías que requieren aprobación humana
# ─────────────────────────────────────────────────────────────────────

def _categorias_que_requieren_aprobacion() -> set[str]:
    """Lee del budget.yaml las categorías que requieren OK humano."""
    if not BUDGET_PATH.exists():
        return {
            "implica_pago",
            "es_irreversible",
            "es_publicacion_publica",
            "envia_email_masivo",
            "modifica_produccion",
            "elimina_archivos",
            "ejecuta_comando_shell",
        }
    with BUDGET_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return set(data.get("aprobacion_humana_obligatoria_si") or [])


def requiere_aprobacion_humana(accion: Accion) -> tuple[bool, list[str]]:
    """Devuelve (necesita_ok, motivos)."""
    categorias = _categorias_que_requieren_aprobacion()
    motivos = [c for c in categorias if getattr(accion, c, False)]
    return (len(motivos) > 0, motivos)


# ─────────────────────────────────────────────────────────────────────
# Validaciones
# ─────────────────────────────────────────────────────────────────────

def validar_ruta_escritura(ruta: str | Path) -> Path:
    """Valida que una ruta esté dentro del proyecto y no en directorio prohibido.

    Devuelve el `Path` resuelto si OK. Lanza `GuardrailViolation` si no.
    """
    p = Path(ruta).resolve()
    s = str(p)
    for prohibida in _RUTAS_PROHIBIDAS:
        if s.lower().startswith(prohibida.lower()):
            raise GuardrailViolation(
                f"Ruta prohibida: {p}. No puedo escribir en directorios del sistema."
            )
    # Debe estar dentro del proyecto.
    try:
        p.relative_to(PROJECT_ROOT)
    except ValueError:
        raise GuardrailViolation(
            f"Ruta fuera del proyecto: {p}. Solo puedo escribir dentro de {PROJECT_ROOT}."
        )
    return p


def validar_comando_shell(comando: str) -> None:
    """Lanza `GuardrailViolation` si el comando hace match con la lista negra."""
    for patron in _SHELL_BLACKLIST:
        if patron.search(comando):
            raise GuardrailViolation(
                f"Comando bloqueado por lista negra: {comando!r}. "
                f"Si crees que es un falso positivo, avisa al humano."
            )


def validar_accion(accion: Accion) -> tuple[bool, list[str]]:
    """Validación genérica antes de ejecutar.

    Devuelve (necesita_ok_humano, motivos). Lanza GuardrailViolation si la
    acción está prohibida directamente.

    No comprueba aprobación previa: eso lo hace el llamador (Durruti) usando
    `human_channel.solicitar_aprobacion(...)`.
    """
    if accion.ejecuta_comando_shell:
        # Si la acción declara shell, esperamos que `objetivo` sea el comando.
        validar_comando_shell(accion.objetivo)

    if accion.tipo == "escribir_archivo":
        validar_ruta_escritura(accion.objetivo)

    necesita_ok, motivos = requiere_aprobacion_humana(accion)
    if necesita_ok:
        log.info(f"Acción {accion.tipo!r} sobre {accion.objetivo!r} requiere OK humano: {motivos}")
    return (necesita_ok, motivos)

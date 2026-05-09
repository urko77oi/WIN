"""Compositor del prompt completo de un agente.

Problema que resuelve: la versión inicial de Fase 0 inyectaba al modelo
únicamente el archivo `system_prompt.md` de cada agente. Pero los agentes
(diseñados por el founder) tienen 9-10 archivos `.md` que definen su
identidad, misión, skills, playbook, scoring, guardrails, etc. Sin
componer el contexto completo, el modelo solo veía un trozo y se quedaba
sin la mayor parte de su diseño.

Este loader:
  1. Antepone un bloque común (`CONTEXTO_FORRARSE`) con el organigrama
     del proyecto y las reglas inviolables. Todos los agentes lo reciben.
  2. Concatena los `.md` que pidas, en el orden que pidas, separados por
     cabeceras claras para que el modelo navegue.

Quien lo usa: cada clase de agente en su `__init__`.
"""
from __future__ import annotations

from pathlib import Path

from shared.logger import PROJECT_ROOT, log_de

log = log_de("loader")


# ─────────────────────────────────────────────────────────────────────
# Contexto común a todos los agentes — el organigrama de FORRARSE.
# Se inyecta como cabecera del prompt de Durruti, Scout y Domenech.
# ─────────────────────────────────────────────────────────────────────

CONTEXTO_FORRARSE: str = """\
# Contexto: Proyecto FORRARSE

Trabajas dentro del proyecto **FORRARSE**, un sistema multi-agente para
construir y operar negocios online.

## Organigrama (jerarquía estricta)

- **Founder** — el humano que paga y decide. Único que da órdenes finales
  y aprueba acciones con impacto real (pagos, publicaciones, irreversibles).
- **CEO Operativo: Durruti** — único interlocutor con el Founder. Recibe
  órdenes, descompone, delega, supervisa, pide aprobaciones, reporta.
- **Equipo (reporta a Durruti)**:
  - **Scout** — Analista de Oportunidades. Investiga nichos, valida
    mercados, scorea oportunidades (triple lectura: Conservador / Equilibrado
    / Agresivo). No actúa: solo reporta.
  - **Domenech** — Builder. Constructor de activos digitales (landings,
    blogs, SaaS, automatizaciones). Toma oportunidades validadas y las
    convierte en algo funcional, publicado, con calidad de día 1.

## Flujo de información

```
Founder → Durruti → Scout / Domenech (briefing)
                  ↘
Scout / Domenech → Durruti (entrega)
                  ↘
                   Durruti → Founder (consolidación + aprobación si toca)
```

Scout y Domenech **nunca hablan al Founder directamente**. Si necesitan
algo del Founder, lo piden a Durruti y Durruti decide cómo plantearlo.

## Reglas inviolables del proyecto

1. Solo Durruti habla con el Founder.
2. Ningún pago, publicación pública, envío masivo o acción irreversible
   se ejecuta sin aprobación explícita del Founder.
3. Ningún agente modifica su propio prompt o identidad sin pasar por
   `proposals/` y aprobación.
4. Honestidad operativa por encima de marketing: si algo no funciona o
   no es viable, se dice. No se simula éxito.
5. Idioma operativo: **español** en todo (logs, reportes, prompts).
   Excepción: nombres de variables/funciones/librerías en código → inglés.
"""


# ─────────────────────────────────────────────────────────────────────
# Loader
# ─────────────────────────────────────────────────────────────────────

def cargar_prompt_de(agente: str, archivos: list[str]) -> str:
    """Compone el prompt completo de un agente.

    Args:
        agente: nombre del agente, debe coincidir con la subcarpeta de
            `agents/` (ej. ``"durruti"``, ``"scout"``, ``"domenech"``).
        archivos: lista de nombres de `.md` a concatenar, en el orden
            que se quiere que aparezcan en el prompt. Ejemplo:
            ``["identity.md", "system_prompt.md", "playbook.md"]``.

    Returns:
        El prompt completo como string, listo para pasarse como `system`
        al modelo.

    Si un archivo no existe, se omite con un warning en el log (en vez
    de fallar) para que el sistema sea robusto a renombrados.
    """
    base = PROJECT_ROOT / "agents" / agente
    partes: list[str] = [CONTEXTO_FORRARSE]

    for nombre in archivos:
        ruta = base / nombre
        if not ruta.exists():
            log.warning(f"{ruta} no existe; lo omito del prompt de {agente!r}")
            continue
        contenido = ruta.read_text(encoding="utf-8")
        partes.append(
            f"\n---\n\n# === {agente}/{nombre} ===\n\n{contenido}"
        )

    return "\n".join(partes)

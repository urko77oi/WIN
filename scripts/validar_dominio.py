"""Validador de ideas de negocio: dominio disponible + nivel de competencia.

Uso:
    uv run python scripts/validar_dominio.py autonomotools
    uv run python scripts/validar_dominio.py "marketing seniors"

Para cada nombre comprueba:
  - Disponibilidad .com y .es (WHOIS)
  - Nivel de competencia estimado (DuckDuckGo)
  - Webs directamente competidoras
  - Puntuación de viabilidad
"""
from __future__ import annotations

import re
import sys
import socket
import time
from pathlib import Path

# Fuerza UTF-8 en la consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def _slug(nombre: str) -> str:
    s = nombre.lower().strip()
    s = re.sub(r"[áàä]", "a", s)
    s = re.sub(r"[éèë]", "e", s)
    s = re.sub(r"[íìï]", "i", s)
    s = re.sub(r"[óòö]", "o", s)
    s = re.sub(r"[úùü]", "u", s)
    s = re.sub(r"ñ", "n", s)
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


def _dominio_resuelve(dominio: str) -> bool:
    """Comprueba si el dominio tiene registros DNS (= está registrado)."""
    try:
        socket.getaddrinfo(dominio, None)
        return True
    except socket.gaierror:
        return False


def _competencia_ddg(nombre: str) -> dict:
    """Estima competencia con 3 búsquedas ponderadas."""
    try:
        from duckduckgo_search import DDGS

        queries = [
            (f'"{nombre}" site:es',               3),   # marca exacta en .es
            (f"{nombre} herramienta servicio web", 2),   # competidores directos
            (f"{nombre} alternativa comparativa",  1),   # reviews y comparativas
        ]

        puntos_comp = 0
        todos_urls: list[str] = []

        for q, peso in queries:
            try:
                ddgs = DDGS(timeout=12)
                res = list(ddgs.text(q, max_results=5, region="es-es"))
                puntos_comp += len(res) * peso
                todos_urls += [r.get("href", "") for r in res[:3]]
                time.sleep(0.4)
            except Exception:
                pass

        # puntos_comp max teórico: 5*3 + 5*2 + 5*1 = 30
        pct = puntos_comp / 30
        if pct < 0.25:
            nivel = "BAJO"
        elif pct < 0.6:
            nivel = "MEDIO"
        else:
            nivel = "ALTO"

        urls_unicas = list(dict.fromkeys(u for u in todos_urls if u))[:5]
        return {"nivel": nivel, "puntos": puntos_comp, "urls": urls_unicas}
    except Exception as e:
        return {"nivel": "?", "puntos": 0, "urls": [], "error": str(e)}


def validar(nombre: str) -> dict:
    slug = _slug(nombre)
    print(f"\n{'='*55}")
    print(f"  Validando: {nombre!r}  (slug: {slug})")
    print(f"{'='*55}")

    # Dominios
    dominios = {}
    for tld in (".com", ".es", ".io"):
        dominio = f"{slug}{tld}"
        registrado = _dominio_resuelve(dominio)
        estado = "[OCUPADO]" if registrado else "[LIBRE]  "
        dominios[dominio] = {"libre": not registrado, "estado": estado}
        print(f"  {dominio:<30} {estado}")
        time.sleep(0.3)

    # Competencia
    print(f"\n  Buscando competencia...")
    comp = _competencia_ddg(nombre)
    print(f"  Competencia: {comp['nivel']} (score {comp.get('puntos',0)}/30)")
    if comp["urls"]:
        print("  Competidores encontrados:")
        for url in comp["urls"][:3]:
            print(f"    > {url}")

    # Puntuación
    libres = sum(1 for d in dominios.values() if d["libre"])
    puntos = 0
    puntos += libres * 20          # hasta 60 pts por dominios libres
    if comp["nivel"] == "BAJO":    puntos += 40
    elif comp["nivel"] == "MEDIO": puntos += 20
    else:                          puntos += 0

    if puntos >= 70:
        veredicto = "++ MUY VIABLE"
    elif puntos >= 40:
        veredicto = "+  VIABLE"
    else:
        veredicto = "-- DIFICIL"

    print(f"\n  Puntuación: {puntos}/100  →  {veredicto}")

    return {
        "nombre": nombre,
        "slug": slug,
        "dominios": dominios,
        "competencia": comp,
        "puntuacion": puntos,
        "veredicto": veredicto,
    }


def validar_lista(nombres: list[str]) -> list[dict]:
    resultados = []
    for n in nombres:
        r = validar(n)
        resultados.append(r)
        time.sleep(1)

    print(f"\n\n{'='*55}")
    print("  RANKING FINAL")
    print(f"{'='*55}")
    ranking = sorted(resultados, key=lambda x: x["puntuacion"], reverse=True)
    for i, r in enumerate(ranking, 1):
        print(f"  {i}. {r['nombre']:<30} {r['puntuacion']}/100  {r['veredicto']}")

    return ranking


if __name__ == "__main__":
    if len(sys.argv) > 1:
        nombres = sys.argv[1:]
    else:
        # Valida las 10 propuestas del informe de Scout
        nombres = [
            "autonomotools",
            "marketingparaseniors",
            "suscripcioncontent",
            "traduccionnegocios",
            "procolabora",
            "techaemprendedores",
        ]

    validar_lista(nombres)

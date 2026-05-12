"""Relanza Domenech para construir la landing de AutonomoTools."""
from __future__ import annotations
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import shutil
from agents.domenech.domenech import Domenech

# Limpia el intento anterior
prev = PROJECT_ROOT / "output" / "autonomotools"
if prev.exists():
    shutil.rmtree(prev)
    print("Limpiado output/autonomotools anterior")

domenech = Domenech()

brief = """
Crea una landing page profesional y completa para:

NOMBRE: AutonomoTools
TAGLINE: "Las mejores herramientas digitales para autonomos espanoles, curadas y comparadas"
PROPUESTA: Directorio curado de herramientas (gratuitas y de pago) para autonomos espanoles,
con comparativas reales, tutoriales practicos y guias paso a paso.
MONETIZACION: afiliados (comision cuando alguien contrata una herramienta) + newsletter premium 5 euros/mes
AUDIENCIA: autonomos espanoles 30-55 anos, poco tiempo, buscan soluciones practicas sin complicaciones

ESTRUCTURA DE LA LANDING:
1. HEADER: logo texto + nav minimalista
2. HERO: titular potente, subtitulo, CTA principal ("Ver herramientas gratis")
3. PROBLEMA: 3 frustraciones tipicas del autonomo (con emojis, texto directo)
4. SOLUCION: como AutonomoTools lo resuelve
5. CATEGORIAS: 3 tarjetas (Facturacion, Productividad, Conseguir Clientes) con 2-3 ejemplos cada una
6. TESTIMONIOS: 3 testimonios ficticios pero realistas de autonomos espanoles
7. NEWSLETTER: formulario captura email con propuesta de valor clara
8. FOOTER: links legales

DISENO:
- Colores: azul marino (#1a3a5c) + naranja (#f4821f) + blanco
- Tipografia: sistema fonts (no Google Fonts, sin dependencias externas)
- Mobile-first, responsive
- CSS inline en el mismo HTML (un solo archivo, sin dependencias)
- Copy en castellano, tono directo y practico, nada corporativo

Guarda el resultado como output/autonomotools/index.html (todo en un solo archivo HTML completo).
"""

print("Domenech construyendo landing (70B model, puede tardar 1-2 min)...")
resultado = domenech.proponer_landing(brief)
print("\n[Domenech] Resultado:", resultado[:200])

# Verifica archivos generados
output = PROJECT_ROOT / "output" / "autonomotools"
if output.exists():
    archivos = list(output.rglob("*"))
    archivos = [f for f in archivos if f.is_file()]
    print(f"\nArchivos generados ({len(archivos)}):")
    for f in archivos:
        print(f"  {f.relative_to(output.parent.parent)} ({f.stat().st_size} bytes)")

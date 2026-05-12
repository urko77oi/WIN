"""Sesion de trabajo autonoma: Scout profundiza + Domenech construye."""
from __future__ import annotations
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from agents.scout.scout import Scout
from agents.domenech.domenech import Domenech

scout    = Scout()
domenech = Domenech()

# ── RONDA 1: Scout audita los 3 nichos con menor competencia ──────────
nichos = [
    "tutoriales tecnologia marketing para seniors espana mercado digital",
    "modelos suscripcion contenido educativo espanol ticket bajo recurrente",
    "servicios digitales autonomos freelancers espana herramientas carencias",
]

print("\n=== SCOUT: auditando nichos de baja competencia ===")
for nicho in nichos:
    print(f"\n[Scout] Auditando: {nicho[:60]}")
    resultado = scout.auditar_competidor(nicho)
    print(resultado[:300])

# ── RONDA 2: Scout investiga la oportunidad mas especifica ────────────
print("\n=== SCOUT: investigacion profunda oportunidad principal ===")
brief_profundo = """
Investiga en profundidad este nicho especifico:
NICHO: Herramientas y recursos digitales para autonomos espanoles

Busca:
1. Cuantos autonomos hay en Espana y que problemas digitales tienen
2. Que herramientas usan actualmente y que les falta
3. Cuanto pagan por software/servicios (precio medio mensual)
4. Plataformas existentes y sus puntos debiles
5. Como monetizar un servicio dirigido a ellos con inversion cero

Objetivo: determinar si es viable lanzar un servicio de nicho en 30 dias.
Guarda el informe completo.
"""
informe = scout.investigar(brief_profundo)
print("\n[Scout] Informe completo guardado.")
print(informe[:400])

# ── RONDA 3: Domenech construye landing ──────────────────────────────
print("\n=== DOMENECH: construyendo landing page ===")
brief_landing = """
Crea una landing page profesional para este servicio:

NOMBRE: AutonomoTools
PROPUESTA: Directorio curado de herramientas digitales gratuitas y de pago
para autonomos espanoles, con comparativas, tutoriales y guias practicas.
MONETIZACION: afiliados + newsletter de pago (5 euros/mes)
AUDIENCIA: autonomos espanoles 30-55 anos, poco tiempo, buscan soluciones practicas

La landing debe tener:
- Hero con propuesta de valor clara
- Seccion de problemas que resuelve
- 3 categorias de herramientas (facturacion, productividad, clientes)
- CTA para newsletter gratuita como primer paso
- Diseno limpio, colores profesionales (azul/blanco), mobile-friendly

Guarda todos los archivos en output/autonomotools/.
"""
resultado_landing = domenech.proponer_landing(brief_landing)
print("\n[Domenech] Landing generada.")
print(resultado_landing[:300])

# ── Regenera PDFs ─────────────────────────────────────────────────────
print("\n=== Regenerando informes PDF ===")
import subprocess
subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "generar_informe.py")],
               cwd=str(PROJECT_ROOT))

print("\n=== Sesion completada ===")

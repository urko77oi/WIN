"""Genera el contenido COMPLETO de la semana 1 de la comunidad Skool.

Entrega por dia:
  Lunes    — Video bienvenida: script + SRT + thumbnail + descripcion YouTube
             Post Skool dia 1 + imagen Instagram
  Martes   — Tutorial: "5 herramientas gratis" script Reel + post Skool + imagen
  Miercoles — Debate: "Cuanto cobras" post Skool + carousel Instagram + LinkedIn
  Jueves   — Video tutorial: "Como facturar en 2026" script + SRT + thumbnail
             Post Skool + email newsletter
  Viernes  — Resumen semana + teaser semana 2 + calendario CSV para programar

Total: ~20 archivos listos para publicar.
"""
from __future__ import annotations
import sys, csv, io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from shared.herramientas import (
    crear_archivo, generar_srt, generar_descripcion_youtube,
    crear_thumbnail_html, crear_post_imagen_html, exportar_csv,
)

OUT = PROJECT_ROOT / "output" / "skool"

def sep(d): print(f"\n{'='*55}\n  {d}\n{'='*55}")
def ok(f):  print(f"  [OK] {f}")


# ══════════════════════════════════════════════════════════════
#  LUNES — Bienvenida + Presentación
# ══════════════════════════════════════════════════════════════
sep("LUNES — Bienvenida y presentacion")

SCRIPT_LUNES = """
Llevas tiempo buscando una comunidad de autonomos espanoles de verdad.
No un grupo de WhatsApp donde solo se quejan. No un curso caro que no
aplica aqui. Una comunidad donde gente como tu comparte lo que funciona,
lo que falla, y te ayuda a crecer.

Eso es exactamente lo que hemos construido.

Me llamo [TU NOMBRE]. Llevo [X] anos como autonomo en Espana.
He cometido todos los errores posibles: cobrar demasiado barato,
no tener contrato, perder clientes por no hacer seguimiento,
pagar herramientas que no necesitaba.

Y he aprendido de todos ellos.

Esta comunidad existe para que tu no tengas que cometer esos mismos errores.
Para que tengas acceso a las herramientas correctas, a gente que ya ha
pasado por lo que estas pasando, y a recursos que funcionan en Espana,
no en Silicon Valley.

Somos [N] autonomos ya. De diseno, programacion, consultoria, marketing,
traduccion, fotografia, contabilidad. De Madrid, Barcelona, Valencia,
Sevilla, Bilbao y de todo el territorio nacional.

Y todos tenemos algo en comun: preferimos trabajar para nosotros mismos,
aunque a veces sea dificil, porque la libertad no tiene precio.

Hoy abrimos las puertas. La comunidad es gratuita. Siempre lo sera.
Y si quieres ir mas lejos, hay un nivel premium con cursos, mentoria
y herramientas exclusivas por diecinueve euros al mes.

El link para unirte esta en la descripcion. Tardas treinta segundos.
Y puede ser el mejor movimiento que hagas esta semana.

Bienvenido a Autonomos Espana. Te veo dentro.
"""

crear_archivo("skool/videos/lunes_script_bienvenida.md",
    f"# Script — Video Bienvenida\n**Formato:** YouTube (3-4 min) + corte Reel (60s)\n**Publicacion:** Lunes semana 1\n\n{SCRIPT_LUNES}")
ok("script bienvenida")

generar_srt(SCRIPT_LUNES, "lunes-bienvenida")
ok("SRT subtitulos bienvenida")

crear_thumbnail_html(
    titulo="Bienvenido a\nAutónomos España",
    subtitulo="La comunidad que llevabas tiempo buscando",
    nombre="lunes-thumbnail-bienvenida",
)
ok("thumbnail bienvenida HTML")

generar_descripcion_youtube(
    titulo="Bienvenido a Autónomos España — La comunidad para freelances y autónomos españoles",
    script=SCRIPT_LUNES,
    tags="autonomos, freelance, comunidad autonomos, trabajar por cuenta propia, skool, herramientas autonomos"
)
ok("descripcion YouTube")

# Post Skool lunes
POST_SKOOL_LUNES = """# POST SKOOL — Lunes semana 1
**Categoria:** Bienvenida
**Tipo:** Presentacion + CTA presentarse

---
## Hola, soy [TU NOMBRE] — y esto es lo que hemos construido para ti

Llevaba tiempo queriendo crear un espacio donde los autonomos espanoles
pudiéramos hablar de verdad.

Sin vendehúmos. Sin promesas de "gana 10.000€ al mes haciendo nada".
Sin contenido en ingles que no aplica aqui.

Solo autonomos reales compartiendo lo que funciona, lo que falla,
y ayudandose mutuamente.

**Hoy arrancamos.**

En esta comunidad encontraras:
→ Herramientas curadas para el mercado espanol
→ Debates sobre precios, clientes y facturacion
→ Retos semanales practicos
→ Gente que entiende tus problemas de verdad

**Tu primer paso:** Presentate abajo. Di quien eres, a que te dedicas
y una cosa que quieres mejorar este mes.

Yo empiezo: [PRESENTACION DEL ADMIN]

Bienvenido al equipo. 👋

---
**Hashtags:** #autonomosespana #bienvenida #comunidad #freelance
"""
crear_archivo("skool/posts/lunes_post_skool.md", POST_SKOOL_LUNES)
ok("post Skool lunes")

crear_post_imagen_html(
    titulo="Bienvenido a\nAutónomos España",
    cuerpo="""Herramientas curadas para el mercado español
Debates sobre precios y clientes
Retos semanales prácticos
Gente que entiende tus problemas
Comunidad 100% gratuita""",
    nombre="lunes-post-instagram",
    color1="#1a3a5c", color2="#f4821f",
)
ok("imagen Instagram lunes")

CAPTION_LUNES = """Por fin una comunidad de autónomos españoles de verdad. 🇪🇸

Sin vendehúmos. Sin promesas imposibles. Solo gente como tú compartiendo lo que funciona.

Ya somos [N] autónomos. Únete gratis (link en bio 👆)

¿A qué te dedicas como autónomo? Cuéntanos abajo 👇

#autonomosespana #autonomo #freelance #trabajarparatimismo #emprendimiento #negociodigital #herramientasdigitales #comunidadautonomos"""
crear_archivo("skool/redes/lunes_caption_instagram.txt", CAPTION_LUNES)
ok("caption Instagram lunes")


# ══════════════════════════════════════════════════════════════
#  MARTES — Tutorial: 5 herramientas gratis
# ══════════════════════════════════════════════════════════════
sep("MARTES — Tutorial 5 herramientas gratis")

SCRIPT_REEL_MARTES = """
Para. Antes de gastar un euro en software, escucha esto.

Estas cinco herramientas son completamente gratuitas, las uso cada dia,
y si eres autonomo en Espana no tienes excusa para no tenerlas.

Numero uno: Conta Simple. Facturas, gastos, calculo de IVA.
Todo lo que necesitas si tu gestor solo te pide los numeros. Gratis.

Numero dos: Toggl Track. Control del tiempo por proyecto y cliente.
Si cobras por horas, esto es obligatorio. Si cobras por proyecto,
te ayudara a saber si estas ganando o perdiendo dinero. Gratis.

Numero tres: Notion. Tu segundo cerebro. Clientes, proyectos,
notas, base de datos. Sustituye a cinco herramientas de pago. Gratis.

Numero cuatro: Calendly. Agendar reuniones sin el ida y vuelta
de correos. Mandas el link, el cliente elige. Acabas con el
"cuando te viene bien". Gratis en el plan basico.

Numero cinco: Apollo. Para encontrar clientes potenciales con
email verificado. Si prospecting es parte de tu trabajo,
esto te cambia la vida. Gratis hasta 50 contactos al mes.

Las cinco en el link de mi bio, con tutorial de como configurarlas.
Guardalo. Compartelo con otro autonomo. Se lo merece.
"""

crear_archivo("skool/videos/martes_script_reel_herramientas.md",
    f"# Script Reel — 5 Herramientas Gratis\n**Formato:** Reel/TikTok 60-90 segundos\n**Publicacion:** Martes semana 1\n\n{SCRIPT_REEL_MARTES}")
ok("script Reel martes")

generar_srt(SCRIPT_REEL_MARTES, "martes-reel-herramientas", segundos_por_linea=3.5)
ok("SRT subtitulos Reel")

crear_thumbnail_html(
    titulo="5 Herramientas Gratis\nque Todo Autónomo Necesita",
    subtitulo="Sin pagar un euro. Con tutorial de configuración.",
    nombre="martes-thumbnail-herramientas",
    color_fondo="#0f172a",
    color_acento="#10b981",
)
ok("thumbnail herramientas")

# Post Skool martes (educativo con tabla)
POST_SKOOL_MARTES = """# POST SKOOL — Martes semana 1
**Categoria:** Herramientas
**Tipo:** Educativo — recurso con tabla comparativa

---
## Las 5 herramientas gratis que uso cada dia como autonomo (y por que)

Llevo [X] años como autonomo. He probado decenas de herramientas.
Estas cinco son las que han sobrevivido porque de verdad funcionan.

| Herramienta | Para que | Precio |
|-------------|----------|--------|
| Conta Simple | Facturas + IVA | Gratis |
| Toggl Track | Control del tiempo | Gratis |
| Notion | Gestion y notas | Gratis |
| Calendly | Agendar reuniones | Gratis (basico) |
| Apollo.io | Encontrar clientes | Gratis (50/mes) |

**Por que estas y no otras:**

→ **Conta Simple** en vez de Holded o Quipu: si no necesitas contabilidad
compleja, es excesivo pagar 14€/mes. Conta Simple hace el 80% por 0€.

→ **Toggl** en vez de Clockify: interfaz mas limpia, la app movil no te
quita las ganas de usarla (Clockify si).

→ **Notion** en vez de Trello o Asana: mas flexible, hace de todo,
y la curva de aprendizaje ya merece la pena.

**Tu turno:** ¿Cual usas tu? ¿Hay alguna que añadirias a la lista?

---
*Recurso guardado en la categoria HERRAMIENTAS de la comunidad.*
**Hashtags:** #herramientas #autonomos #software #productividad #gratis
"""
crear_archivo("skool/posts/martes_post_skool.md", POST_SKOOL_MARTES)
ok("post Skool martes")

crear_post_imagen_html(
    titulo="5 Herramientas Gratis\npara Autónomos",
    cuerpo="""Conta Simple — facturas y IVA gratis
Toggl Track — control del tiempo
Notion — tu segundo cerebro
Calendly — agendar sin emails
Apollo.io — encontrar clientes""",
    nombre="martes-post-herramientas",
    color1="#0f172a", color2="#10b981",
)
ok("imagen post Instagram martes")

CAPTION_MARTES = """Antes de gastar un euro en software, lee esto. 👇

5 herramientas 100% gratuitas que uso cada día como autónomo en España:

01 — Conta Simple (facturas + IVA)
02 — Toggl Track (control del tiempo)
03 — Notion (gestión y notas)
04 — Calendly (agendar reuniones)
05 — Apollo.io (encontrar clientes)

Todas con tutorial de configuración en nuestra comunidad gratuita (link en bio 👆)

¿Cuál usas tú? ¿Me falta alguna? 👇

#autonomos #herramientasdigitales #freelance #productividad #softwaregratis #autonomosespana #negociodigital #trabajarporcuentapropia"""
crear_archivo("skool/redes/martes_caption_instagram.txt", CAPTION_MARTES)
crear_archivo("skool/redes/martes_caption_tiktok.txt",
    "Antes de gastar un euro en software como autónomo, escucha esto 👇 #autonomo #herramientas #freelance #dinero")
ok("captions redes martes")


# ══════════════════════════════════════════════════════════════
#  MIERCOLES — Debate: Cuanto cobras
# ══════════════════════════════════════════════════════════════
sep("MIERCOLES — Debate precios y tarifas")

POST_SKOOL_MIERCOLES = """# POST SKOOL — Miercoles semana 1
**Categoria:** Debates
**Tipo:** Pregunta directa — tablas de precios

---
## Pregunta del miercoles: ¿Cuanto cobras por hora? (sin tabues)

Voy directo al grano porque es una pregunta que nadie hace en voz alta
y todos queremos que alguien responda.

¿Cuanto cobras por hora o por proyecto?

No te pido el numero exacto si no quieres. Pero si me interesa saber:
→ Sector (diseno, programacion, consultoria, marketing, otro)
→ Anos de experiencia
→ Rango aproximado (menos de 30€/h, 30-60€/h, 60-100€/h, mas de 100€/h)
→ Cobras por hora o por proyecto cerrado

**Por que importa esto:**

El 70% de los autonomos que acaban de empezar cobran un 40% menos
de lo que deberían. Lo se porque yo tambien lo hice.

Y la unica forma de saber si estas en precio de mercado es hablar
con otros autonomos de tu sector. Cosa que casi nadie hace.

Este hilo es el lugar para hacerlo.

Yo empiezo: [DATOS DEL ADMIN]

---
*Si prefieres responder anonimamente, escribe tu sector y rango
sin dar tu nombre. Todo vale.*
"""
crear_archivo("skool/posts/miercoles_post_skool.md", POST_SKOOL_MIERCOLES)
ok("post Skool miercoles")

# Carousel Instagram (brief detallado)
CAROUSEL_IG = """# Carousel Instagram — Miercoles semana 1
**Titulo:** Cuanto deberías cobrar como autónomo en España (guia real)
**Slides:** 7 | **Formato:** 1080x1350 (retrato)

## SLIDE 1 — Portada
Fondo: #1a3a5c
Texto grande: "¿Cobras lo que mereces?"
Subtexto: "La guia que nadie te da"
Icono: emoji 💰

## SLIDE 2 — El problema
Texto: "El 70% de los autónomos nuevos cobran un 40% menos de lo que deberían."
Subtexto: "¿Por qué? Porque nadie les enseñó a calcular su precio mínimo."

## SLIDE 3 — La formula
Titulo: "Tu precio mínimo = ?"
Formula visual:
  Gastos mensuales (fijo + variable)
  ÷ Horas facturables al mes
  × Factor de incertidumbre (1.3)
  = Tu precio mínimo por hora

## SLIDE 4 — Ejemplo real
Titulo: "Ejemplo: diseñador freelance"
- Gastos: 2.200€/mes
- Horas facturables: 100h/mes (de 160h totales)
- Factor: ×1.3
- Precio mínimo: 28,6€/hora
- Precio recomendado: 40-55€/hora

## SLIDE 5 — El error más común
Titulo: "El error: cobrar lo que 'parece razonable'"
Texto: "El precio razonable es el que cubre tus costes + genera beneficio.
No el que te da miedo cobrar."

## SLIDE 6 — Sectores de referencia
Tabla orientativa (rangos España 2026):
- Diseño gráfico: 25-65€/h
- Programación: 40-90€/h
- Copywriting: 30-70€/h
- Consultoría: 50-150€/h
- Marketing digital: 35-80€/h

## SLIDE 7 — CTA
Titulo: "¿Cuanto cobras tú?"
Texto: "Comparte en nuestra comunidad gratuita y descubre cómo compara con tu sector"
CTA: "Únete gratis — link en bio"
Logo + @autonomosespana
"""
crear_archivo("skool/posts/miercoles_carousel_instagram.md", CAROUSEL_IG)
ok("brief carousel Instagram miercoles")

crear_post_imagen_html(
    titulo="¿Cobras lo que mereces\ncomo autónomo?",
    cuerpo="""El 70% cobra un 40% menos de lo que debería
Formula: gastos ÷ horas × 1.3
Diseño: 25-65€/h | Dev: 40-90€/h
Marketing: 35-80€/h | Consultoría: 50-150€/h
Descarga la guía completa → link en bio""",
    nombre="miercoles-cobrar-autonomo",
    color1="#7c3aed", color2="#f4821f",
)
ok("imagen post miercoles")

CAPTION_MIER = """El 70% de los autónomos nuevos cobran un 40% menos de lo que deberían. 💸

¿Por qué? Porque nadie les enseñó a calcular su precio mínimo.

Desliza para ver la fórmula exacta y los rangos por sector en España 👉

¿En qué rango estás tú? Cuéntanos abajo (sin tabúes) 👇

#autonomos #precios #freelance #tarifas #cuantocobrar #autonomosespana #negociodigital #emprendimiento"""
crear_archivo("skool/redes/miercoles_caption_instagram.txt", CAPTION_MIER)
crear_archivo("skool/redes/miercoles_post_linkedin.txt",
"""El error más caro que cometí como autónomo: cobrar lo que me parecía "razonable".

El precio razonable no existe. Existe el precio que cubre tus costes y genera beneficio.

Fórmula que uso ahora:
→ Suma todos tus gastos mensuales (fijos + variables + impuestos estimados)
→ Divide entre las horas que realmente puedes facturar al mes (no las que trabajas, las que cobras)
→ Multiplica por 1.3 (colchón para vacaciones, bajas, meses flojos)
→ Ese es tu precio mínimo. Lo que cobres por encima es tu beneficio real.

¿En qué rango estás? ¿Cobras por hora o por proyecto cerrado?

Llevamos esta conversación a nuestra comunidad gratuita de autónomos españoles. Link en comentarios.

#autonomos #freelance #precios #negocio #emprendimiento""")
ok("captions miercoles")


# ══════════════════════════════════════════════════════════════
#  JUEVES — Video tutorial: Como facturar en 2026
# ══════════════════════════════════════════════════════════════
sep("JUEVES — Video tutorial facturacion 2026")

SCRIPT_JUEVES = """
Si eres autonomo en Espana y aun no tienes claro como facturar correctamente
en 2026, este video es para ti. En ocho minutos te explico todo lo que
necesitas saber. Sin tecnicismos. Sin rollos.

Primero, lo basico: que debe tener una factura legal en Espana.
Numero de factura correlativo. Fecha de emision. Tus datos completos:
nombre o razon social, NIF, direccion. Datos del cliente: lo mismo.
Descripcion del servicio. Base imponible. IVA (normalmente el veintiuno
por ciento). Retencion si aplica (habitualmente el quince por ciento
si el cliente es empresa). Total.

Segundo: el IVA. Si eres autonomo persona fisica en regimen general,
cargas un veintiuno por ciento de IVA. Ese dinero no es tuyo.
Lo cobras al cliente y lo ingresas a Hacienda cada trimestre en el modelo
tres cero tres. No lo gastes.

Tercero: la retencion. Si tu cliente es una empresa o autonomo espanol,
generalmente te aplican una retencion del quince por ciento en el IRPF.
Eso significa que te pagan menos, pero tu ya esas pagando impuestos
adelantados. Se descuenta en tu declaracion anual.

Cuarto: el modelo ciento treinta. Si eres autonomo en estimacion directa
y tus clientes no te retienen, tienes que presentar este modelo cada
trimestre para pagar el IRPF a cuenta. Tu gestor te dira si aplica.

Quinto: herramientas. Para facturar, las opciones gratuitas como
Conta Simple o Invoice Ninja son suficientes para la mayoria.
Si necesitas algo mas robusto, Quipu desde nueve euros al mes
o Holded desde catorce.

Y el consejo mas importante: guarda todas tus facturas, tanto las
que emites como las que recibes. Cuatro anos de prescripcion en Espana
y no quieres buscar un gasto de hace tres anos en tu correo.

En la descripcion tienes el link a la comunidad gratuita donde hemos
preparado una plantilla de factura lista para usar y una guia completa.

Si te ha quedado alguna duda, dejala en los comentarios. Leo todos.
"""

crear_archivo("skool/videos/jueves_script_tutorial_facturacion.md",
    f"# Script — Tutorial Facturacion 2026\n**Formato:** YouTube 8-10 min\n**Publicacion:** Jueves semana 1\n\n{SCRIPT_JUEVES}")
ok("script tutorial facturacion")

generar_srt(SCRIPT_JUEVES, "jueves-tutorial-facturacion")
ok("SRT subtitulos tutorial")

crear_thumbnail_html(
    titulo="Cómo Facturar\nen España 2026",
    subtitulo="IVA · Retenciones · Modelo 303 · Herramientas gratis",
    nombre="jueves-thumbnail-facturacion",
    color_fondo="#1e3a2f",
    color_acento="#10b981",
)
ok("thumbnail facturacion")

generar_descripcion_youtube(
    titulo="Cómo facturar correctamente en España en 2026 — Guía completa para autónomos",
    script=SCRIPT_JUEVES,
    tags="facturar autonomo, IVA autonomo, modelo 303, factura autonomo españa, como facturar españa 2026"
)
ok("descripcion YouTube facturacion")

POST_SKOOL_JUEVES = """# POST SKOOL — Jueves semana 1
**Categoria:** Dinero y Finanzas
**Tipo:** Tutorial con recurso descargable

---
## Como facturar correctamente en 2026: la guia que le envio a todo autonomo nuevo

Cada semana me llegan mensajes de autonomos que llevan meses facturando
mal. No por descuido, sino porque nadie se lo explico bien.

Esta semana lo arreglamos.

**Los 5 puntos que toda factura correcta necesita:**

1. **Numero correlativo** — no puedes saltarte numeros ni repetirlos
2. **IVA 21%** — ese dinero es de Hacienda, no tuyo. No lo gastes.
3. **Retencion 15%** — si tu cliente es empresa, te la aplican ellos
4. **Modelo 303** — trimestral, para ingresar el IVA cobrado
5. **Guardar TODO** — 4 anos de prescripcion en Espana

**Herramientas recomendadas:**
→ Gratis: Conta Simple, Invoice Ninja
→ De pago: Quipu (9€/mes), Holded (14€/mes)

**Recurso:** Plantilla de factura lista para personalizar. En la categoria
RECURSOS de la comunidad, carpeta DINERO.

¿Tienes alguna duda sobre facturacion? Pregunta abajo, respondo hoy.

---
**Hashtags:** #facturacion #autonomos #IVA #impuestos #hacienda
"""
crear_archivo("skool/posts/jueves_post_skool.md", POST_SKOOL_JUEVES)
ok("post Skool jueves")

# Plantilla de factura
PLANTILLA_FACTURA = """# PLANTILLA DE FACTURA — Autonomo Espana
*(Copia y adapta a tu caso)*

---
**FACTURA Nº:** [AÑO]-[NUMERO]  *(ej: 2026-0001)*
**FECHA:** [DD/MM/AAAA]

---
**EMISOR (tus datos):**
Nombre completo: ___________________
NIF/DNI: ___________________
Direccion: ___________________
CP y ciudad: ___________________
Email: ___________________

**RECEPTOR (datos del cliente):**
Empresa/Nombre: ___________________
CIF/NIF: ___________________
Direccion: ___________________

---
**CONCEPTO:**
| Descripcion | Cantidad | Precio unidad | Total |
|-------------|----------|---------------|-------|
| [Servicio prestado] | 1 | [IMPORTE]€ | [IMPORTE]€ |

---
**BASE IMPONIBLE:** [IMPORTE]€
**IVA 21%:** +[IMPORTE]€
**IRPF -15%:** -[IMPORTE]€  *(solo si el receptor es empresa/autonomo en ES)*
**TOTAL A PAGAR:** [IMPORTE]€

---
**Forma de pago:** Transferencia bancaria
**IBAN:** ES__ ____ ____ ____ ____ ____
**Titular:** [TU NOMBRE]
**Plazo de pago:** [X] dias desde emision

---
*Factura emitida por [TU NOMBRE], autonomo/a en regimen de estimacion directa,
con NIF [TU NIF], segun lo acordado. El tipo de retencion aplicable del 15%
se ingresara en Hacienda por el pagador en concepto de IRPF a cuenta.*
"""
crear_archivo("skool/recursos/plantilla_factura.md", PLANTILLA_FACTURA)
ok("plantilla factura descargable")

EMAIL_NEWSLETTER = """# EMAIL NEWSLETTER — Jueves semana 1
**Asunto:** ⚡ Como facturar bien en 2026 (guia + plantilla gratis)
**Preview text:** El error de facturacion que cometen casi todos los autonomos nuevos

---
Hola [NOMBRE],

Esta semana en la comunidad hemos tocado uno de los temas que mas dudas genera:
la facturacion.

No el "como se hace una factura" — eso lo explica cualquier tutorial de 2015.
Sino el "como no cagarla" — que es lo que nadie te cuenta.

**Los 3 errores mas frecuentes que veo:**

**1. Mezclar el IVA con tus ingresos**
El IVA que cobras al cliente no es tuyo. Es de Hacienda. Si lo gastas,
tendras un problema serio en la declaracion trimestral.
Consejo: abre una cuenta separada o ponlo en un sobre virtual nada mas cobrar.

**2. No saber si te aplica retencion**
Si tu cliente es una empresa espanola, generalmente te aplicaran
un 15% de retencion en tu factura. Eso reduce el importe que cobras,
pero ya estas pagando IRPF por adelantado. No te alarmes.

**3. No guardar facturas de gastos**
Todo lo que gastes relacionado con tu actividad es deducible.
Software, suscripciones, material, telefono (parcialmente), formacion.
Sin factura a tu nombre, no puedes deducirlo.

**Esta semana en la comunidad:**
→ [VIDEO] Tutorial completo de facturacion 2026 (8 min)
→ [RECURSO] Plantilla de factura lista para usar
→ [DEBATE] ¿Cuanto cobras? — ya hay 47 respuestas, muy interesante

Unete si aun no estas: [LINK SKOOL]

Hasta la semana que viene,
[NOMBRE]

---
*Te llega este email porque te apuntaste a la newsletter de Autonomos Espana.
Si no quieres recibirla, [darte de baja aqui].*
"""
crear_archivo("skool/emails/jueves_newsletter_semana1.md", EMAIL_NEWSLETTER)
ok("email newsletter jueves")

crear_post_imagen_html(
    titulo="Cómo Facturar\ncomo Autónomo en 2026",
    cuerpo="""Número correlativo obligatorio
IVA 21% — es de Hacienda, no tuyo
Retención 15% si el cliente es empresa
Modelo 303 cada trimestre
Guarda TODAS las facturas (4 años)""",
    nombre="jueves-facturacion-post",
    color1="#1e3a2f", color2="#10b981",
)
ok("imagen Instagram jueves")


# ══════════════════════════════════════════════════════════════
#  VIERNES — Resumen + Teaser semana 2
# ══════════════════════════════════════════════════════════════
sep("VIERNES — Resumen semana 1 + teaser semana 2")

POST_SKOOL_VIERNES = """# POST SKOOL — Viernes semana 1
**Categoria:** Comunidad
**Tipo:** Resumen semanal + celebracion + teaser

---
## Semana 1 completada — aqui lo que hemos hecho juntos

Primera semana y ya somos [N] autonomos aqui dentro. No esta mal.

**Resumen de lo que ha pasado esta semana:**

📹 **Video:** Como facturar en 2026 — [N] visualizaciones
🛠️ **Recurso:** 5 herramientas gratis para autonomos — [N] guardados
💬 **Debate estrella:** ¿Cuanto cobras? — [N] respuestas (lee el hilo, vale mucho)
🏆 **Miembro de la semana:** [NOMBRE] por [LOGRO]

**Lo mejor que hemos aprendido juntos:**
→ [INSIGHT 1 del debate de precios]
→ [INSIGHT 2 de los comentarios]
→ [HERRAMIENTA descubierta por un miembro]

---
**Semana que viene:**

Lunes — Como conseguir tu primer cliente (o el siguiente) sin publicidad
Miercoles — Debate: ¿Contrato siempre, o a veces sin contrato?
Jueves — Tutorial: LinkedIn para autonomos que odian LinkedIn
Viernes — Recurso especial: el kit de bienvenida para nuevos clientes

Comparte este post con un autonomo que conozcas. Cuantos mas seamos,
mejor para todos.

Buen fin de semana. 🙌
"""
crear_archivo("skool/posts/viernes_resumen_semana1.md", POST_SKOOL_VIERNES)
ok("post Skool viernes")

CAPTION_VIERNES = """Semana 1 completada. 🙌

Esta semana en la comunidad:
→ Tutorial completo de facturación 2026
→ Las 5 herramientas gratis para autónomos
→ Debate real sobre tarifas (muy recomendable leerlo)
→ Plantilla de factura lista para usar

Todo gratuito. Todo en nuestra comunidad Skool.

La semana que viene: cómo conseguir clientes sin publicidad + LinkedIn para autónomos.

¿Te apuntas? Link en bio 👆

#autonomosespana #freelance #semana1 #autonomo #emprendimiento #resumen"""
crear_archivo("skool/redes/viernes_caption_instagram.txt", CAPTION_VIERNES)
ok("caption viernes")

# Teaser semana 2 (Reel script)
SCRIPT_TEASER_S2 = """La semana que viene en Autonomos Espana.

Lunes: como conseguir tu primer cliente sin gastar en publicidad.
El metodo exacto que use yo. Sin anuncios. Sin agencia. Sin magia.

Miercoles: debate sobre contratos. ¿Siempre o no siempre?
Hay autonomos que llevan anos sin contrato y les va bien.
Otros que por no tener contrato perdieron miles de euros.

Jueves: LinkedIn para autonomos que odian LinkedIn.
Si, yo tambien lo odiaba. Ahora me trae dos o tres clientes al mes.
Te cuento como en un tutorial de diez minutos.

Unete a la comunidad gratis antes del lunes para no perderte nada.
Link en bio.
"""
crear_archivo("skool/videos/viernes_script_teaser_semana2.md",
    f"# Script Teaser Semana 2\n**Formato:** Reel/Story 30 segundos\n\n{SCRIPT_TEASER_S2}")
generar_srt(SCRIPT_TEASER_S2, "viernes-teaser-semana2", segundos_por_linea=3.0)
ok("script + SRT teaser semana 2")


# ══════════════════════════════════════════════════════════════
#  CSV para programacion en Buffer / Later / Meta Business
# ══════════════════════════════════════════════════════════════
sep("CSV calendario para Buffer / Later")

filas_csv = [
    ["2026-06-01", "Instagram", "Imagen", "Bienvenido a Autónomos España 🇪🇸", "output/skool/posts_img/lunes-post-instagram.html", "#autonomosespana #autonomo #freelance"],
    ["2026-06-01", "TikTok",    "Video",  "Video bienvenida comunidad",          "output/skool/videos/lunes_script_bienvenida.md",  "#autonomo #comunidad"],
    ["2026-06-01", "LinkedIn",  "Texto",  "Presentacion comunidad Autonomos España", "", "#autonomos #freelance #comunidad"],
    ["2026-06-02", "Instagram", "Reel",   "5 herramientas gratis para autonomos", "output/skool/videos/martes_script_reel_herramientas.md", "#herramientas #gratis #autonomo"],
    ["2026-06-02", "TikTok",    "Video",  "5 apps gratis para autonomos espanoles", "output/skool/videos/martes_script_reel_herramientas.md", "#autonomo #herramientas"],
    ["2026-06-03", "Instagram", "Carousel","Cuanto deberias cobrar como autonomo", "output/skool/posts/miercoles_carousel_instagram.md", "#precios #autonomo #freelance"],
    ["2026-06-03", "LinkedIn",  "Texto",  "El error mas caro que cometi como autonomo", "output/skool/redes/miercoles_post_linkedin.txt", "#autonomos #precios"],
    ["2026-06-04", "Instagram", "Imagen", "Como facturar en 2026",                "output/skool/posts_img/jueves-facturacion-post.html", "#facturacion #IVA #autonomo"],
    ["2026-06-04", "YouTube",   "Video",  "Como facturar en Espana 2026",          "output/skool/videos/jueves_script_tutorial_facturacion.md", "tutorial facturacion autonomo"],
    ["2026-06-05", "Instagram", "Imagen", "Resumen semana 1",                      "", "#autonomosespana #semana1 #resumen"],
    ["2026-06-05", "TikTok",    "Reel",   "Teaser semana 2",                       "output/skool/videos/viernes_script_teaser_semana2.md", "#autonomo #semana2 #teaser"],
]

exportar_csv(
    filas=filas_csv,
    nombre="calendario-semana1-buffer",
    cabeceras=["Fecha", "Plataforma", "Tipo", "Descripcion", "Archivo_contenido", "Hashtags"]
)
ok("CSV calendario semana 1 para Buffer/Later")


# ══════════════════════════════════════════════════════════════
#  RESUMEN FINAL
# ══════════════════════════════════════════════════════════════
sep("RESUMEN COMPLETO SEMANA 1")
archivos = sorted([f for f in (OUT).rglob("*") if f.is_file()])
# Mostrar solo los nuevos de skool (excluyendo los de la sesion anterior)
nuevos = [f for f in archivos if any(d in str(f) for d in
          ["videos","posts","redes","emails","recursos","thumbnails","posts_img"])]
for f in sorted(nuevos):
    print(f"  {str(f.relative_to(OUT.parent.parent))} ({f.stat().st_size:,}b)")
print(f"\nTotal nuevos: {len(nuevos)} archivos")
print(f"\nPARA USAR:")
print(f"  Scripts de video  → output/skool/videos/")
print(f"  SRT subtitulos    → output/skool/videos/*.srt")
print(f"  Thumbnails HTML   → output/skool/thumbnails/ (abre en navegador, captura)")
print(f"  Imagenes posts    → output/skool/posts_img/ (abre en navegador, captura)")
print(f"  Posts Skool       → output/skool/posts/")
print(f"  Captions redes    → output/skool/redes/")
print(f"  Email newsletter  → output/skool/emails/")
print(f"  Plantilla factura → output/skool/recursos/")
print(f"  CSV Buffer/Later  → output/skool/calendario-semana1-buffer.csv")

# Actualiza panel
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("gp", PROJECT_ROOT/"scripts"/"generar_panel.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); mod.generar()
    print("\n[OK] Panel actualizado")
except Exception as e:
    print(f"[panel] {e}")

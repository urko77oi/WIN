"""Genera el contenido COMPLETO de la semana 2 de la comunidad Skool.

Tema semana 2: MONETIZACION Y CLIENTES
  Lunes    — "Como conseguir tu primer cliente online" video + SRT + thumbnail + desc YT
             Post Skool + imagen IG + caption
  Martes   — "Cuanto cobrar como autonomo" Reel script + SRT + thumbnail
             Post Skool + imagen IG + captions IG/TikTok
  Miercoles — "El error que cometemos todos al poner precios" post debate Skool
             Carousel Instagram (7 slides) + post imagen + LinkedIn
  Jueves   — "Propuesta de servicios que cierra ventas" video completo (8-10 min)
             Script + SRT + thumbnail + desc YT + post Skool
             Plantilla descargable propuesta + email newsletter
  Viernes  — Resumen semana 2 + teaser semana 3 + CSV calendario Buffer

Total: ~20 archivos listos para publicar.
"""
from __future__ import annotations
import sys
from pathlib import Path

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

def sep(titulo): print(f"\n{'='*55}\n  {titulo}\n{'='*55}")
def ok(etiqueta): print(f"  [OK] {etiqueta}")


# ================================================================
#  LUNES — Como conseguir tu primer cliente online
# ================================================================
sep("LUNES — Primer cliente online")

SCRIPT_LUNES = """
Conseguir el primer cliente es lo mas dificil. No porque no tengas
habilidades. Sino porque no sabes donde buscar ni como presentarte.

Hoy te cuento el metodo exacto que uso yo y que han usado cientos
de autonomos de esta comunidad para conseguir su primer cliente online
en menos de 30 dias.

No necesitas una web perfecta. No necesitas miles de seguidores.
Solo necesitas tres cosas: claridad, oferta y contacto directo.

PASO 1: DEFINE A QUIEN AYUDAS CON UNA FRASE
Muchos autonomos fallan aqui. Dicen "ayudo a empresas a mejorar su marketing".
Eso no dice nada.

La formula correcta es: ayudo a [QUIEN] a conseguir [RESULTADO] sin [PROBLEMA].

Ejemplo real: ayudo a fisioterapeutas a conseguir 10 pacientes nuevos al mes
sin depender de Instagram.

Cuando tienes esa frase, todo lo demas se vuelve mas facil.

PASO 2: IDENTIFICA DONDE ESTAN TUS CLIENTES
No intentes estar en todos lados. Elige uno.
Si tu cliente es una empresa: LinkedIn.
Si tu cliente es un particular: Instagram o TikTok.
Si tu cliente busca soluciones concretas: Google (SEO local o anuncios).

Empieza por donde ya esta tu cliente, no por donde tu quieres estar.

PASO 3: LA OFERTA DE ENTRADA
El error clasico es empezar con el servicio mas caro.
Primero necesitas confianza. Crea una oferta de entrada de bajo riesgo.

Puede ser una auditoria gratuita de 30 minutos.
Puede ser un mini-servicio de 97 euros que resuelve un problema concreto.
Puede ser un PDF o herramienta gratuita que muestre lo que sabes hacer.

El objetivo de la oferta de entrada no es ganar dinero.
Es conseguir el primer SI.

PASO 4: CONTACTO DIRECTO (el que nadie quiere hacer)
Aqui es donde la mayoria se para. El miedo al rechazo.

Pero la matematica es simple: si contactas a 20 personas bien elegidas
con un mensaje personalizado, conseguiras 2-3 reuniones.
Y de esas 2-3 reuniones, 1 se convierte en cliente.

El mensaje no es un copy-paste. Es genuino. Estudia a la persona,
menciona algo concreto de su negocio, y ofrece valor antes de pedir algo.

CIERRE:
Tu primer cliente no va a venir solo. Lo tienes que ir a buscar.
Pero una vez que tienes uno, todo cambia: tienes un caso de exito,
tienes confianza, y tienes una referencia.

En el post de hoy en la comunidad te dejo una plantilla de mensaje
de primer contacto que puedes adaptar a tu sector.

Si ya tienes tu primer cliente online, cuéntanoslo en los comentarios.
Si aun no lo tienes, esta semana es la semana. Vamos.
"""

crear_archivo(
    "skool/videos/lunes_s2_script_primer_cliente.md",
    f"# Script: Como conseguir tu primer cliente online\n\n{SCRIPT_LUNES.strip()}"
)
ok("script primer cliente")

generar_srt(SCRIPT_LUNES, "lunes-s2-primer-cliente", segundos_por_linea=4.5)
ok("SRT subtitulos")

crear_thumbnail_html(
    titulo="Tu PRIMER CLIENTE online",
    subtitulo="El metodo en 4 pasos que funciona",
    nombre="lunes-s2-thumbnail-primer-cliente",
    color_fondo="#1a1a2e",
    color_acento="#e94560"
)
ok("thumbnail HTML")

generar_descripcion_youtube(
    titulo="Como conseguir tu PRIMER CLIENTE online siendo autonomo",
    script=SCRIPT_LUNES,
    tags="primer cliente autonomo, conseguir clientes online, freelance espana, autonomo espana, como conseguir clientes, freelance principiante, emprender espana, autonomos espana, primer cliente freelance"
)
ok("descripcion YouTube")

POST_SKOOL_LUNES = """# Como conseguir tu primer cliente online (el metodo real)

Llevo anos viendo autonomos paralizados en este punto.
Tienen habilidades. Tienen ganas. Pero no tienen clientes.

El problema no es la habilidad. Es el sistema.

Hoy te doy el metodo en 4 pasos que funciona incluso si partes de cero:

**Paso 1 — Define con precision a quien ayudas**
No "empresas". No "particulares". Algo concreto.
Usa esta formula: *Ayudo a [QUIEN] a conseguir [RESULTADO] sin [PROBLEMA]*

**Paso 2 — Identifica donde esta tu cliente**
Un canal. Solo uno. No intentes estar en todos.
LinkedIn para B2B. Instagram/TikTok para consumidor final. Google para busqueda activa.

**Paso 3 — Crea una oferta de entrada de bajo riesgo**
Algo que cueste poco dinero o poco tiempo para el cliente.
El objetivo es el primer SI, no el primer gran cheque.

**Paso 4 — Contacto directo personalizado**
20 mensajes bien dirigidos = 2-3 reuniones = 1 cliente.
La matematica no falla si el mensaje es genuino.

---
En el video de hoy en YouTube lo explico con ejemplos reales de cada sector.

PREGUNTA PARA LA COMUNIDAD:
Como conseguiste tu primer cliente? Cuanto tardaste?
Los que ya tienen varios: que consejo darias a los que empiezan?
"""

crear_archivo("skool/posts/lunes_s2_post_skool.md", POST_SKOOL_LUNES.strip())
ok("post Skool lunes")

crear_post_imagen_html(
    titulo="Tu PRIMER CLIENTE online",
    cuerpo="4 pasos. Sin web perfecta.\nSin miles de seguidores.\nSolo claridad + accion.",
    nombre="lunes-s2-post-instagram",
    formato="cuadrado",
    color1="#1a1a2e",
    color2="#e94560"
)
ok("imagen Instagram lunes")

CAPTION_LUNES = """El primer cliente es el mas dificil.
No por falta de habilidad. Por falta de sistema.

4 pasos para conseguirlo en menos de 30 dias:

1. Define a quien ayudas con precision
2. Elige UN solo canal donde estan
3. Crea una oferta de entrada de bajo riesgo
4. Contacto directo. Personalizado. Sin miedo.

La matematica no falla: 20 mensajes bien dirigidos = 1 cliente.

En el link de la bio tienes el video completo con plantillas incluidas.

Autonomo que ya tiene clientes: que cambio todo para ti?
Cuéntalo en comentarios para ayudar a los que empiezan.

#autonomoespana #freelanceespana #conseguirclientes #emprender #autonomo
#trabajardesdecase #primercliente #freelance #negocioonline #emprendedor"""

crear_archivo("skool/redes/lunes_s2_caption_instagram.txt", CAPTION_LUNES.strip())
ok("caption Instagram lunes")


# ================================================================
#  MARTES — Cuanto cobrar como autonomo (Reel)
# ================================================================
sep("MARTES — Cuanto cobrar como autonomo")

SCRIPT_MARTES = """
Cuanto cobrar. La pregunta que mas ansiedad genera entre autonomos.
Y casi siempre nos equivocamos en la misma direccion: cobramos de menos.

En 60 segundos te explico por que pasa y como calcularlo correctamente.

El error numero uno: calcular el precio basandote en lo que cobra la competencia.
Eso es una trampa. Acabas en una guerra de precios que nadie gana.

El error numero dos: poner un precio que te parece "justo" sin hacer los numeros.
Y luego a final de mes descubres que trabajaste 200 horas y ganaste menos que un empleado.

La formula correcta tiene tres elementos:

Primero: tus gastos reales al mes. No los que crees que tienes. Los reales.
Alquiler, cuota autonomo, herramientas, impuestos, seguro. Sumalo todo.

Segundo: las horas que puedes facturar de verdad. Ojo: no las que trabajas.
Las que puedes cobrar al cliente. Normalmente entre 15 y 20 horas semanales.

Tercero: el margen para crecer. Si cobras justo lo que necesitas para sobrevivir,
nunca podras invertir en formacion, herramientas o marketing.

Divide tus gastos reales por las horas facturables. Añade el 40% de margen.
Ese es tu precio minimo. Por debajo de eso, estas perdiendo dinero.

Y si ese numero te da miedo ofrecerselo a un cliente, el problema
no es el precio. Es que aun no has comunicado bien el valor que aportas.

Comentame: cuanto llevas cobrando y si crees que es justo para lo que das.
"""

crear_archivo(
    "skool/videos/martes_s2_script_reel_precios.md",
    f"# Script Reel: Cuanto cobrar como autonomo\n\n{SCRIPT_MARTES.strip()}"
)
ok("script Reel precios")

generar_srt(SCRIPT_MARTES, "martes-s2-reel-precios", segundos_por_linea=3.5)
ok("SRT subtitulos Reel")

crear_thumbnail_html(
    titulo="Cuanto COBRAR como autonomo",
    subtitulo="La formula que nadie te enseno",
    nombre="martes-s2-thumbnail-precios",
    color_fondo="#0d1117",
    color_acento="#f0b429"
)
ok("thumbnail precios")

POST_SKOOL_MARTES = """# La formula para saber cuanto cobrar (y dejar de cobrar de menos)

El 80% de los autonomos cobra de menos. No por falta de valor. Por falta de calculo.

Haz este ejercicio ahora mismo:

**1. Calcula tus gastos reales al mes**
- Cuota autonomo: ~300-350 EUR
- IRPF estimado (guarda el 20-25% de cada factura)
- Herramientas y suscripciones
- Alquiler/hipoteca + suministros
- Alimentacion y transporte
- Imprevistos (reserva el 10%)
TOTAL = X EUR/mes

**2. Calcula tus horas facturables reales**
Semanas laborables al mes: ~3.5 (descontando festivos, vacaciones, enfermedad)
Horas por semana que PUEDES COBRAR (no que trabajas): 15-20h
TOTAL = 52-70 horas/mes facturables

**3. Tu precio minimo por hora**
X EUR / 52 horas = precio de supervivencia
Añade 40% de margen = precio real sostenible

**Ejemplo:**
Gastos: 2.500 EUR/mes
Horas facturables: 60h/mes
Precio minimo: 2.500/60 = 41,7 EUR/h
Con margen 40%: **58 EUR/hora**

Si cobras menos, estas perdiendo dinero aunque no lo veas.

---
Cuantas horas facturables tienes al mes? Que te da el calculo?
Ponlo en comentarios sin miedo, aqui no juzgamos.
"""

crear_archivo("skool/posts/martes_s2_post_skool.md", POST_SKOOL_MARTES.strip())
ok("post Skool martes")

crear_post_imagen_html(
    titulo="Cuanto cobrar: la formula",
    cuerpo="Gastos reales / horas facturables\n+ 40% de margen\n= tu precio minimo real",
    nombre="martes-s2-post-precios",
    formato="cuadrado",
    color1="#0d1117",
    color2="#f0b429"
)
ok("imagen Instagram martes")

CAPTION_MARTES_IG = """Cobrando de menos? Probablemente si.

La formula que nadie te enseno en el cole:

Tus gastos reales al mes
dividido por tus horas facturables
mas un 40% de margen

= tu precio MINIMO por hora

Si cobras menos, trabajas para pagar facturas. No para crecer.

En el link de la bio tienes la calculadora completa con ejemplo real.

Cuanto cobras ahora? Te da el numero o te quedas corto?

#autonomoespana #tarifas #cuantocobrar #freelance #preciosfreelance
#autonomo #emprender #negocio #trabajarporlibre"""

CAPTION_MARTES_TT = """Cuanto cobrar como autonomo: la formula real en 60 segundos #autonomo #freelance #emprender #dinero #trabajo"""

crear_archivo("skool/redes/martes_s2_caption_instagram.txt", CAPTION_MARTES_IG.strip())
crear_archivo("skool/redes/martes_s2_caption_tiktok.txt", CAPTION_MARTES_TT.strip())
ok("captions redes martes")


# ================================================================
#  MIERCOLES — El error al poner precios (debate)
# ================================================================
sep("MIERCOLES — El error al poner precios")

POST_SKOOL_MIERCOLES = """# El error que casi todos cometemos al poner precios

Voy a ser directo porque esto nos ha costado dinero a todos.

Cuando empezamos como autonomos, ponemos precios bajos por tres razones:
1. Miedo a que nos digan que no
2. Sindrome del impostor ("no se si valgo tanto")
3. Compararnos con el mas barato de la competencia

Y esos precios bajos generan tres problemas que nadie te cuenta:

**Problema 1: Atraes al peor tipo de cliente**
El cliente que elige por precio siempre pedira mas de lo que paga,
pagara tarde, y te cambiara por alguien 10 euros mas barato el proximo mes.

**Problema 2: No puedes dar tu mejor trabajo**
Si cobras poco, tienes que coger muchos clientes para llegar a fin de mes.
Con muchos clientes, cada uno recibe menos atencion. Calidad cae. Reputacion sufre.

**Problema 3: Es casi imposible subir precios despues**
Una vez que un cliente te paga 500 EUR al mes, decirle que ahora son 900
es una conversacion muy dificil. Mucho mas facil empezar en 900.

La solucion no es cobrar mas de la noche a la manana.
Es entender que el precio comunica valor.
Un precio bajo dice "soy el mas barato". Un precio justo dice "soy el que vale".

---
PREGUNTA DE HOY:
Alguna vez has subido precios a un cliente existente?
Como fue la conversacion? Cuanto subiste?

(Si nunca lo has hecho y llevas mas de 6 meses con el mismo cliente,
este es tu aviso de que probablemente ya toca.)
"""

crear_archivo("skool/posts/miercoles_s2_post_skool.md", POST_SKOOL_MIERCOLES.strip())
ok("post debate Skool miercoles")

CAROUSEL_MIERCOLES = """# Brief Carousel Instagram Miercoles S2
# "Los 3 errores de precio que te cuestan clientes"

## Slide 1 — Portada
Titulo: LOS 3 ERRORES DE PRECIO que te cuestan los MEJORES clientes
Subtitulo: (y como evitarlos)
Estilo: fondo oscuro, texto blanco, icono de precio tachado en rojo

## Slide 2 — Error 1
Titulo: ERROR #1: Copiar el precio de la competencia
Cuerpo:
- La competencia puede estar perdiendo dinero y no saberlo
- Sus costes no son los tuyos
- Sus clientes no son los tuyos
Conclusion: Pon tu precio basandote en tu valor, no en el de otro

## Slide 3 — Error 2
Titulo: ERROR #2: Precio "por lo que sea justo"
Cuerpo:
- Sin calculos = precio a ciegas
- "Justo" para quien? Para ti o para el cliente?
- El 70% de autonomos cobra menos de lo que necesita para crecer
Conclusion: Haz los numeros. Siempre.

## Slide 4 — Error 3
Titulo: ERROR #3: No subir precios nunca
Cuerpo:
- La inflacion es real: lo que era suficiente hace 2 anos ya no lo es
- Tus habilidades han mejorado: tu precio deberia reflejarlo
- Un cliente que lleva 1 ano contigo te conoce y valora mas que uno nuevo
Conclusion: Revision de precios = minimo 1 vez al ano

## Slide 5 — El efecto oculto
Titulo: El problema que nadie te cuenta sobre los precios bajos
Cuerpo:
- Precio bajo = cliente que elige por precio
- Cliente de precio = el mas exigente, el que mas tarda en pagar
- Y el primero en irse cuando encuentra a alguien 10 euros mas barato

## Slide 6 — La solucion
Titulo: Como subir precios sin perder clientes
Cuerpo:
1. Avisa con 30-60 dias de antelacion
2. Justifica con resultados que has conseguido para ellos
3. Ofrece cerrar proyectos actuales al precio actual
4. El cliente que se va... probablemente era el que mas problemas daba

## Slide 7 — CTA
Titulo: Unete a Autonomos Espana
Cuerpo: Cada semana compartimos estrategias reales de precios, negociacion y clientes
CTA: Link en bio -> comunidad gratuita
"""

crear_archivo("skool/posts/miercoles_s2_carousel_instagram.md", CAROUSEL_MIERCOLES.strip())
ok("brief carousel Instagram miercoles")

crear_post_imagen_html(
    titulo="3 errores de precio",
    cuerpo="Que alejan a tus mejores clientes\n(y como evitarlos)",
    nombre="miercoles-s2-precios-error",
    formato="cuadrado",
    color1="#2d1b69",
    color2="#c084fc"
)
ok("imagen post miercoles")

CAPTION_MIERCOLES = """El precio bajo no te consigue mas clientes. Te consigue los peores.

3 errores de precio que alejan a los buenos clientes:

1. Copiar el precio de la competencia (sin saber sus costes)
2. Poner lo que "parece justo" sin hacer los calculos
3. No subir precios nunca (aunque lleves anos con el cliente)

Guardalo porque lo necesitaras mas pronto de lo que crees.

Alguna vez has subido precios? Como fue?

#autonomoespana #precios #freelance #negocio #emprender #tarifas
#autonomo #clientes #negociacion"""

LINKEDIN_MIERCOLES = """Llevo hablando con autonomos desde hace anos y hay un patron claro:

Los que mas trabajan no son los que mas ganan.
Los que mejor comunican su valor, si.

El precio es comunicacion. Un precio bajo no dice "soy accesible".
Dice "yo mismo no creo que valga mas".

Y los clientes lo notan.

He visto autonomos doblar sus ingresos sin conseguir un solo cliente nuevo.
Solo subiendo precios a los clientes actuales y siendo mas selectivos con los nuevos.

El proceso:
1. Calcula tu precio real (gastos + horas facturables + margen)
2. Identifica a tus 2-3 mejores clientes (los que pagan bien y son agradables)
3. Mantenlos. Sube precios al resto o no los renueves.
4. Con ese tiempo libre, busca clientes al nuevo precio.

No es rapido. Pero es el camino sostenible.

Que ha cambiado en tu negocio cuando subiste precios?

#autonomos #freelance #pricing #negocios #emprendimiento #pymes"""

crear_archivo("skool/redes/miercoles_s2_caption_instagram.txt", CAPTION_MIERCOLES.strip())
crear_archivo("skool/redes/miercoles_s2_post_linkedin.txt", LINKEDIN_MIERCOLES.strip())
ok("captions miercoles")


# ================================================================
#  JUEVES — Propuesta de servicios que cierra ventas
# ================================================================
sep("JUEVES — Propuesta de servicios que cierra ventas")

SCRIPT_JUEVES = """
Una propuesta de servicios mal hecha te puede costar el cliente
aunque hayas hecho una reunion perfecta.
Hoy te enseño la estructura exacta que cierra ventas.

La mayoria de autonomos manda una propuesta que es basicamente una lista de precios.
El cliente la ve, la compara con otras, y elige el mas barato.
Porque no le diste otra razon para elegirte.

Una propuesta que cierra ventas no es una lista de precios.
Es un documento que reafirma que entiendes el problema del cliente,
que tienes la solucion exacta, y que eres la persona obvia para ejecutarla.

La estructura tiene 5 partes.

PARTE 1: EL PROBLEMA DEL CLIENTE (en sus propias palabras)
Empieza por lo que te contaron en la reunion. Literalmente.
"En nuestra conversacion del martes me comentaste que vuestra pagina web
no esta generando leads y que llevas 6 meses sin conseguir un cliente por internet."

Cuando el cliente lee sus propios problemas en tu propuesta, siente que le escuchas.
Y confiar en alguien que te escucha es mucho mas facil.

PARTE 2: EL COSTE DEL PROBLEMA (lo que les esta costando no resolverlo)
Esto es lo que diferencia las propuestas que se contratan de las que se archivan.
Ayuda al cliente a visualizar lo que esta perdiendo cada mes que no actua.

"Cada mes sin una web optimizada son aproximadamente X clientes potenciales
que van a la competencia. A tu ticket medio de Y euros, eso son Z euros al mes."

Si pones los numeros reales, el precio de tu servicio deja de parecer un gasto.
Parece una inversion con retorno claro.

PARTE 3: TU SOLUCION ESPECIFICA
Aqui va lo que vas a hacer. Pero no como una lista de tareas.
Como un proceso con logica.

"En los primeros 15 dias haremos X. Esto resuelve Y.
En el mes 1 implementaremos Z. El resultado esperado es W."

El cliente tiene que poder visualizar el camino completo.

PARTE 4: POR QUE TU
No lo pongas como autobombo. Ponlo como tranquilidad para el cliente.
Caso de exito parecido. Una cifra concreta de resultado. Un testimonio.

Si no tienes historial, pon tu proceso. La metodologia detallada inspira confianza
aunque no tengas casos de exito todavia.

PARTE 5: INVERSION Y SIGUIENTES PASOS
Al precio llamale "inversion", no "coste". Las palabras importan.
Da dos o tres opciones: basico, estandar, premium.
Los clientes con opciones se quedan. Los clientes con precio unico, comparan.

Y termina con los siguientes pasos concretos.
No "dimelo si te interesa". Eso es pasivo.
"El siguiente paso es una llamada de 20 minutos el jueves o viernes.
Que te viene mejor?"

CIERRE:
Una buena propuesta no es una obra de arte. Es un documento funcional
que responde a la pregunta del cliente: por que tu y por que ahora.

En la comunidad os dejo hoy la plantilla completa lista para personalizar.
"""

crear_archivo(
    "skool/videos/jueves_s2_script_propuesta_servicios.md",
    f"# Script: Propuesta de servicios que cierra ventas\n\n{SCRIPT_JUEVES.strip()}"
)
ok("script propuesta servicios")

generar_srt(SCRIPT_JUEVES, "jueves-s2-propuesta-servicios", segundos_por_linea=4.5)
ok("SRT subtitulos")

crear_thumbnail_html(
    titulo="Propuesta que CIERRA VENTAS",
    subtitulo="La estructura exacta en 5 partes",
    nombre="jueves-s2-thumbnail-propuesta",
    color_fondo="#0f3460",
    color_acento="#e94560"
)
ok("thumbnail propuesta")

generar_descripcion_youtube(
    titulo="Propuesta de servicios que CIERRA VENTAS (estructura en 5 partes)",
    script=SCRIPT_JUEVES,
    tags="propuesta de servicios, como hacer una propuesta, cerrar ventas autonomo, propuesta comercial freelance, conseguir clientes autonomo, ventas freelance, autonomo espana, propuesta de servicios ejemplo, freelance espana"
)
ok("descripcion YouTube")

POST_SKOOL_JUEVES = """# La propuesta de servicios que cierra ventas (plantilla incluida)

Mandas propuestas y no cierras? El problema casi siempre esta en la estructura.

La mayoria de propuestas son listas de precios. Eso obliga al cliente a comparar.
Una buena propuesta hace que el cliente piense: "este me entiende, quiero trabajar con el".

**La estructura en 5 partes:**

**1. El problema del cliente** (en sus propias palabras)
Demuestra que escuchaste. El cliente se reconoce y baja la guardia.

**2. El coste de no resolverlo**
Cuanto le esta costando cada mes no tener solucion?
Cuando el cliente ve el numero, tu precio se convierte en inversion.

**3. Tu solucion con hoja de ruta**
No una lista de tareas. Un proceso con logica y resultados esperados.
"En las primeras 2 semanas haremos X, lo que consigue Y..."

**4. Por que tu**
Un caso de exito parecido o tu metodologia detallada.
Inspira confianza, no arrogancia.

**5. Opciones de inversion + siguiente paso concreto**
Tres opciones (basico/estandar/premium) y un siguiente paso especifico.
No "dimelo si te interesa". "Hablamos el jueves o el viernes, que te viene mejor?"

---
La plantilla completa (Word + PDF) la encontrais en la seccion Recursos de la comunidad.

Pregunta de hoy: en cuantos dias mandais vuestra propuesta tras la primera reunion?
Hay un tiempo ideal (pista: no es ni el mismo dia ni una semana despues).
"""

crear_archivo("skool/posts/jueves_s2_post_skool.md", POST_SKOOL_JUEVES.strip())
ok("post Skool jueves")

PLANTILLA_PROPUESTA = """# Plantilla: Propuesta de Servicios Profesional

**[TU NOMBRE / NOMBRE DE TU NEGOCIO]**
Propuesta para: [NOMBRE CLIENTE / EMPRESA]
Fecha: [FECHA]
Valida hasta: [FECHA + 15 DIAS]

---

## 1. Lo que me contaste

En nuestra conversacion del [DIA], me comentaste que:

- [PROBLEMA 1 en las palabras del cliente]
- [PROBLEMA 2]
- [OBJETIVO que quieren conseguir]

Entiendo que esto te esta afectando porque [CONSECUENCIA NEGATIVA].

---

## 2. Lo que te esta costando no resolverlo

Cada mes sin una solucion a [PROBLEMA] supone aproximadamente:
- [CALCULO: X clientes perdidos x Y euros de ticket medio = Z euros/mes]
- [OTRO IMPACTO CUANTIFICABLE]

En 6 meses, eso equivale a [TOTAL SEMESTRAL] en oportunidades perdidas.

---

## 3. Lo que propongo

**Fase 1 — [NOMBRE] (semanas 1-2)**
Que hago: [ACCIONES]
Resultado esperado: [ENTREGABLE O METRICA]

**Fase 2 — [NOMBRE] (semanas 3-4)**
Que hago: [ACCIONES]
Resultado esperado: [ENTREGABLE O METRICA]

**Fase 3 — [NOMBRE] (mes 2)**
Que hago: [ACCIONES]
Resultado esperado: [ENTREGABLE O METRICA]

---

## 4. Por que yo

He ayudado a [TIPO DE CLIENTE SIMILAR] a conseguir [RESULTADO CONCRETO].

[CASO DE EXITO BREVE: empresa/sector, problema, solucion, resultado medible]

Mi metodologia se basa en [2-3 PRINCIPIOS CLAVE que te diferencian].

---

## 5. Opciones de inversion

| | ESENCIAL | PROFESIONAL | COMPLETO |
|---|---|---|---|
| [SERVICIO BASE] | Incluido | Incluido | Incluido |
| [EXTRA 1] | No | Incluido | Incluido |
| [EXTRA 2] | No | No | Incluido |
| Sesiones de seguimiento | 1/mes | 2/mes | Semanal |
| **Inversion** | **[PRECIO]** | **[PRECIO]** | **[PRECIO]** |

---

## Siguiente paso

Si quieres avanzar, el siguiente paso es una llamada de 20 minutos
para resolver dudas y confirmar los detalles.

Te viene mejor el [DIA] o el [DIA]?

Puedes responder a este email o escribirme directamente al [TELEFONO/WHATSAPP].

---
*[TU NOMBRE] | [EMAIL] | [WEB si tienes]*
"""

crear_archivo("skool/recursos/plantilla_propuesta_servicios.md", PLANTILLA_PROPUESTA.strip())
ok("plantilla propuesta descargable")

NEWSLETTER_JUEVES = """# Newsletter Semana 2 — Jueves
# Asunto: La propuesta que casi nunca mandan (pero que siempre cierra)

---

Hola [NOMBRE],

Esta semana en la comunidad hemos estado hablando de precios y clientes.

Y hoy quiero cerrar la semana con algo practico:
la estructura de propuesta que uso (y que cambia el resultado completamente).

**El problema con las propuestas normales**

La mayoria de autonomos manda una propuesta que es una lista de precios.
El cliente la compara con otras tres listas de precios. Y elige el mas barato.

No porque seas malo. Sino porque no le diste otra razon para elegirte.

**La propuesta que cierra tiene 5 partes:**

1. El problema del cliente (en sus propias palabras)
2. El coste de no resolverlo (con numeros)
3. Tu solucion con hoja de ruta clara
4. Por que tu (caso de exito o metodologia)
5. Opciones de inversion + siguiente paso concreto

El cambio clave esta en el punto 2.
Cuando el cliente ve cuanto le cuesta cada mes no tener solucion,
tu precio deja de ser un gasto y se convierte en una inversion con retorno.

**Esta semana en la comunidad:**

- Video completo: como estructurar cada parte con ejemplos reales
- Plantilla descargable (Word y PDF) en la seccion Recursos
- Post de debate: en cuanto tiempo mandais la propuesta tras la primera reunion?

Si aun no eres miembro, entra gratis este mes:
[LINK COMUNIDAD SKOOL]

Hasta la semana que viene,
[TU NOMBRE]

---
*Recibes este email porque te apuntaste a la lista de Autonomos Espana.*
*Para darte de baja: [LINK BAJA]*
"""

crear_archivo("skool/emails/jueves_s2_newsletter.md", NEWSLETTER_JUEVES.strip())
ok("email newsletter jueves")

crear_post_imagen_html(
    titulo="Propuesta que cierra",
    cuerpo="5 partes. La mayoria manda solo\nuna lista de precios.\nTu no.",
    nombre="jueves-s2-post-propuesta",
    formato="cuadrado",
    color1="#0f3460",
    color2="#e94560"
)
ok("imagen Instagram jueves")


# ================================================================
#  VIERNES — Resumen semana 2 + teaser semana 3
# ================================================================
sep("VIERNES — Resumen semana 2 + teaser semana 3")

POST_SKOOL_VIERNES = """# Resumen Semana 2 — Monetizacion y Clientes

Cerramos la semana 2. Repaso rapido de lo que hemos cubierto:

**Lunes:** Como conseguir tu primer cliente online
-> El metodo en 4 pasos. La formula para llegar al primer SI.

**Martes:** Cuanto cobrar como autonomo
-> La formula real: gastos / horas facturables + 40% de margen = precio minimo sostenible.

**Miercoles:** El error que cometemos todos al poner precios
-> Por que el precio bajo atrae al peor tipo de cliente (y como cambiarlo).

**Jueves:** Propuesta de servicios que cierra ventas
-> La estructura en 5 partes + plantilla descargable en Recursos.

---

Si has aplicado algo esta semana, cuéntanoslo.
No importa si es pequeño. Cada paso cuenta.

---

SEMANA 3 — Lo que viene:
La semana que viene entramos en **productividad y gestion del tiempo** del autonomo.
Porque ganar mas no sirve de nada si trabajas 60 horas para conseguirlo.

Temas: metodo Pomodoro adaptado al freelance, batching de tareas,
como decir NO a proyectos que no encajan, y herramientas de gestion del tiempo
que cuestan 0 euros.

Hasta el lunes. Buen fin de semana.
"""

crear_archivo("skool/posts/viernes_s2_resumen.md", POST_SKOOL_VIERNES.strip())
ok("post resumen Skool viernes")

CAPTION_VIERNES = """Semana 2 completada.

Esta semana en la comunidad hemos hablado de lo que a nadie le gusta hablar: dinero.

- Como conseguir el primer cliente (metodo real, sin secretos)
- Cuanto cobrar y por que casi todos cobramos de menos
- Los errores de precio que alejan a los buenos clientes
- Propuesta de servicios que cierra ventas (plantilla gratis)

La semana 3 viene fuerte: productividad real del autonomo.
Porque ganar mas no vale nada si trabajas 60 horas para conseguirlo.

Unete gratis en el link de la bio.

#autonomoespana #freelance #emprender #autonomo #clientes #precios
#productividad #negocio #trabajo"""

crear_archivo("skool/redes/viernes_s2_caption_instagram.txt", CAPTION_VIERNES.strip())
ok("caption viernes")

SCRIPT_TEASER = """
La semana 3 de la comunidad llega con un tema que todos necesitamos
pero nadie quiere admitir que tiene problema: el tiempo.

No falta tiempo. Falta sistema.
La semana que viene te enseñamos el sistema.
"""

crear_archivo(
    "skool/videos/viernes_s2_script_teaser_semana3.md",
    f"# Script Teaser Semana 3\n\n{SCRIPT_TEASER.strip()}"
)
generar_srt(SCRIPT_TEASER, "viernes-s2-teaser-semana3", segundos_por_linea=3.0)
ok("script + SRT teaser semana 3")


# ================================================================
#  CSV CALENDARIO SEMANA 2
# ================================================================
sep("CSV calendario para Buffer / Later")

FILAS_CSV = [
    ["2026-05-18", "YouTube",   "Video largo",  "Como conseguir tu primer cliente online",             "videos/lunes_s2_script_primer_cliente.md",   "#autonomoespana #freelance #conseguirclientes"],
    ["2026-05-18", "Instagram", "Post imagen",  "Tu primer cliente online: 4 pasos",                  "posts_img/lunes-s2-post-instagram.html",      "#autonomoespana #primercliente #freelance"],
    ["2026-05-18", "Instagram", "Caption",      "Caption lunes semana 2",                              "redes/lunes_s2_caption_instagram.txt",        "#autonomo #emprender #primercliente"],
    ["2026-05-19", "TikTok",    "Reel/Short",   "Cuanto cobrar como autonomo: la formula en 60s",     "videos/martes_s2_script_reel_precios.md",     "#autonomo #cuantocobrar #freelance #dinero"],
    ["2026-05-19", "Instagram", "Reel",         "Cuanto cobrar como autonomo: la formula real",       "videos/martes_s2_script_reel_precios.md",     "#precios #autonomo #freelanceespana"],
    ["2026-05-19", "Instagram", "Post imagen",  "Formula cuanto cobrar",                              "posts_img/martes-s2-post-precios.html",       "#tarifas #autonomo #cuantocobrar"],
    ["2026-05-20", "Instagram", "Carousel",     "3 errores de precio que alejan tus mejores clientes","posts/miercoles_s2_carousel_instagram.md",    "#precios #freelance #negocio"],
    ["2026-05-20", "LinkedIn",  "Articulo",     "Por que los autonomos que mas trabajan no son los que mas ganan", "redes/miercoles_s2_post_linkedin.txt", "#autonomos #freelance #pricing"],
    ["2026-05-21", "YouTube",   "Video largo",  "Propuesta de servicios que cierra ventas",           "videos/jueves_s2_script_propuesta_servicios.md","#propuesta #ventas #autonomo #cerrarventas"],
    ["2026-05-21", "Instagram", "Post imagen",  "Propuesta que cierra ventas: 5 partes",              "posts_img/jueves-s2-post-propuesta.html",     "#ventas #propuesta #freelance"],
    ["2026-05-21", "Email",     "Newsletter",   "La propuesta que casi nunca mandan",                 "emails/jueves_s2_newsletter.md",             ""],
    ["2026-05-22", "Instagram", "Post texto",   "Resumen semana 2 + teaser semana 3",                 "redes/viernes_s2_caption_instagram.txt",     "#autonomoespana #semana2 #resumen"],
    ["2026-05-22", "TikTok",    "Teaser",       "Teaser semana 3: productividad del autonomo",        "videos/viernes_s2_script_teaser_semana3.md", "#autonomo #productividad #teaser"],
]

CABECERAS = ["Fecha", "Plataforma", "Tipo", "Descripcion", "Archivo_contenido", "Hashtags"]
exportar_csv(FILAS_CSV, "calendario-semana2-buffer", CABECERAS)
ok("CSV calendario semana 2 para Buffer/Later")


# ================================================================
#  RESUMEN FINAL
# ================================================================
sep("RESUMEN COMPLETO SEMANA 2")

archivos = sorted((OUT).rglob("*s2*"), key=lambda f: f.stat().st_size if f.is_file() else 0, reverse=True)
for f in archivos:
    if f.is_file():
        rel = f.relative_to(PROJECT_ROOT / "output")
        print(f"  {rel} ({f.stat().st_size:,}b)")

total = len([f for f in archivos if f.is_file()])
print(f"\nTotal nuevos: {total} archivos")

print("""
PARA USAR:
  Scripts de video  -> output/skool/videos/
  SRT subtitulos    -> output/skool/videos/*.srt
  Thumbnails HTML   -> output/skool/thumbnails/ (abre en navegador, captura)
  Imagenes posts    -> output/skool/posts_img/ (abre en navegador, captura)
  Posts Skool       -> output/skool/posts/
  Captions redes    -> output/skool/redes/
  Email newsletter  -> output/skool/emails/
  Plantilla propuesta -> output/skool/recursos/
  CSV Buffer/Later  -> output/skool/calendario-semana2-buffer.csv
""")

# Actualizar panel
try:
    import importlib.util, os
    spec = importlib.util.spec_from_file_location("panel", PROJECT_ROOT / "scripts" / "generar_panel.py")
    panel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(panel)
    print("[OK] Panel actualizado")
except Exception as e:
    print(f"[Panel] {e}")

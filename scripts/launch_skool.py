"""Sesion de lanzamiento de la comunidad Skool para autonomos españoles.

Cada agente genera su parte. Sin LLM real = genera estructura y plantillas mock.
Con LLM real = contenido completo y personalizado.
"""
from __future__ import annotations
import sys, os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

COMUNIDAD    = "Autonomos España — La Comunidad"
DESCRIPCION  = """Comunidad hibrida (free + premium) para autonomos espanoles.
Free: recursos, herramientas, networking, 1 post semanal de valor.
Premium (19€/mes): cursos, mentoria grupal, acceso directo a expertos,
plantillas y herramientas exclusivas."""
PROPUESTA    = "El lugar donde los autonomos espanoles aprenden, se conectan y crecen juntos"

# ── Modo real: usa LLM. Modo mock: genera estructura sin LLM ──────────
MODO = os.getenv("LLM_MODE", "mock").strip().lower()

def separador(titulo: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")

# ── Si hay LLM, usa agentes. Si no, genera directo. ──────────────────
if MODO == "real":
    from agents.pixel.pixel  import Pixel
    from agents.emma.emma    import Emma
    from agents.guion.guion  import Guion
    from agents.viral.viral  import Viral

    separador("PIXEL — Identidad Visual")
    Pixel().crear_identidad_visual(f"{COMUNIDAD}\n{DESCRIPCION}")
    print("[OK] Identidad visual generada")

    separador("EMMA — Onboarding + Normas")
    Emma().crear_onboarding(f"{COMUNIDAD}\n{DESCRIPCION}")
    Emma().crear_normas(COMUNIDAD)
    print("[OK] Onboarding y normas generados")

    separador("GUION — Hooks + Script de presentacion")
    Guion().crear_hooks("autonomos espana herramientas digitales comunidad", n=10)
    Guion().crear_script_video("Por que todo autonomo espanol necesita una comunidad", "youtube", "3-5min")
    print("[OK] Hooks y script generados")

    separador("VIRAL — Estrategia + Bios + Calendario junio")
    Viral().crear_estrategia(COMUNIDAD, "Conseguir 500 miembros free y 50 premium en 90 dias")
    Viral().crear_bio_perfiles(COMUNIDAD, PROPUESTA)
    Viral().crear_calendario(COMUNIDAD, "Junio 2026", posts_semana=5)
    print("[OK] Estrategia, bios y calendario generados")

else:
    # Sin LLM: genera directamente toda la estructura en Python
    _out = PROJECT_ROOT / "output" / "skool"

    # ── IDENTIDAD VISUAL ──────────────────────────────────────────────
    separador("PIXEL — Identidad Visual")
    (_out / "identidad").mkdir(parents=True, exist_ok=True)

    identidad = """# Identidad Visual — Autonomos España

## Paleta de colores
| Nombre       | Hex       | Uso                                      |
|--------------|-----------|------------------------------------------|
| Azul noche   | #1a3a5c   | Fondo principal, headers, texto importante |
| Naranja      | #f4821f   | CTAs, acentos, highlights                |
| Verde exito  | #10b981   | Logros, confirmaciones, elementos positivos |
| Gris claro   | #f7f9fc   | Fondos secundarios, cards                |
| Blanco       | #ffffff   | Texto sobre oscuro, espaciado            |

## Tipografia
- **Titulares**: Inter Bold / Poppins Bold (Google Fonts)
- **Cuerpo**: Inter Regular / System fonts stack
- **Codigo/numeros destacados**: JetBrains Mono

## Estilo visual
- Moderno, limpio, profesional pero cercano
- Sin gradientes complicados — planos o gradiente sutil
- Iconos: estilo outline (Heroicons o Lucide)
- Fotografia: personas reales trabajando, no stock americano
- Mood: "esto es serio pero no aburrido"

## Especificaciones Canva

### Banner Skool (1920 x 384 px)
- Fondo: #1a3a5c
- Texto principal: "Autonomos España" — Inter Bold 72px, blanco
- Subtexto: "Aprende. Conécta. Crece." — Inter Regular 36px, #f4821f
- Elemento derecho: ilustracion minimalista de persona con ordenador
- Logo: esquina superior izquierda

### Thumbnail post (1200 x 675 px)
- Fondo: blanco o #f7f9fc
- Titulo en grande: Inter Bold 60px, #1a3a5c
- Franja inferior: #1a3a5c con texto blanco (nombre comunidad)
- Icono o emoji grande centrado o izquierda

### Foto de perfil comunidad (400 x 400 px)
- Fondo circular: #1a3a5c
- Iniciales "AE" o icono simple
- Sin texto pequeno (no se ve en miniaturas)
"""
    (_out / "identidad" / "identidad_visual.md").write_text(identidad, encoding="utf-8")

    # Banner HTML
    banner_html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  body { margin: 0; font-family: -apple-system, "Segoe UI", Roboto, sans-serif; }
  .banner {
    width: 1920px; height: 384px;
    background: linear-gradient(135deg, #1a3a5c 0%, #264d7a 100%);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 80px;
    box-sizing: border-box;
  }
  .left h1 { color: #fff; font-size: 72px; font-weight: 800; margin: 0 0 12px; letter-spacing: -2px; }
  .left p  { color: #f4821f; font-size: 36px; margin: 0; font-weight: 600; }
  .badge {
    background: #f4821f; color: #fff;
    padding: 16px 32px; border-radius: 50px;
    font-size: 24px; font-weight: 700;
  }
</style></head>
<body>
<div class="banner">
  <div class="left">
    <h1>Autónomos España</h1>
    <p>Aprende · Conéctate · Crece</p>
  </div>
  <div class="badge">Comunidad Gratuita</div>
</div>
</body></html>"""
    (_out / "identidad" / "banner_preview.html").write_text(banner_html, encoding="utf-8")
    print("[OK] Identidad visual + banner HTML generados")

    # ── ONBOARDING ────────────────────────────────────────────────────
    separador("EMMA — Onboarding + Normas")
    (_out / "onboarding").mkdir(parents=True, exist_ok=True)

    onboarding = """# Secuencia de Onboarding — Autonomos España

## Mensaje de bienvenida (aparece al unirse)

---
¡Bienvenido/a a Autonomos España! 👋

Me alegra que hayas dado el paso. Esta comunidad la creamos para que
los autonomos espanoles tengamos un lugar donde aprender, conectarnos
y crecer — sin rollos, sin vendehúmos, sin teoría que no funciona aqui.

**Tus primeros pasos (5 minutos):**

1. 📌 **Presentate** en el hilo de presentaciones — di quien eres, a que te dedicas y que buscas aqui
2. 📚 **Explora las categorias** — hay recursos gratis, herramientas curadas y debates
3. 🎯 **Haz el primer reto** — publica la herramienta digital que mas te ha cambiado la vida como autonomo
4. 🔔 **Activa notificaciones** — asi no te pierdes nada importante

Si tienes dudas, escribe aqui mismo. Estamos para ayudarte.

¡Bienvenido al equipo!
---

## Tour de la comunidad (mensaje dia 2)

---
¡Hola de nuevo! Ya llevas 24h con nosotros. ¿Has explorado todo?

Aqui te dejo un mapa rapido:

📁 **RECURSOS GRATUITOS** — Herramientas, plantillas y guias que usamos
💬 **DEBATES** — Preguntas, dudas, experiencias reales
🏆 **RETOS SEMANALES** — Cada lunes un reto practico para mejorar tu negocio
📣 **NOVEDADES** — Actualizaciones de la comunidad y nuevos recursos

¿Quieres más? Con **Premium** (19€/mes) accedes a:
✅ Cursos completos (facturacion, clientes, productividad)
✅ Mentoria grupal mensual en directo
✅ Plantillas y herramientas exclusivas
✅ Acceso directo a expertos

[Mas info sobre Premium →]
---

## Primer reto para nuevos miembros

**Reto de bienvenida: "Tu herramienta clave"**

Publica en la categoria RECURSOS:
- Nombre de la herramienta
- Para que la usas
- Por que la recomiendas
- Nivel de precio (gratis / pago / freemium)

El mejor recurso de la semana lo destacamos en el post del viernes. 🏆

## Diferencia Free vs Premium

| | Free | Premium (19€/mes) |
|---|---|---|
| Acceso a la comunidad | ✅ | ✅ |
| Recursos y herramientas | ✅ basicos | ✅ todos |
| Debates y networking | ✅ | ✅ |
| Cursos completos | ❌ | ✅ |
| Mentoria grupal mensual | ❌ | ✅ |
| Plantillas exclusivas | ❌ | ✅ |
| Soporte directo | ❌ | ✅ |
"""
    (_out / "onboarding" / "onboarding_completo.md").write_text(onboarding, encoding="utf-8")

    normas = """# Normas de la Comunidad — Autonomos España

## Para que estamos aqui

Esta comunidad existe para que los autonomos espanoles tengamos un lugar
donde aprender cosas que funcionan de verdad, conectar con gente como nosotros
y crecer juntos. Sin teorias, sin humo, sin spam.

## Lo que SI esta permitido (y animamos)

✅ Preguntar cualquier cosa relacionada con ser autonomo en España
✅ Compartir herramientas, recursos y experiencias reales
✅ Pedir y dar feedback honesto
✅ Celebrar logros (por pequenos que sean)
✅ Debatir ideas — se puede estar en desacuerdo con respeto
✅ Recomendar servicios o herramientas que genuinamente usas

## Lo que NO esta permitido

❌ Spam o autopromociones sin aportar valor primero
❌ Vender directamente sin permiso del admin
❌ Contenido ofensivo, politico o discriminatorio
❌ Informacion falsa o enganos
❌ Scraping o extraccion de datos de miembros

## Como pedir ayuda

1. Busca primero si ya se ha respondido antes
2. Explica tu situacion con contexto (cuanto mas detalle, mejor respuesta)
3. Si alguien te ayuda, cierra el hilo con el resultado
4. Si la respuesta te ha servido, dale un ❤️ al que te ayudo

## Consecuencias

Primera vez: aviso privado
Segunda vez: restriccion temporal
Tercera vez: expulsion de la comunidad

Cualquier duda, escribe al admin. Esto no es una dictadura — las normas
pueden cambiar si la comunidad lo decide.
"""
    (_out / "onboarding" / "normas.md").write_text(normas, encoding="utf-8")
    print("[OK] Onboarding y normas generados")

    # ── HOOKS + SCRIPT ────────────────────────────────────────────────
    separador("GUION — Hooks + Script de presentacion")
    (_out / "contenido").mkdir(parents=True, exist_ok=True)

    hooks = """# Hooks de Alto Impacto — Autonomos España

## Reels / TikTok (max 10 palabras)
1. "Si eres autonomo en España, esto te cambia la vida"
2. "El error que cometen el 90% de los autonomos espanoles"
3. "La herramienta que uso todos los dias y es gratis"
4. "Cuanto cobrar como autonomo — la formula exacta"
5. "Por que tu gestor no te cuenta esto"

## Titulares YouTube
1. "Las 10 herramientas digitales que uso como autonomo (y cuanto me cuestan)"
2. "Como consegui mis primeros 5 clientes sin publicidad de pago"
3. "Todo lo que nadie te explica cuando te das de alta como autonomo"
4. "De 0 a 3.000€/mes: mi historia real como autonomo en España"
5. "La estrategia de precios que doblo mis ingresos en 6 meses"

## Asuntos de email
1. "⚡ La herramienta que te ahorra 3 horas esta semana"
2. "Lo que aprendi facturando 40.000€ como autonomo (sin secretos)"

## Titulares post Skool
1. "Pregunta directa: ¿Cuanto cobras por hora? (sin tabues)"
2. "Recurso de la semana: esta herramienta me ahorra 5h semanales"
"""
    (_out / "contenido" / "hooks.md").write_text(hooks, encoding="utf-8")

    script = """# Script — Video de Presentacion de la Comunidad
## Formato: YouTube / Reel corto | Duracion: 3-4 min

---
### [HOOK — 0 a 15 segundos]
[CAMARA: plano medio, directo a camara, fondo neutro o workspace]

"Llevas tiempo queriendo conectar con otros autonomos que entienden
tus problemas de verdad. No tu familia, no tus amigos con contrato fijo.
Otros autonomos. Los que saben lo que es esperar que te paguen,
gestionar clientes dificiles y preguntarte si lo estas haciendo bien.
Esta comunidad existe para eso."

---
### [PROBLEMA — 15 a 60 segundos]
[CAMARA: se puede cortar con texto en pantalla con estadisticas]

"Ser autonomo en España puede ser increible. Pero tambien puede ser
muy solitario. No hay un jefe que te guie. No hay un compa de oficina
que te cuente el truco. Y cuando tienes una duda — de facturacion,
de precios, de herramientas — acabas en un foro de hace 10 anos
o en un video en ingles que no aplica aqui."

[TEXTO EN PANTALLA: "3,3 millones de autonomos en España. La mayoria, solos."]

---
### [SOLUCION — 60 a 120 segundos]
[CAMARA: muestra pantalla de Skool mientras hablas]

"Por eso creamos Autonomos España. Una comunidad donde encontraras:
recursos y herramientas curadas especificamente para el mercado espanol,
gente real con los mismos retos que tu, y respuestas a preguntas
que en Google no encuentras."

"Es gratis entrar. Y si quieres ir mas alla — cursos, mentoria,
plantillas exclusivas — tienes el nivel premium por 19 euros al mes.
Menos que una cena."

---
### [CTA FINAL — ultimos 30 segundos]
[CAMARA: directo a camara, tono mas personal]

"El link para unirte esta en la descripcion. Es gratis, tarda
30 segundos y puede ser la mejor decision que tomes esta semana.
Te veo dentro."

[TEXTO EN PANTALLA: URL de la comunidad Skool + "Unete gratis"]

---
### Notas de produccion
- Duracion total: 3-4 min (editar para Reel en 60 segundos con las partes clave)
- Musica de fondo: instrumental suave, no distractora
- Subtitulos: siempre activados (80% ve sin sonido en movil)
- Thumbnail: foto tuya + texto "Por fin una comunidad de verdad"
"""
    (_out / "contenido" / "script_presentacion.md").write_text(script, encoding="utf-8")

    posts = """# Posts de Engagement — Semana 1 a 4

## POST 1 — Presentacion (Lunes semana 1)
**Titulo:** ¿Quien eres y a que te dedicas?
**Cuerpo:**
Empezamos con lo mas importante: conocernos.

Cuéntanos en un comentario:
→ Tu nombre y a que te dedicas
→ Cuanto tiempo llevas como autonomo
→ Una cosa que te gustaria aprender o mejorar este mes

Yo empiezo: [presentacion del admin]

Te leo 👇
**CTA:** Comenta abajo — el primero que se presente se lleva un recurso exclusivo

---
## POST 2 — Educativo (Miercoles semana 1)
**Titulo:** La herramienta de facturacion mas infravalorada para autonomos españoles
**Cuerpo:**
Llevaba 2 años usando [herramienta cara] sin saber que existia [alternativa].

La diferencia: 47€/mes vs 0€/mes. Con las mismas funciones que yo usaba.

La herramienta: Conta Simple (version gratuita).
Lo que hace: facturas, gastos, calculo de IVA, exportacion para gestor.
Lo que no hace: contabilidad compleja (para eso ya esta tu gestor).

¿La conocias? ¿Que herramienta de facturacion usas tu?
**CTA:** Comparte la tuya abajo — estamos construyendo el directorio definitivo

---
## POST 3 — Debate (Viernes semana 1)
**Titulo:** Pregunta del viernes: ¿Cuanto cobras por hora?
**Cuerpo:**
Pregunta directa, sin tabues.

Uno de los mayores problemas de los autonomos es no saber si estamos
cobrando bien o regalando nuestro trabajo.

¿Cobras por hora o por proyecto?
¿Cuanto cobras? (rango aproximado, sin revelar nada que no quieras)
¿Como llegaste a ese numero?

No hay respuestas correctas. Solo datos reales que nos ayudan a todos.
**CTA:** Responde anonimamente si prefieres — aqui no se juzga

---
## POST 4 — Reto semanal (Lunes semana 2)
**Titulo:** Reto de la semana: audita tus suscripciones
**Cuerpo:**
Este lunes, un reto de 20 minutos que puede ahorrarte dinero:

1. Abre tu banco o tarjeta
2. Busca todos los cobros recurrentes del mes pasado
3. Por cada uno preguntate: ¿lo uso realmente? ¿hay alternativa gratis?
4. Cancela al menos una cosa que no necesitas

Comparte aqui: ¿cuanto te has ahorrado? ¿que has cancelado?

El autonomo con el mayor ahorro se lleva reconocimiento publico en el post del viernes 🏆
**CTA:** Comparte tu resultado antes del domingo

---
## POST 5 — Recurso (Miercoles semana 2)
**Titulo:** Plantilla gratis: propuesta comercial que convierte
**Cuerpo:**
Uno de los recursos mas pedidos: como estructurar una propuesta
que el cliente lea, entienda y firme.

He preparado una plantilla en Google Docs (copia y adapta):
[LINK]

Estructura:
✅ Resumen ejecutivo (1 parrafo, lo mas importante)
✅ Situacion actual del cliente (demuestra que has escuchado)
✅ Lo que propones (concreto, sin humo)
✅ Como lo hacemos (proceso claro)
✅ Inversion (precio claro, sin letra pequena)
✅ Proximos pasos (para cerrar hoy, no "ya te llamo")

¿La usas? Comenta que cambias o mejoras para tu sector.
**CTA:** Descarga gratis — solo necesitas tener cuenta en la comunidad
"""
    (_out / "contenido" / "posts_engagement.md").write_text(posts, encoding="utf-8")
    print("[OK] Hooks, script y posts de engagement generados")

    # ── REDES SOCIALES ────────────────────────────────────────────────
    separador("VIRAL — Estrategia + Bios + Calendario")
    (_out / "redes").mkdir(parents=True, exist_ok=True)

    estrategia = """# Estrategia de Redes Sociales — Autonomos España

## Objetivo
500 miembros free + 50 premium en 90 dias.
Conversion esperada: 10% de seguidores → visitan Skool. 20% de visitas → se unen.

## Perfil del seguidor ideal
- Autonomo espanol, 28-50 anos
- 1-5 anos de experiencia
- Factura entre 20.000-80.000€/ano
- Usa movil para consumir contenido (Instagram/TikTok)
- Usa LinkedIn para captar clientes
- Dolor principal: soledad, incertidumbre, falta de sistematizacion

## Tono y voz
- Directo: sin rodeos, sin padding
- Cercano: "tu" no "usted", como un colega que sabe mas que tu
- Honesto: datos reales, no promesas magicas
- Practico: cada post debe tener una accion concreta

## 5 Pilares de contenido
1. **Herramientas** — comparativas y guias de herramientas digitales
2. **Dinero** — precios, facturacion, impuestos, finanzas del autonomo
3. **Clientes** — como conseguirlos, retenerlos, cobrarlos
4. **Productividad** — sistemas, automatizacion, gestion del tiempo
5. **Comunidad** — logros de miembros, debates, retos

## Estrategia de hashtags

### Instagram
Principal: #autonomosespana #trabajarparati #freelanceespana
Secundarios: #autonomos #emprendedoresespana #negociodigital
Long tail: #herramientasdigitales #facturacionautonomo #clientesfreelance

### TikTok
#autonomo #freelance #trabajoindependiente #emprendimiento #dineroespana

### LinkedIn
#autonomos #freelance #emprendimiento #productividad #negociodigital

## Horarios optimos de publicacion
- **Instagram**: L-V a las 7:30h (antes del trabajo) y 20:00h
- **TikTok**: L-V a las 12:00h y 21:00h
- **LinkedIn**: M-J a las 8:00h y 12:30h (hora de comer)

## Embudo de conversion (seguidores → miembros Skool)
1. Post de valor → seguidor
2. Stories/Reels → engagement y confianza
3. Post con CTA explicito → visita al link de bio
4. Landing Skool convincente → se une gratis
5. Onboarding en Skool → considera premium

## Metricas clave (revisar cada lunes)
- Seguidores nuevos por plataforma
- Alcance organico por post
- CTR del link en bio
- Nuevos miembros Skool esa semana
- Conversion free → premium
"""
    (_out / "redes" / "estrategia.md").write_text(estrategia, encoding="utf-8")

    bios = """# Bios de Perfil — Autonomos España

## Instagram (max 150 caracteres)
```
Comunidad para autónomos 🇪🇸
Herramientas · Clientes · Dinero
Sin humo. Sin relleno. Solo lo que funciona.
👇 Únete gratis (link en bio)
```

## TikTok (max 80 caracteres)
```
Autónomos España 🇪🇸
Herramientas y trucos reales
Link: comunidad gratis 👇
```

## LinkedIn (max 220 caracteres)
```
Comunidad para autónomos españoles que quieren crecer sin depender de nadie.
Herramientas digitales, estrategias de captación y finanzas para freelances.
+500 autónomos ya dentro. Únete gratis →
```

## Skool (sin limite)
```
Bienvenido a Autónomos España, la comunidad donde los autónomos españoles
aprendemos, nos conectamos y crecemos juntos.

¿Para quién es esto?
Para autónomos, freelances y profesionales independientes en España que
quieren usar mejor la tecnología, conseguir más clientes y gestionar
mejor su dinero — sin teoría, sin vendehúmos, sin contenido en inglés
que no aplica aquí.

¿Qué encontrarás aquí?
→ Recursos y herramientas curadas para el mercado español
→ Debates reales sobre precios, clientes y facturación
→ Retos semanales prácticos
→ Una comunidad que entiende tus problemas de verdad

¿Cómo funciona?
Free: acceso a la comunidad, recursos básicos y networking
Premium (19€/mes): cursos completos, mentoría grupal mensual,
plantillas exclusivas y acceso directo a expertos

¿Cuánto cuesta unirse?
Gratis. Ahora mismo. Sin tarjeta.

Nos vemos dentro.
```
"""
    (_out / "redes" / "bios.md").write_text(bios, encoding="utf-8")

    calendario = """# Calendario Editorial — Junio 2026
## Autonomos España | 5 posts/semana/plataforma

| Dia | Plataforma | Tipo | Idea | CTA |
|-----|-----------|------|------|-----|
| Lun 1 | Instagram | Educativo | "3 herramientas gratis que uso cada dia como autonomo" | Link bio Skool |
| Lun 1 | TikTok | Hook rapido | "La app que me ahorra 2h a la semana (y es gratis)" | Link bio |
| Lun 1 | LinkedIn | Reflexion | "Lo que nadie te cuenta al hacerte autonomo en España" | CTA comunidad |
| Mar 2 | Instagram | Stories | Encuesta: "¿Cual es tu mayor problema como autonomo?" | Respuesta en DM |
| Mar 2 | TikTok | Tutorial | "Como facturar correctamente en 2026 paso a paso" | Comunidad |
| Mie 3 | Instagram | Carrusel | "5 errores de precio que cometen los autonomos nuevos" | Skool |
| Mie 3 | LinkedIn | Articulo corto | "Por que los autonomos espanoles cobran un 30% menos de lo que deberian" | |
| Jue 4 | TikTok | Detras camaras | "Mi setup de trabajo como autonomo (todo lo que uso)" | Link bio |
| Jue 4 | Instagram | Reel | "Si eres autonomo en España, necesitas saber esto" | Comunidad |
| Vie 5 | Todas | Logro miembro | "Esta semana [nombre] consiguio [logro]. Asi lo hizo." | Unirse free |
| Lun 8 | Instagram | Educativo | "Herramienta de la semana: [nombre]" | Demo + link |
| Mar 9 | TikTok | Debate | "¿Cobras por hora o por proyecto? Mi respuesta honesta" | |
| Mie 10 | LinkedIn | Caso real | "Como pase de 15€/h a 60€/h en 18 meses" | Comunidad |
| Jue 11 | Instagram | Carrusel | "Checklist: lo que revisar antes de enviar una factura" | Plantilla gratis |
| Vie 12 | Todas | Recurso semana | "Plantilla de propuesta comercial (gratis en Skool)" | Link comunidad |
| Lun 15 | Instagram | Motivacional | "Llevas X meses como autonomo. Aqui lo que has aprendido." | |
| Mar 16 | TikTok | Tutorial | "Como consegui mi primer cliente sin publicidad" | |
| Mie 17 | LinkedIn | Opinion | "El mayor error que veo en los perfiles de LinkedIn de autonomos" | |
| Jue 18 | Instagram | Reel | "La reunion con el cliente que casi me cuesta el proyecto" | |
| Vie 19 | Todas | Highlight semana | Resumen de lo mejor de la comunidad esta semana | Skool |
| Lun 22 | Todas | Lanzamiento | "Ya somos [N] autonomos en la comunidad — gracias" | Invitar a amigos |
| Mar 23 | TikTok | Educativo | "Como calcular tu precio minimo como autonomo (formula)" | |
| Mie 24 | Instagram | Carrusel | "Las mejores herramientas de productividad para autonomos 2026" | |
| Jue 25 | LinkedIn | Reflexion | "6 meses de comunidad: lo que hemos aprendido juntos" | |
| Vie 26 | Todas | Premium highlight | "Esto es lo que se perdieron los que no son premium este mes" | Upgrade |
| Lun 29 | Todas | Reto julio | "Reto de julio: [objetivo mensual]" | Unirse para participar |

## Notas de produccion
- Todos los posts de Instagram con subtitulos en el video
- LinkedIn: sin links en el post (poner en primer comentario)
- TikTok: gancho en los primeros 2 segundos o se va
- Ratio 4:5 para feed Instagram, 9:16 para Stories y Reels
"""
    (_out / "redes" / "calendario_junio.md").write_text(calendario, encoding="utf-8")
    print("[OK] Estrategia, bios y calendario generados")

# ── Resumen final ─────────────────────────────────────────────────────
separador("RESUMEN — Todo listo")
output = PROJECT_ROOT / "output" / "skool"
archivos = [f for f in output.rglob("*") if f.is_file()]
for f in sorted(archivos):
    print(f"  {str(f.relative_to(output.parent.parent))} ({f.stat().st_size:,}b)")
print(f"\nTotal: {len(archivos)} archivos generados en output/skool/")

# Actualiza panel
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("generar_panel", PROJECT_ROOT / "scripts" / "generar_panel.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); mod.generar()
except Exception as e:
    print(f"[panel] {e}")

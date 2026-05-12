"""Construye 3 landings adicionales de las propuestas de Scout."""
from __future__ import annotations
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT_ROOT / "output"


LANDINGS = {
    "seniordigital": {
        "titulo": "SeniorDigital",
        "tagline": "Aprende tecnología a tu ritmo, en español y sin complicaciones",
        "color1": "#2d6a4f",
        "color2": "#52b788",
        "naranja": "#f77f00",
        "publico": "Personas mayores de 55 años",
        "problemas": [
            ("📱", "El móvil y el ordenador dan miedo", "Cada actualización es un misterio. Nadie explica las cosas con calma y sin tecnicismos."),
            ("🎣", "Miedo a estafas online", "Phishing, virus, fraudes... sin saber qué es seguro y qué no, mejor no tocar nada."),
            ("👨‍👩‍👧", "Depender siempre de los hijos", "Tener que llamar a alguien cada vez que algo no funciona es frustrante y agotador."),
        ],
        "categorias": [
            ("📱 Móvil y WhatsApp", ["Videollamadas con familia", "Fotos y álbumes digitales", "Grupos y mensajes seguros"]),
            ("💻 Ordenador básico", ["Navegar sin miedo", "Correo electrónico fácil", "Documentos y fotos"]),
            ("🛡️ Seguridad online", ["Identificar estafas", "Contraseñas seguras", "Compras online seguras"]),
        ],
        "testimonios": [
            ("Con 68 años aprendí a hacer videollamadas con mis nietos. Ahora los veo todos los días.", "Carmen R., jubilada, Sevilla"),
            ("Por fin entiendo mi móvil. Las explicaciones son claras, sin prisas.", "Manolo G., 72 años, Barcelona"),
            ("Mi hijo ya no tiene que venir cada semana a arreglarme el ordenador.", "Pilar M., 65 años, Madrid"),
        ],
        "cta": "Empieza gratis esta semana",
        "monetizacion": "Cursos online desde 15€ · Suscripción mensual 9€/mes",
        "precios": [
            ("Gratis", "0€", ["Acceso a 5 lecciones básicas", "Comunidad de apoyo", "Newsletter semanal"], False),
            ("Mensual", "9€/mes", ["Todo el contenido", "Nuevos cursos cada mes", "Soporte por email", "Sin permanencia"], True),
            ("Anual", "79€/año", ["Todo lo del mensual", "Ahorra 29€ al año", "Sesión grupal mensual", "Acceso anticipado"], False),
        ],
        "faq": [
            ("¿Necesito saber mucho de tecnología para empezar?", "Para nada. Todo está explicado desde cero, con paciencia y sin tecnicismos. Si sabes encender el móvil, puedes empezar."),
            ("¿En qué formato son las lecciones?", "Videos cortos de 5-10 minutos, con texto explicativo y ejercicios prácticos. A tu ritmo, sin presión."),
            ("¿Qué pasa si tengo dudas?", "Puedes escribirnos por email o preguntar en la comunidad. Respondemos en menos de 24 horas."),
            ("¿Puedo cancelar cuando quiera?", "Sí, sin preguntas ni penalizaciones. Cancelas desde tu perfil en menos de 1 minuto."),
        ],
    },
    "traduceweb": {
        "titulo": "TraduceWeb",
        "tagline": "Traducciones profesionales para negocios españoles con entrega en 24h",
        "color1": "#1e40af",
        "color2": "#3b82f6",
        "naranja": "#f59e0b",
        "publico": "PYMEs y autónomos que necesitan traducir documentos",
        "problemas": [
            ("⏳", "Las agencias tardan días", "Necesitas el contrato traducido para mañana y te dicen que en 5 días hábiles."),
            ("💸", "Precios desorbitados", "Las grandes agencias cobran por palabra y el presupuesto final siempre dobla el inicial."),
            ("🤷", "Calidad inconsistente", "Google Translate no vale para documentos legales. Un error de traducción puede costar una venta."),
        ],
        "categorias": [
            ("📄 Documentos legales", ["Contratos", "Estatutos y escrituras", "Documentación notarial"]),
            ("🌐 Web y marketing", ["Páginas web", "Catálogos y folletos", "Redes sociales"]),
            ("📧 Comunicación", ["Emails de negocio", "Propuestas comerciales", "Atención al cliente"]),
        ],
        "testimonios": [
            ("Necesitaba un contrato traducido al inglés urgente. En 6 horas lo tenía perfecto.", "Roberto L., exportador, Valencia"),
            ("Tradujeron nuestra web completa al inglés y alemán. Calidad impecable.", "Ana C., e-commerce, Madrid"),
            ("Por fin un servicio que entiende el sector legal. Sin tecnicismos mal traducidos.", "Javier P., abogado, Bilbao"),
        ],
        "cta": "Pide presupuesto gratis en 5 minutos",
        "monetizacion": "Por proyecto · Desde 0,08€/palabra · Urgente disponible",
        "precios": [
            ("Básico", "0,08€/palabra", ["Entrega en 48h", "1 idioma", "Documentos estándar"], False),
            ("Profesional", "0,12€/palabra", ["Entrega en 24h", "Revisión incluida", "Documentos legales y técnicos"], True),
            ("Urgente", "0,18€/palabra", ["Entrega en 6h", "Revisor nativo", "Cualquier tipo de documento"], False),
        ],
        "faq": [
            ("¿Cómo funciona el proceso?", "Subes tu documento, recibes presupuesto gratuito en 15 minutos y confirmas. Nosotros asignamos al traductor especializado en tu sector."),
            ("¿Los traductores son nativos?", "Sí. Todos nuestros traductores son nativos en el idioma de destino y especializados en áreas concretas (legal, técnico, marketing)."),
            ("¿Qué idiomas ofrecéis?", "Inglés, francés, alemán, italiano, portugués y chino. Más idiomas bajo consulta."),
            ("¿Hacéis traducciones juradas?", "Sí, disponemos de traductores jurados para documentos que requieren validez legal oficial."),
        ],
    },
    "contenidopro": {
        "titulo": "ContenidoPro",
        "tagline": "Suscríbete y recibe recursos de marketing digital que realmente funcionan",
        "color1": "#7c3aed",
        "color2": "#a78bfa",
        "naranja": "#f4821f",
        "publico": "Autónomos y pequeñas empresas que hacen su propio marketing",
        "problemas": [
            ("🌊", "Demasiado contenido, poca claridad", "Hay miles de blogs de marketing pero el 90% son genéricos, en inglés o desactualizados."),
            ("🎯", "Lo que funciona en EEUU no funciona aquí", "Las estrategias americanas rara vez encajan con el mercado español y latinoamericano."),
            ("⏰", "Sin tiempo para aprender", "Llevas el negocio solo. No puedes estar horas buscando qué funciona y qué no."),
        ],
        "categorias": [
            ("📱 Redes sociales", ["Plantillas de posts", "Calendarios editoriales", "Scripts para Reels"]),
            ("📧 Email marketing", ["Secuencias de bienvenida", "Newsletters que venden", "Asuntos con alta apertura"]),
            ("🔍 SEO básico", ["Palabras clave para tu nicho", "Fichas de Google My Business", "Contenido que posiciona"]),
        ],
        "testimonios": [
            ("Cada semana recibo exactamente lo que necesito. Sin ruido, sin rollo.", "María S., fisioterapeuta, Granada"),
            ("El calendar editorial me ahorró 3 horas semanales de planificación.", "Carlos M., fotógrafo freelance, Zaragoza"),
            ("Por fin recursos en español adaptados a negocios pequeños de verdad.", "Laura P., tienda online, Pamplona"),
        ],
        "cta": "Primer mes gratis — sin tarjeta",
        "monetizacion": "Newsletter premium 7€/mes · Recursos descargables",
        "precios": [
            ("Free", "0€", ["Newsletter semanal", "1 plantilla al mes", "Acceso comunidad"], False),
            ("Pro", "7€/mes", ["Todo cada semana", "Plantillas ilimitadas", "Calendarios editoriales", "Sin permanencia"], True),
            ("Equipo", "19€/mes", ["Todo lo Pro", "Hasta 3 usuarios", "Recursos exclusivos", "Soporte prioritario"], False),
        ],
        "faq": [
            ("¿Con qué frecuencia llega la newsletter?", "Cada martes recibes un email con la herramienta o estrategia de la semana, testada y lista para aplicar."),
            ("¿Es solo para España o también para Latam?", "Para todo el mercado hispanohablante. Los ejemplos y casos son de España, México, Argentina y Colombia."),
            ("¿Puedo cancelar en cualquier momento?", "Sí, desde tu perfil sin necesidad de contactarnos. Sin preguntas ni períodos de espera."),
            ("¿Qué diferencia hay con otros boletines de marketing?", "Nosotros solo enviamos lo que funciona en negocios pequeños hispanohablantes. Sin teoría, sin casos de Fortune 500."),
        ],
    },
}


def _landing_html(k: str, d: dict) -> str:
    c1, c2, naranja = d["color1"], d["color2"], d["naranja"]

    problemas_html = "".join(f"""
      <div class="card">
        <div class="icon">{e}</div>
        <h3>{t}</h3>
        <p>{desc}</p>
      </div>""" for e, t, desc in d["problemas"])

    # Sección precios
    precios_html = ""
    for nombre_p, precio, items, destacado in d.get("precios", []):
        borde = f"border: 2px solid {naranja}; transform: scale(1.03);" if destacado else "border: 1px solid #e5e7eb;"
        badge = f'<div style="background:{naranja};color:#fff;font-size:0.72rem;font-weight:700;padding:0.2rem 0.7rem;border-radius:4px;text-align:center;margin-bottom:0.8rem">MÁS POPULAR</div>' if destacado else ""
        items_html = "".join(f"<li>{i}</li>" for i in items)
        precios_html += f"""
      <div style="background:#fff;border-radius:12px;padding:1.8rem;{borde}text-align:center;flex:1;min-width:220px">
        {badge}
        <div style="font-size:1rem;font-weight:700;color:{c1};margin-bottom:0.4rem">{nombre_p}</div>
        <div style="font-size:2rem;font-weight:800;color:{naranja};margin-bottom:1rem">{precio}</div>
        <ul style="list-style:none;text-align:left;margin-bottom:1.5rem">
          {"".join(f'<li style="padding:0.3rem 0;font-size:0.9rem;color:#4b5563;border-bottom:1px solid #f3f4f6">✓ {i}</li>' for i in items)}
        </ul>
        <a href="#newsletter" style="display:block;background:{naranja if destacado else c1};color:#fff;padding:0.7rem;border-radius:6px;text-decoration:none;font-weight:700;font-size:0.9rem">Empezar</a>
      </div>"""

    # FAQ
    faq_html = ""
    for preg, resp in d.get("faq", []):
        faq_html += f"""
      <details style="border:1px solid #e5e7eb;border-radius:8px;padding:1rem 1.2rem;background:#fff">
        <summary style="font-weight:600;cursor:pointer;color:{c1};font-size:0.97rem">{preg}</summary>
        <p style="margin-top:0.7rem;color:#4b5563;font-size:0.93rem;line-height:1.6">{resp}</p>
      </details>"""

    cats_html = "".join(f"""
      <div class="cat-card">
        <h3>{nombre}</h3>
        <ul>{"".join(f"<li>{item}</li>" for item in items)}</ul>
      </div>""" for nombre, items in d["categorias"])

    tests_html = "".join(f"""
      <div class="testimonial">
        <p>"{texto}"</p>
        <strong>— {autor}</strong>
      </div>""" for texto, autor in d["testimonios"])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d["titulo"]} — {d["tagline"]}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          color: #1f2937; line-height: 1.6; }}
  nav {{ background: {c1}; padding: 0 1.5rem; height: 60px; display: flex;
         align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }}
  .logo {{ color: #fff; font-size: 1.3rem; font-weight: 800; }}
  .logo span {{ color: {naranja}; }}
  nav a {{ color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.9rem; margin-left: 1.5rem; }}
  .hero {{ background: linear-gradient(135deg, {c1} 0%, {c2} 100%); color: #fff;
           padding: 5rem 1.5rem 4rem; text-align: center; }}
  .hero h1 {{ font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 800; margin-bottom: 1rem; }}
  .hero h1 em {{ color: {naranja}; font-style: normal; }}
  .hero p {{ font-size: 1.1rem; color: rgba(255,255,255,0.85); max-width: 560px;
             margin: 0 auto 2rem; }}
  .btn {{ display: inline-block; background: {naranja}; color: #fff; padding: 0.85rem 2rem;
          border-radius: 6px; font-weight: 700; text-decoration: none; font-size: 1rem;
          border: none; cursor: pointer; }}
  .btn:hover {{ opacity: 0.9; }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  section {{ padding: 4rem 1.5rem; }}
  .bg-light {{ background: #f7f9fc; }}
  .bg-dark {{ background: {c1}; color: #fff; }}
  h2 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 0.4rem; }}
  .sub {{ color: #6b7280; margin-bottom: 2.5rem; font-size: 1rem; }}
  .bg-dark .sub {{ color: rgba(255,255,255,0.7); }}
  .bg-dark h2 {{ color: #fff; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px,1fr)); gap: 1.2rem; }}
  .card {{ background: #fff; border-radius: 10px; padding: 1.6rem;
           box-shadow: 0 2px 10px rgba(0,0,0,0.07); }}
  .card .icon {{ font-size: 2rem; margin-bottom: 0.7rem; }}
  .card h3 {{ font-size: 1rem; font-weight: 700; color: {c1}; margin-bottom: 0.5rem; }}
  .card p {{ color: #6b7280; font-size: 0.93rem; }}
  .cat-card {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
              border-radius: 10px; padding: 1.5rem; }}
  .cat-card h3 {{ color: {naranja}; font-size: 1rem; margin-bottom: 0.8rem; }}
  .cat-card ul {{ list-style: none; }}
  .cat-card li {{ color: rgba(255,255,255,0.85); padding: 0.3rem 0; font-size: 0.92rem; }}
  .cat-card li::before {{ content: "→ "; color: {naranja}; }}
  .testimonial {{ background: #fff; border-left: 4px solid {naranja};
                  border-radius: 0 8px 8px 0; padding: 1.4rem 1.6rem;
                  box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
  .testimonial p {{ font-style: italic; color: #374151; margin-bottom: 0.7rem; font-size: 0.95rem; }}
  .testimonial strong {{ color: {c1}; font-size: 0.88rem; }}
  .newsletter {{ background: {naranja}; color: #fff; text-align: center; }}
  .newsletter h2 {{ color: #fff; }}
  .newsletter .sub {{ color: rgba(255,255,255,0.9); }}
  .form-row {{ display: flex; gap: 0.8rem; max-width: 460px; margin: 0 auto; flex-wrap: wrap;
               justify-content: center; }}
  .form-row input {{ flex: 1; min-width: 200px; padding: 0.85rem 1rem; border: none;
                     border-radius: 6px; font-size: 1rem; }}
  .btn-dark {{ background: {c1}; }}
  .note {{ margin-top: 0.8rem; font-size: 0.8rem; color: rgba(255,255,255,0.75); }}
  footer {{ background: {c1}; color: rgba(255,255,255,0.6); text-align: center;
            padding: 1.5rem; font-size: 0.83rem; }}
  footer a {{ color: rgba(255,255,255,0.5); text-decoration: none; margin: 0 0.5rem; }}
</style>
</head>
<body>
<nav>
  <div class="logo">{d["titulo"].replace(d["titulo"][-2:], f'<span>{d["titulo"][-2:]}</span>')}</div>
  <div><a href="#como">Cómo funciona</a><a href="#newsletter">Empezar gratis</a></div>
</nav>

<section class="hero">
  <div class="container">
    <h1>{d["tagline"].split(",")[0]},<br><em>{", ".join(d["tagline"].split(",")[1:]).strip() if "," in d["tagline"] else d["tagline"]}</em></h1>
    <p>Para {d["publico"].lower()}. Sin complicaciones. En español.</p>
    <a href="#newsletter" class="btn">{d["cta"]}</a>
  </div>
</section>

<section class="bg-light">
  <div class="container">
    <h2>¿Te identificas con esto?</h2>
    <p class="sub">Los problemas que resolvemos cada día.</p>
    <div class="grid-3">{problemas_html}</div>
  </div>
</section>

<section class="bg-dark" id="como">
  <div class="container">
    <h2>Lo que encontrarás</h2>
    <p class="sub">Todo lo que necesitas, organizado y listo para usar.</p>
    <div class="grid-3">{cats_html}</div>
  </div>
</section>

<section class="bg-light">
  <div class="container">
    <h2>Lo que dicen nuestros usuarios</h2>
    <p class="sub">Personas reales, resultados reales.</p>
    <div class="grid-3">{tests_html}</div>
  </div>
</section>

<section style="padding:4rem 1.5rem;background:#fff">
  <div class="container">
    <h2 style="color:{c1};text-align:center;margin-bottom:0.5rem">Precios claros, sin sorpresas</h2>
    <p style="text-align:center;color:#6b7280;margin-bottom:2.5rem">Empieza gratis. Actualiza cuando quieras.</p>
    <div style="display:flex;gap:1.2rem;flex-wrap:wrap;justify-content:center;align-items:flex-start">
      {precios_html}
    </div>
  </div>
</section>

<section style="padding:4rem 1.5rem;background:#f7f9fc">
  <div class="container">
    <h2 style="color:{c1};margin-bottom:2rem">Preguntas frecuentes</h2>
    <div style="display:flex;flex-direction:column;gap:0.8rem;max-width:720px">
      {faq_html}
    </div>
  </div>
</section>

<section class="newsletter" id="newsletter">
  <div class="container">
    <h2>{d["cta"]}</h2>
    <p class="sub">{d["monetizacion"]}</p>
    <form class="form-row" onsubmit="sub(event)">
      <input type="email" placeholder="tu@email.com" required id="em"
             oninvalid="this.setCustomValidity('Introduce un email válido')"
             oninput="this.setCustomValidity('')">
      <button type="submit" class="btn btn-dark">Quiero entrar</button>
    </form>
    <p class="note">Sin spam. Baja cuando quieras.</p>
  </div>
</section>

<footer>
  <a href="#">Aviso legal</a><a href="#">Privacidad</a><a href="#">Contacto</a><br><br>
  © 2025 {d["titulo"]}
</footer>

<script>
function sub(e) {{
  e.preventDefault();
  var email = document.getElementById('em').value;
  var b = e.target.querySelector('button');
  if (!email) return;
  b.textContent = 'Apuntado!';
  b.disabled = true;
  b.style.background = '#10b981';
  e.target.querySelector('input').disabled = true;
}}
</script>
</body>
</html>"""


def main() -> None:
    for key, datos in LANDINGS.items():
        out = OUTPUT / key / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        html = _landing_html(key, datos)
        out.write_text(html, encoding="utf-8")
        print(f"[OK] {key}/index.html ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

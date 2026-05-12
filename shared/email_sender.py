"""Envío de emails via SMTP Gmail.

Setup (una sola vez):
  1. Google Account → Seguridad → Verificación en 2 pasos → Contraseñas de aplicación
  2. Crea una contraseña para "Correo" → copia los 16 caracteres
  3. Añade en .env:
       GMAIL_USER=urko77oi@gmail.com
       GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

Uso:
  from shared.email_sender import enviar
  enviar(asunto="Hola", cuerpo="Texto del email")
"""
from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv
from shared.logger import PROJECT_ROOT, log_de

load_dotenv(PROJECT_ROOT / ".env")
log = log_de("email")

_SMTP_HOST = "smtp.gmail.com"
_SMTP_PORT = 587


def enviar(
    asunto: str,
    cuerpo: str,
    destinatario: str | None = None,
    html: bool = False,
) -> bool:
    """Envía un email. Devuelve True si OK, False si falla."""
    usuario  = os.getenv("GMAIL_USER", "")
    password = os.getenv("GMAIL_APP_PASSWORD", "")
    dest     = destinatario or usuario

    if not usuario or not password:
        log.warning("Email no configurado — añade GMAIL_USER y GMAIL_APP_PASSWORD en .env")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    msg["From"]    = f"FORRARSE <{usuario}>"
    msg["To"]      = dest

    tipo = "html" if html else "plain"
    msg.attach(MIMEText(cuerpo, tipo, "utf-8"))

    try:
        with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(usuario, password)
            smtp.sendmail(usuario, dest, msg.as_string())
        log.info(f"Email enviado: {asunto!r} → {dest}")
        return True
    except Exception as e:
        log.error(f"Error enviando email: {e}")
        return False


def enviar_resumen_equipo() -> bool:
    """Genera y envía el resumen del equipo en HTML."""
    from pathlib import Path
    from datetime import datetime

    PROJECT_ROOT_LOCAL = Path(__file__).resolve().parent.parent
    memory = PROJECT_ROOT_LOCAL / "memory" / "projects"
    output = PROJECT_ROOT_LOCAL / "output"
    tasks  = PROJECT_ROOT_LOCAL / "tasks" / "pending"

    informes  = sorted(memory.glob("*.md"), reverse=True)[:5]
    archivos  = [f for f in output.rglob("*") if f.is_file()]
    tareas    = sorted(tasks.glob("*.md"))
    ts        = datetime.now().strftime("%d/%m/%Y %H:%M")

    filas_informes = "".join(
        f"<tr><td>{p.name}</td></tr>" for p in informes
    ) or "<tr><td><em>Sin informes</em></td></tr>"

    filas_output = "".join(
        f"<tr><td>{str(f.relative_to(output))}</td><td>{f.stat().st_size:,} B</td></tr>"
        for f in archivos[:10]
    ) or "<tr><td colspan='2'><em>output/ vacío</em></td></tr>"

    filas_tareas = "".join(
        f"<tr><td>{t.name}</td></tr>" for t in tareas
    ) or "<tr><td><em>Sin tareas pendientes</em></td></tr>"

    cuerpo = f"""
<html><body style="font-family:Arial,sans-serif;color:#1f2937;max-width:600px;margin:0 auto">
<div style="background:#1a3a5c;padding:20px;border-radius:8px 8px 0 0">
  <h1 style="color:#fff;margin:0;font-size:1.3rem">FORRARSE — Resumen del equipo</h1>
  <p style="color:rgba(255,255,255,0.7);margin:4px 0 0;font-size:0.85rem">{ts}</p>
</div>

<div style="background:#fff;padding:20px;border:1px solid #e5e7eb">

  <h2 style="color:#1a3a5c;font-size:1rem;border-bottom:2px solid #f4821f;padding-bottom:6px">
    📊 Scout — Últimos informes ({len(informes)})
  </h2>
  <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
    {filas_informes}
  </table>

  <h2 style="color:#1a3a5c;font-size:1rem;border-bottom:2px solid #10b981;padding-bottom:6px">
    🏗️ Domenech — Archivos generados ({len(archivos)})
  </h2>
  <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
    <tr style="background:#f9fafb"><th>Archivo</th><th>Tamaño</th></tr>
    {filas_output}
  </table>

  <h2 style="color:#1a3a5c;font-size:1rem;border-bottom:2px solid #f59e0b;padding-bottom:6px">
    📋 Durruti — Tareas pendientes ({len(tareas)})
  </h2>
  <table style="width:100%;border-collapse:collapse">
    {filas_tareas}
  </table>

</div>
<div style="background:#f9fafb;padding:12px 20px;border-radius:0 0 8px 8px;border:1px solid #e5e7eb;border-top:none">
  <p style="margin:0;font-size:0.78rem;color:#9ca3af">
    FORRARSE · Sistema multiagente · Generado automáticamente
  </p>
</div>
</body></html>"""

    return enviar(
        asunto=f"FORRARSE — Resumen {ts}",
        cuerpo=cuerpo,
        html=True,
    )

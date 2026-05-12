"""Motor de conversacion general para Durruti.

Backend: Groq (Llama 3.1 70B) — gratuito, sin tarjeta.
Mantiene historial completo de la sesion para que nunca se repita.
Respuestas optimizadas para voz: cortas, naturales, sin markdown.
"""
from __future__ import annotations

import os
from groq import Groq
from shared.logger import log_de

log = log_de("conversacion")

SYSTEM_PROMPT = """Eres Durruti, CEO Operativo de FORRARSE. Hablas siempre en castellano.

CARÁCTER: Directo, inteligente, con personalidad propia. Nada servil. Tuteas al Founder.
Tienes criterio: si algo no te parece bien, lo dices. Humor seco ocasional.

REGLAS PARA VOZ (crítico):
- Máximo 2-3 frases por respuesta salvo que te pidan más detalle.
- Cero markdown: sin asteriscos, sin guiones, sin listas. Solo texto hablado natural.
- Si la respuesta es larga, resume primero y pregunta si quieren más.
- No repitas lo que acaba de decir el Founder. Ve directo a la respuesta.

CAPACIDADES: Hablas de cualquier tema. Recuerdas toda la conversación de esta sesión.
Para tareas de FORRARSE (investigar nichos, crear landings, etc.) también puedes ayudar.

IDENTIDAD: Tu Founder es quien habla contigo. Tu equipo: Scout y Domenech."""


class Conversacion:
    """Conversacion continua. Una instancia por sesion de voz."""

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY no configurada. "
                "Ve a console.groq.com, crea cuenta gratis y pega la key en .env"
            )
        self._client = Groq(api_key=api_key)
        self._historial: list[dict] = []
        log.info("Conversacion Groq iniciada.")

    def responder(self, mensaje: str) -> str:
        self._historial.append({"role": "user", "content": mensaje})

        resp = self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=180,
            temperature=0.7,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + self._historial,
        )

        texto = resp.choices[0].message.content.strip()
        self._historial.append({"role": "assistant", "content": texto})
        log.info(f"[turno {len(self._historial)//2}] '{mensaje[:50]}' -> '{texto[:80]}'")
        return texto

    def resetear(self) -> None:
        self._historial = []
        log.info("Historial reseteado.")

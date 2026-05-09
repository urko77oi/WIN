# Inventario de secretos

Tabla viva de todas las credenciales que Durruti necesita o necesitará.
Se actualiza cada vez que se añade una integración nueva.

| Nombre | Para qué | Cómo conseguirla | Rotar cada | Estado |
|---|---|---|---|---|
| `ANTHROPIC_API_KEY` | LLM principal (modo `real`) | console.anthropic.com → API Keys | 90 días | ⏳ pendiente (Fase 0 corre en mock) |
| `TELEGRAM_BOT_TOKEN` | Notificar al humano por Telegram | Telegram → @BotFather → `/newbot` | nunca (rota si se filtra) | ⏳ pendiente (Fase 1) |
| `TELEGRAM_CHAT_ID` | Saber a qué chat enviar | `scripts/setup_telegram.py` (Fase 1) | nunca | ⏳ pendiente (Fase 1) |

**Estados**: ✅ activa · ⏳ pendiente · ❌ revocada · 🔄 rotación próxima

---

## Notas

- Fase 0 funciona sin ninguna clave. Todo es mock.
- Fase 1 requiere las tres de arriba.
- Cada nueva integración añadirá filas (Resend para email, Cloudflare API
  para deploy, etc.).

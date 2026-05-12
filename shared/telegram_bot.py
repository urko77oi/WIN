"""Bot de Telegram — canal principal de comunicación con Durruti.

Funcionalidades:
  - Mensajes de texto → Durruti → respuesta en texto + voz (ElevenLabs)
  - Mensajes de voz → STT (Google) → Durruti → respuesta en texto + voz
  - /voz → selector de voces de ElevenLabs con botones
  - /start → bienvenida
  - Botones de aprobación (✅ ❌ 💬) para acciones que Durruti pide confirmar

Arquitectura:
  Durruti es síncrono; el bot es async. Se usa run_in_executor para no bloquear
  el event loop del bot, y run_coroutine_threadsafe para que Durruti pueda enviar
  mensajes al canal desde hilos secundarios.

Quien lo arranca: scripts/start_telegram.py
"""
from __future__ import annotations

import asyncio
import io
import os
import threading
import uuid
from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from shared.logger import log_de

if TYPE_CHECKING:
    from agents.durruti import Durruti

log = log_de("telegram_bot")

# Estado global del bot (se rellena en _post_init)
_app: Application | None = None
_loop: asyncio.AbstractEventLoop | None = None
_durruti: "Durruti | None" = None

# Aprobaciones pendientes: id → (threading.Event, dict con resultado)
_pending_approvals: dict[str, tuple[threading.Event, dict]] = {}


# ─────────────────────────────────────────────────────────────────────
# Helpers para llamar desde código síncrono (Durruti / TelegramChannel)
# ─────────────────────────────────────────────────────────────────────

def enviar_texto_sync(texto: str, chat_id: int | None = None) -> None:
    """Envía un mensaje de texto desde código síncrono."""
    if _app is None or _loop is None:
        return
    cid = chat_id or _chat_id_por_defecto()
    for chunk in _trocear(texto, 4000):
        future = asyncio.run_coroutine_threadsafe(
            _app.bot.send_message(chat_id=cid, text=chunk, parse_mode="Markdown"),
            _loop,
        )
        future.result(timeout=30)


def solicitar_aprobacion_sync(
    *,
    accion: str,
    motivos: list[str],
    coste_estimado_eur: float = 0.0,
    contexto: str = "",
    chat_id: int | None = None,
) -> tuple[bool, str]:
    """Envía botones de aprobación y bloquea hasta que el Founder responda."""
    if _app is None or _loop is None:
        return False, "Bot no iniciado"

    approval_id = str(uuid.uuid4())[:8]
    event = threading.Event()
    resultado: dict = {}
    _pending_approvals[approval_id] = (event, resultado)

    motivos_txt = "\n".join(f"• {m}" for m in motivos) if motivos else "—"
    texto = (
        f"⚠️ *APROBACIÓN REQUERIDA*\n\n"
        f"*Acción:* {accion}\n\n"
        f"*Motivos:*\n{motivos_txt}\n\n"
        f"*Coste estimado:* {coste_estimado_eur:.4f} €"
    )
    if contexto:
        texto += f"\n\n_{contexto}_"

    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar:{approval_id}"),
            InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar:{approval_id}"),
        ],
        [InlineKeyboardButton("💬 Discutir", callback_data=f"discutir:{approval_id}")],
    ])

    cid = chat_id or _chat_id_por_defecto()
    future = asyncio.run_coroutine_threadsafe(
        _app.bot.send_message(
            chat_id=cid, text=texto, reply_markup=teclado, parse_mode="Markdown"
        ),
        _loop,
    )
    future.result(timeout=30)

    # Bloquea hasta respuesta (máximo 24 horas)
    event.wait(timeout=86400)
    _pending_approvals.pop(approval_id, None)
    return resultado.get("aprobada", False), resultado.get("comentario", "")


def _chat_id_por_defecto() -> int:
    cid = os.getenv("TELEGRAM_CHAT_ID")
    if not cid:
        raise RuntimeError("TELEGRAM_CHAT_ID no configurado en .env")
    return int(cid)


def _trocear(texto: str, max_len: int) -> list[str]:
    if len(texto) <= max_len:
        return [texto]
    chunks = []
    while texto:
        chunks.append(texto[:max_len])
        texto = texto[max_len:]
    return chunks


# ─────────────────────────────────────────────────────────────────────
# Handlers del bot
# ─────────────────────────────────────────────────────────────────────

async def _cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    log.info(f"╔══════════════════════════════════╗")
    log.info(f"║  TU CHAT ID ES: {chat_id:<18}║")
    log.info(f"╚══════════════════════════════════╝")

    modo = os.getenv("LLM_MODE", "mock")
    color = "🟡" if modo == "mock" else "🟢"
    await update.message.reply_text(
        f"*Durruti online* {color}\n\n"
        f"Modo LLM: `{modo}`\n\n"
        f"Tu Chat ID: `{chat_id}`\n"
        f"_(Cópialo en el .env como TELEGRAM\\_CHAT\\_ID)_\n\n"
        f"Escríbeme o mándame un audio con tu orden.\n"
        f"Usa /voz para elegir cómo suena mi voz.",
        parse_mode="Markdown",
    )


async def _cmd_voz(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra selector de voces ElevenLabs con botones inline."""
    from shared.tts_service import listar_voces

    await update.message.reply_text("⏳ Cargando voces de ElevenLabs...")

    try:
        voces = listar_voces()
    except RuntimeError as e:
        await update.message.reply_text(f"❌ {e}")
        return
    except Exception as e:
        await update.message.reply_text(f"❌ Error inesperado: {e}")
        return

    if not voces:
        await update.message.reply_text("No hay voces disponibles en tu cuenta.")
        return

    # Máximo 20 voces, 2 por fila
    voces = voces[:20]
    botones = []
    for i in range(0, len(voces), 2):
        fila = []
        for v in voces[i : i + 2]:
            etiqueta = v["nombre"][:22]
            if v.get("genero"):
                etiqueta += f" ({v['genero'][:1].upper()})"
            fila.append(
                InlineKeyboardButton(
                    etiqueta,
                    callback_data=f"voz:{v['id']}:{v['nombre'][:20]}",
                )
            )
        botones.append(fila)

    voz_actual = os.getenv("DURRUTI_VOICE_ID", "—")
    await update.message.reply_text(
        f"🎙️ *Elige la voz de Durruti*\nActual: `{voz_actual}`",
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode="Markdown",
    )


async def _handle_texto(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    orden = (update.message.text or "").strip()
    if not orden:
        return
    await _procesar_orden(update, orden)


async def _handle_voz(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Descarga el audio de Telegram, lo transcribe y lo pasa a Durruti."""
    from shared.stt_service import transcribir_ogg

    msg = await update.message.reply_text("🎤 Transcribiendo tu mensaje de voz...")

    voz_file = await update.message.voice.get_file()
    ogg_bytes = bytes(await voz_file.download_as_bytearray())

    try:
        orden = transcribir_ogg(ogg_bytes)
    except RuntimeError as e:
        await msg.edit_text(f"❌ {e}")
        return
    except Exception as e:
        await msg.edit_text(f"❌ Error en transcripción: {e}")
        return

    if not orden:
        await msg.edit_text("❌ No pude entender el audio. ¿Lo intentas de nuevo?")
        return

    await msg.edit_text(f"📝 *Entendí:* _{orden}_", parse_mode="Markdown")
    await _procesar_orden(update, orden)


async def _handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Procesa pulsaciones de botones inline (aprobaciones y selección de voz)."""
    query = update.callback_query
    await query.answer()
    data = query.data or ""

    # Selección de voz
    if data.startswith("voz:"):
        partes = data.split(":", 2)
        if len(partes) < 3:
            return
        _, voice_id, nombre = partes
        try:
            from shared.tts_service import guardar_voz_en_env
            guardar_voz_en_env(voice_id)
            await query.edit_message_text(
                f"✅ *Voz configurada:* {nombre}\n`{voice_id}`",
                parse_mode="Markdown",
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Error guardando voz: {e}")
        return

    # Aprobaciones
    if ":" in data:
        accion, approval_id = data.split(":", 1)
        entry = _pending_approvals.get(approval_id)
        if not entry:
            await query.edit_message_text("⏱️ Esta solicitud ya expiró o fue respondida.")
            return

        event, resultado = entry
        if accion == "aprobar":
            resultado["aprobada"] = True
            resultado["comentario"] = ""
            await query.edit_message_text("✅ *Aprobado.*", parse_mode="Markdown")
        elif accion == "rechazar":
            resultado["aprobada"] = False
            resultado["comentario"] = "Rechazado por el Founder."
            await query.edit_message_text("❌ *Rechazado.*", parse_mode="Markdown")
        elif accion == "discutir":
            resultado["aprobada"] = False
            resultado["comentario"] = "Founder quiere discutirlo."
            await query.edit_message_text(
                "💬 *Marcado para discutir.* Escríbeme qué quieres cambiar.",
                parse_mode="Markdown",
            )
        event.set()


# ─────────────────────────────────────────────────────────────────────
# Procesamiento central: orden → Durruti → texto + voz
# ─────────────────────────────────────────────────────────────────────

async def _procesar_orden(update: Update, orden: str) -> None:
    loop = asyncio.get_event_loop()
    espera = await update.message.reply_text("⏳ Durruti procesando...")

    try:
        resultado = await loop.run_in_executor(None, lambda: _durruti.procesar(orden))
    except Exception as e:
        log.exception("Error en Durruti.procesar")
        await espera.edit_text(f"❌ Error interno: {e}")
        return

    await espera.delete()

    # La respuesta de texto ya la envió TelegramChannel.notificar() internamente.
    # Ahora enviamos la versión de voz.
    texto_tts = resultado.texto_para_humano
    if len(texto_tts) > 1500:
        # Resumir para TTS: solo el primer bloque significativo
        texto_tts = texto_tts[:1500]

    voice_id = os.getenv("DURRUTI_VOICE_ID")
    try:
        from shared.tts_service import sintetizar
        audio = await loop.run_in_executor(None, lambda: sintetizar(texto_tts, voice_id))
        await update.message.reply_voice(voice=io.BytesIO(audio))
    except RuntimeError as e:
        # ElevenLabs no configurada → silencioso, solo avisa una vez
        log.warning(f"TTS no disponible: {e}")
        await update.message.reply_text(
            f"ℹ️ _Voz no disponible: {e}_", parse_mode="Markdown"
        )
    except Exception as e:
        log.warning(f"TTS falló: {e}")


# ─────────────────────────────────────────────────────────────────────
# Inicialización y arranque
# ─────────────────────────────────────────────────────────────────────

async def _post_init(app: Application) -> None:
    """Se ejecuta justo antes de que el bot empiece a recibir mensajes."""
    global _app, _loop, _durruti

    _app = app
    _loop = asyncio.get_running_loop()

    # Inicializar Durruti con TelegramChannel
    from agents.durruti import Durruti
    from shared.human_channel import TelegramChannel

    _durruti = Durruti(canal=TelegramChannel())
    log.info("Durruti inicializado con canal Telegram.")


def crear_y_arrancar() -> None:
    """Crea la aplicación y arranca el bot (bloquea hasta Ctrl+C)."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN no configurado en .env.\n"
            "Créalo con @BotFather en Telegram y pégalo en .env."
        )

    app = (
        Application.builder()
        .token(token)
        .post_init(_post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", _cmd_start))
    app.add_handler(CommandHandler("voz", _cmd_voz))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_texto))
    app.add_handler(MessageHandler(filters.VOICE, _handle_voz))
    app.add_handler(CallbackQueryHandler(_handle_callback))

    log.info("Bot de Telegram arrancando...")
    app.run_polling(drop_pending_updates=True)

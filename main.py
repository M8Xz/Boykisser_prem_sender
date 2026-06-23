import asyncio
import re
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

TOKEN = "YourToken"  # Токен Вашего бота

CHANNEL_LINK = "https://t.me/xMeowwwly"
SUPPORT_LINK = "https://t.me/xMeowwwly"
DONATE_USERNAME = "@Ficto_Furry"

LANG_FILE = "lang_prefs.json"

# =============================================
# Language persistence
# =============================================

def load_langs() -> dict:
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_langs(data: dict):
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_user_lang(user_id: int) -> str | None:
    return load_langs().get(str(user_id))

def set_user_lang(user_id: int, lang: str):
    data = load_langs()
    data[str(user_id)] = lang
    save_langs(data)

# =============================================
# Translations
# =============================================

TEXTS = {
    "en": {
        "welcome": (
            '<tg-emoji emoji-id="6129432481927010933">⭐️</tg-emoji> <b>Premium Emoji Sender</b>\n\n'
            '<tg-emoji emoji-id="6129909635613726974">⭐️</tg-emoji> Send messages using Telegram Premium emojis.\n'
            '<tg-emoji emoji-id="6129479035077531636">⭐️</tg-emoji> Convert emoji placeholders instantly.\n'
            '<tg-emoji emoji-id="6129932613688764241">⭐️</tg-emoji> Publish directly to any Telegram channel.'
        ),
        "btn_help": "❓ Help",
        "btn_lang": "🌐 Language",
        "btn_donate": "💎 Donate",
        "btn_channel_link": "📢 Channel",
        "unsupported": "⚠️ This message type is not supported!",
        "success": "⚡ Message ready! Just forward it.",
        "error": "❌ Unexpected error: {}",
        "lang_prompt": "🌐 Choose language / Выберите язык:",
        "lang_set": "✅ Language set to English.",
        "help_text": (
            '<tg-emoji emoji-id="6129444065453808638">⭐️</tg-emoji> <b>Help & Guide</b>\n\n'
            "<b>What are Premium Emojis?</b>\n"
            "Animated stickers for Telegram Premium subscribers. This bot lets anyone use them for free!\n\n"
            "<b>How to use placeholders?</b>\n"
            "Wrap any emoji ID with <code>%</code> signs and send it here:\n"
            "<code>%6154335299309672955%</code>\n"
            "The bot instantly converts it into a real Premium emoji.\n\n"
            "<b>How to publish to a channel?</b>\n"
            "1. Send your message here — the bot converts it and sends it back.\n"
            "2. Reply to the converted message with:\n"
            "   <code>/send @YourChannel</code>\n"
            "   or <code>/send -1001234567890</code>\n"
            "3. The bot checks it is an admin in that channel and publishes.\n\n"
            "<b>Requirements for /send</b>\n"
            "• The bot must be added as administrator in the channel.\n"
            "• It must have permission to post messages.\n\n"
            "<b>FAQ</b>\n"
            "• Do I need Telegram Premium? <b>No!</b>\n"
            "• Is it free? <b>Yes, completely free.</b>\n"
            "• Where to get emoji IDs? From the internet or apps like ExteraGram."
        ),
        "send_usage": (
            "ℹ️ <b>Usage:</b> Reply to a converted message with\n"
            "<code>/send @YourChannel</code>\n"
            "or <code>/send -1001234567890</code>"
        ),
        "send_no_reply": "❌ Please <b>reply</b> to the message you want to publish, then use <code>/send @Channel</code>.",
        "send_not_admin": "❌ Bot is not an administrator in <b>{}</b>. Please add it as admin with post permission.",
        "send_no_post_perm": "❌ Bot doesn't have permission to post messages in <b>{}</b>.",
        "send_channel_not_found": "❌ Channel <b>{}</b> not found. Check the username or ID.",
        "send_error": "❌ Failed to publish: {}",
        "send_success": (
            '<tg-emoji emoji-id="6129432481927010933">⭐️</tg-emoji> <b>Published successfully!</b>\n\n'
            "Channel: <b>{}</b>"
        ),
        "btn_view_post": "👁 View Post",
        "donate_text": (
            '<tg-emoji emoji-id="6129705667616841573">⭐️</tg-emoji> <b>Support Development</b>\n\n'
            "Enjoy this bot? Consider supporting the project:\n\n"
            "• Boost our channel\n"
            "• Send a Premium gift to the developer"
        ),
        "btn_boost": "🚀 Boost Channel",
        "btn_gift": "🎁 Send Premium Gift",
    },
    "ru": {
        "welcome": (
            '<tg-emoji emoji-id="6129432481927010933">⭐️</tg-emoji> <b>Отправитель Премиум Эмодзи</b>\n\n'
            '<tg-emoji emoji-id="6129909635613726974">⭐️</tg-emoji> Отправляйте сообщения с Telegram Premium эмодзи.\n'
            '<tg-emoji emoji-id="6129479035077531636">⭐️</tg-emoji> Мгновенно конвертируйте плейсхолдеры эмодзи.\n'
            '<tg-emoji emoji-id="6129932613688764241">⭐️</tg-emoji> Публикуйте в любой Telegram канал.'
        ),
        "btn_help": "❓ Помощь",
        "btn_lang": "🌐 Язык",
        "btn_donate": "💎 Донат",
        "btn_channel_link": "📢 Канал",
        "unsupported": "⚠️ Этот тип сообщения не поддерживается!",
        "success": "⚡ Сообщение готово! Теперь просто перешли его.",
        "error": "❌ Непредвиденная ошибка: {}",
        "lang_prompt": "🌐 Выберите язык / Choose language:",
        "lang_set": "✅ Язык установлен на Русский.",
        "help_text": (
            '<tg-emoji emoji-id="6129444065453808638">⭐️</tg-emoji> <b>Помощь и руководство</b>\n\n'
            "<b>Что такое Premium эмодзи?</b>\n"
            "Анимированные стикеры для подписчиков Telegram Premium. Этот бот позволяет использовать их всем бесплатно!\n\n"
            "<b>Как использовать плейсхолдеры?</b>\n"
            "Оберните ID эмодзи знаками <code>%</code> и отправьте сюда:\n"
            "<code>%6154335299309672955%</code>\n"
            "Бот мгновенно преобразует его в настоящий Premium эмодзи.\n\n"
            "<b>Как публиковать в канал?</b>\n"
            "1. Отправьте сообщение сюда — бот конвертирует и отправит обратно.\n"
            "2. Ответьте на конвертированное сообщение командой:\n"
            "   <code>/send @ВашКанал</code>\n"
            "   или <code>/send -1001234567890</code>\n"
            "3. Бот проверит права администратора и опубликует.\n\n"
            "<b>Требования для /send</b>\n"
            "• Бот должен быть добавлен как администратор канала.\n"
            "• У него должно быть разрешение на публикацию сообщений.\n\n"
            "<b>Частые вопросы</b>\n"
            "• Нужен ли Telegram Premium? <b>Нет!</b>\n"
            "• Это бесплатно? <b>Да, полностью бесплатно.</b>\n"
            "• Где получить ID эмодзи? В интернете или в приложениях типа ExteraGram."
        ),
        "send_usage": (
            "ℹ️ <b>Использование:</b> Ответьте на конвертированное сообщение командой\n"
            "<code>/send @ВашКанал</code>\n"
            "или <code>/send -1001234567890</code>"
        ),
        "send_no_reply": "❌ <b>Ответьте</b> на сообщение которое хотите опубликовать, затем используйте <code>/send @Канал</code>.",
        "send_not_admin": "❌ Бот не является администратором в <b>{}</b>. Добавьте его как администратора с правом публикации.",
        "send_no_post_perm": "❌ У бота нет разрешения на публикацию в <b>{}</b>.",
        "send_channel_not_found": "❌ Канал <b>{}</b> не найден. Проверьте юзернейм или ID.",
        "send_error": "❌ Ошибка публикации: {}",
        "send_success": (
            '<tg-emoji emoji-id="6129432481927010933">⭐️</tg-emoji> <b>Успешно опубликовано!</b>\n\n'
            "Канал: <b>{}</b>"
        ),
        "btn_view_post": "👁 Просмотреть пост",
        "donate_text": (
            '<tg-emoji emoji-id="6129705667616841573">⭐️</tg-emoji> <b>Поддержать разработку</b>\n\n'
            "Нравится бот? Поддержите проект:\n\n"
            "• Забустите наш канал\n"
            "• Подарите Premium разработчику"
        ),
        "btn_boost": "🚀 Забустить канал",
        "btn_gift": "🎁 Подарить Premium",
    },
}

def t(user_id: int, key: str) -> str:
    lang = get_user_lang(user_id) or "en"
    return TEXTS.get(lang, TEXTS["en"]).get(key, TEXTS["en"].get(key, key))

# =============================================
# Core emoji processing
# =============================================

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
EMOJI_PATTERN = re.compile(r"%(\d+)%")

def process_text(text: str) -> str:
    if not text:
        return ""
    return EMOJI_PATTERN.sub(r'<tg-emoji emoji-id="\1">⭐️</tg-emoji>', text)

# =============================================
# Keyboards
# =============================================

def main_menu_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=t(user_id, "btn_help"), callback_data="menu:help"),
        types.InlineKeyboardButton(text=t(user_id, "btn_lang"), callback_data="menu:lang"),
    )
    builder.row(
        types.InlineKeyboardButton(text=t(user_id, "btn_donate"), callback_data="menu:donate"),
        types.InlineKeyboardButton(text=t(user_id, "btn_channel_link"), url=CHANNEL_LINK),
    )
    return builder.as_markup()

def lang_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
    )
    return builder.as_markup()

def donate_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=t(user_id, "btn_boost"), url=CHANNEL_LINK),
        types.InlineKeyboardButton(text=t(user_id, "btn_gift"), url=f"https://t.me/{DONATE_USERNAME.lstrip('@')}"),
    )
    return builder.as_markup()

def view_post_keyboard(user_id: int, post_link: str | None) -> types.InlineKeyboardMarkup | None:
    if not post_link:
        return None
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t(user_id, "btn_view_post"), url=post_link))
    return builder.as_markup()

# =============================================
# /start command
# =============================================

@dp.message(Command("start"))
async def start_command(message: types.Message):
    uid = message.from_user.id
    lang = get_user_lang(uid)

    if lang is None:
        await message.answer(
            "🌐 Choose language / Выберите язык:",
            reply_markup=lang_keyboard(),
        )
        return

    await message.answer(
        text=t(uid, "welcome"),
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(uid),
    )

# =============================================
# /lang command
# =============================================

@dp.message(Command("lang"))
async def lang_command(message: types.Message):
    uid = message.from_user.id
    await message.answer(t(uid, "lang_prompt"), reply_markup=lang_keyboard())

# =============================================
# /help command
# =============================================

@dp.message(Command("help"))
async def help_command(message: types.Message):
    uid = message.from_user.id
    await message.answer(text=t(uid, "help_text"), parse_mode=ParseMode.HTML)

# =============================================
# /send @Channel — stateless, no stored data
# =============================================

@dp.message(Command("send"))
async def send_command(message: types.Message, command: CommandObject):
    uid = message.from_user.id

    channel_arg = (command.args or "").strip()
    if not channel_arg:
        await message.answer(text=t(uid, "send_usage"), parse_mode=ParseMode.HTML)
        return

    ref_msg = message.reply_to_message
    if not ref_msg:
        await message.answer(text=t(uid, "send_no_reply"), parse_mode=ParseMode.HTML)
        return

    # Resolve channel
    try:
        chat = await bot.get_chat(channel_arg)
    except TelegramBadRequest:
        await message.answer(
            text=t(uid, "send_channel_not_found").format(channel_arg),
            parse_mode=ParseMode.HTML,
        )
        return
    except Exception as e:
        await message.answer(
            text=t(uid, "send_error").format(str(e)),
            parse_mode=ParseMode.HTML,
        )
        return

    # Check bot is admin with post permission
    try:
        me = await bot.get_me()
        member = await bot.get_chat_member(chat.id, me.id)
    except Exception:
        await message.answer(
            text=t(uid, "send_not_admin").format(channel_arg),
            parse_mode=ParseMode.HTML,
        )
        return

    if member.status not in ("administrator", "creator"):
        await message.answer(
            text=t(uid, "send_not_admin").format(channel_arg),
            parse_mode=ParseMode.HTML,
        )
        return

    if hasattr(member, "can_post_messages") and member.can_post_messages is False:
        await message.answer(
            text=t(uid, "send_no_post_perm").format(channel_arg),
            parse_mode=ParseMode.HTML,
        )
        return

    # Publish
    try:
        sent = await copy_message_to_channel(chat.id, ref_msg)
        if sent is None:
            await message.answer(text=t(uid, "unsupported"), parse_mode=ParseMode.HTML)
            return

        display = f"@{chat.username}" if chat.username else (chat.title or channel_arg)
        post_link = None
        if chat.username and sent.message_id:
            post_link = f"https://t.me/{chat.username}/{sent.message_id}"

        await message.answer(
            text=t(uid, "send_success").format(display),
            parse_mode=ParseMode.HTML,
            reply_markup=view_post_keyboard(uid, post_link),
        )

    except TelegramForbiddenError:
        await message.answer(
            text=t(uid, "send_not_admin").format(channel_arg),
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await message.answer(
            text=t(uid, "send_error").format(str(e)),
            parse_mode=ParseMode.HTML,
        )

# =============================================
# /donate command
# =============================================

@dp.message(Command("donate"))
async def donate_command(message: types.Message):
    uid = message.from_user.id
    await message.answer(
        text=t(uid, "donate_text"),
        parse_mode=ParseMode.HTML,
        reply_markup=donate_keyboard(uid),
    )

# =============================================
# Publish helper — copies message to channel
# =============================================

async def copy_message_to_channel(chat_id: int, ref: types.Message) -> types.Message | None:
    if ref.photo:
        return await bot.send_photo(
            chat_id=chat_id,
            photo=ref.photo[-1].file_id,
            caption=ref.html_text or ref.caption or "",
            parse_mode=ParseMode.HTML,
        )
    elif ref.video:
        return await bot.send_video(
            chat_id=chat_id,
            video=ref.video.file_id,
            caption=ref.html_text or ref.caption or "",
            parse_mode=ParseMode.HTML,
        )
    elif ref.animation:
        return await bot.send_animation(
            chat_id=chat_id,
            animation=ref.animation.file_id,
            caption=ref.html_text or ref.caption or "",
            parse_mode=ParseMode.HTML,
        )
    elif ref.document:
        return await bot.send_document(
            chat_id=chat_id,
            document=ref.document.file_id,
            caption=ref.html_text or ref.caption or "",
            parse_mode=ParseMode.HTML,
        )
    elif ref.audio:
        return await bot.send_audio(
            chat_id=chat_id,
            audio=ref.audio.file_id,
            caption=ref.html_text or ref.caption or "",
            parse_mode=ParseMode.HTML,
        )
    elif ref.voice:
        return await bot.send_voice(
            chat_id=chat_id,
            voice=ref.voice.file_id,
            caption=ref.html_text or ref.caption or "",
            parse_mode=ParseMode.HTML,
        )
    elif ref.video_note:
        return await bot.send_video_note(
            chat_id=chat_id,
            video_note=ref.video_note.file_id,
        )
    elif ref.text:
        return await bot.send_message(
            chat_id=chat_id,
            text=ref.html_text or ref.text,
            parse_mode=ParseMode.HTML,
        )
    return None

# =============================================
# Callback: language selection
# =============================================

@dp.callback_query(F.data.startswith("lang:"))
async def cb_lang(callback: types.CallbackQuery):
    uid = callback.from_user.id
    chosen = callback.data.split(":")[1]
    set_user_lang(uid, chosen)
    await callback.answer()
    await callback.message.edit_text(
        text=t(uid, "welcome"),
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(uid),
    )

# =============================================
# Callback: main menu buttons
# =============================================

@dp.callback_query(F.data.startswith("menu:"))
async def cb_menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    action = callback.data.split(":")[1]
    await callback.answer()

    if action == "help":
        await callback.message.answer(
            text=t(uid, "help_text"),
            parse_mode=ParseMode.HTML,
        )
    elif action == "lang":
        await callback.message.answer(
            t(uid, "lang_prompt"),
            reply_markup=lang_keyboard(),
        )
    elif action == "donate":
        await callback.message.answer(
            text=t(uid, "donate_text"),
            parse_mode=ParseMode.HTML,
            reply_markup=donate_keyboard(uid),
        )

# =============================================
# Core message handler
# =============================================

@dp.message()
async def handle_content(message: types.Message):
    if message.text and message.text.startswith("/"):
        return

    uid = message.from_user.id

    try:
        source = message.html_text or ""
        final_text = process_text(source)

        params = {
            "chat_id": message.chat.id,
            "caption": final_text,
            "parse_mode": ParseMode.HTML,
        }

        if message.photo:
            await bot.send_photo(photo=message.photo[-1].file_id, **params)
        elif message.video:
            await bot.send_video(video=message.video.file_id, **params)
        elif message.animation:
            await bot.send_animation(animation=message.animation.file_id, **params)
        elif message.document:
            await bot.send_document(document=message.document.file_id, **params)
        elif message.audio:
            await bot.send_audio(audio=message.audio.file_id, **params)
        elif message.voice:
            await bot.send_voice(voice=message.voice.file_id, **params)
        elif message.video_note:
            await bot.send_video_note(
                chat_id=message.chat.id,
                video_note=message.video_note.file_id,
            )
        elif message.text:
            await bot.send_message(
                chat_id=message.chat.id,
                text=final_text,
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(t(uid, "unsupported"))
            return

        await message.answer(t(uid, "success"))

    except Exception as e:
        await message.answer(t(uid, "error").format(e))

# =============================================
# Startup: register bot commands
# =============================================

async def set_commands():
    commands_en = [
        BotCommand(command="start", description="Open main menu"),
        BotCommand(command="help", description="Full guide and examples"),
        BotCommand(command="send", description="Publish converted message — reply + /send @Channel"),
        BotCommand(command="lang", description="Change language"),
        BotCommand(command="donate", description="Support development"),
    ]
    commands_ru = [
        BotCommand(command="start", description="Открыть главное меню"),
        BotCommand(command="help", description="Полное руководство и примеры"),
        BotCommand(command="send", description="Опубликовать — ответьте + /send @Канал"),
        BotCommand(command="lang", description="Изменить язык"),
        BotCommand(command="donate", description="Поддержать разработку"),
    ]
    await bot.set_my_commands(commands_en, scope=BotCommandScopeDefault())
    try:
        await bot.set_my_commands(commands_ru, scope=BotCommandScopeDefault(), language_code="ru")
    except Exception:
        pass

async def main():
    print("Boykisser Premium Emoji Sender is running!")
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

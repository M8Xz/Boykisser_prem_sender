import asyncio
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "YourToken" #Токен Вашего бота

START_TEXT = (
    "%5424672277578920981%<b>Мяв! Я могу тебе сделать сообщение с премиум эмодзи, даже если у тебя нету премки, абсолютно бесплатно!</b>\n\n"
    "%6032937473162614352% Для того что-бы использовать прем эмодзи, тебе нужно вставить в %emoji_id% айдишник эмодзи, его можно узнать в интернете или при зажатии в моде ExteraGram (официальном)\n\n"
    "%5346181118884331907% <b>А ещё я опен-сурсный проект, и мой код открыт на гитхабе!</b>\n"
    "%5271604874419647061% github.com/M8Xz/Boykisser_prem_sender"
) #Тут вы можете сделать своё сообщение при команде /start, это стандартное сообщение при запуске бота
#Поддержка %emoji_id% плейсхолдеров, создание строки \n, форматирование <b>Жырный</b> и <i>Курсив</i>

SUPPORT_LINK = "https://YourLink" #Ссылка по нажатию на кнопку приветсвенного сообщения 
# =============================================

bot = Bot(token=TOKEN)
dp = Dispatcher()
EMOJI_PATTERN = re.compile(r"%(\d+)%")

def process_text(text: str) -> str:
    if not text:
        return ""
    return EMOJI_PATTERN.sub(r'<tg-emoji emoji-id="\1">⭐️</tg-emoji>', text)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    final_start_text = process_text(START_TEXT)
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🎁 Текст кнопки", #Текст кнопки под приветсвтенным сообщением 
        url=SUPPORT_LINK)
    )
    
    await message.answer(
        text=final_start_text,
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup()
    )

@dp.message()
async def handle_content(message: types.Message):
    if message.text and message.text.startswith("/"):
        return

    try:
        source = message.html_text or ""
        final_text = process_text(source)
        
        params = {
            "chat_id": message.chat.id, 
            "caption": final_text, 
            "parse_mode": ParseMode.HTML
        }

        if message.photo:
            await bot.send_photo(photo=message.photo[-1].file_id, **params)
        elif message.video:
            await bot.send_video(video=message.video.file_id, **params)
        elif message.animation:
            await bot.send_animation(animation=message.animation.file_id, **params)
        elif message.document:
            await bot.send_document(document=message.document.file_id, **params)
        elif message.text:
            await bot.send_message(chat_id=message.chat.id, text=final_text, parse_mode=ParseMode.HTML)
        else:
            await message.answer("⚠️ Этот тип сообщения не поддерживается!") #Сообщение о формате который не поддерживаеться (Есть поддержка: фото, файлы, гиф, видео)
            return

        await message.answer("⚡ Сообщение готово! Теперь просто перешли его.") #Сообщение об успехе

    except Exception as e:
        await message.answer(f"❌ Непредвиденная ошибка: {e}") #Сообщение для отлатки

async def main():
    print("Бот Boykisser Prem Sender запущен!") #Сообщение в консоль что бот запущен
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

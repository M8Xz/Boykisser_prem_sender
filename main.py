import asyncio
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode

TOKEN = "token" #Укажите токен Вашего бота
ADMIN_IDS = [] #Укажите айди пользователей которые могут пользоваться ботом
#Вы можете настроить все сообщения ниже под себя, НЕ ТРОГОЙТЕ EMOJI_PATTERN И EMOJI_PATTERN.sub!!!

bot = Bot(token=TOKEN)
dp = Dispatcher()
EMOJI_PATTERN = re.compile(r"%(\d+)%")

def process_text(message: types.Message) -> str:
    source = message.html_text or ""
    if not source:
        return ""
    return EMOJI_PATTERN.sub(r'<tg-emoji emoji-id="\1">⭐️</tg-emoji>', source)

@dp.message(F.from_user.id.in_(ADMIN_IDS))
async def handle_admin_content(message: types.Message):
    try:
        final_text = process_text(message)
        
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
            await message.answer("⚠️ Этот тип сообщения не поддерживается!")
            return

        await message.answer("⚡ Сообщение готово! Теперь просто перешли его.")

    except Exception as e:
        await message.answer(f"❌ Непредвиденная ошибка: {e}")

@dp.message()
async def access_denied(message: types.Message):
    await message.answer("❌ Вас нету в вайт листе!")

async def main():
    print("Бот Boykisser Prem Sender запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

//Это код для Cloudflare воркера!!! Это не будет работать как обычная нода!!!
const TOKEN = "YOUR_TOKEN"; //Токен Вашего бота
const SUPPORT_LINK = "https://YourLink"; //Ссылка по нажатию на кнопку приветсвенного сообщения

const START_TEXT = `%5424672277578920981%<b>Мяв! Я могу тебе сделать сообщение с премиум эмодзи, даже если у тебя нету премки, абсолютно бесплатно!</b>\n
%6032937473162614352% Для того что-бы использовать прем эмодзи, тебе нужно вставить в %emoji_id% айдишник эмодзи, его можно узнать в интернете или при зажатии в моде ExteraGram (официальном)\n
%5346181118884331907% <b>А ещё я опен-сурсный проект, и мой код открыт на гитхабе!</b>
%5271604874419647061% github.com/M8Xz/Boykisser_prem_sender`;
//Тут вы можете сделать своё сообщение при команде /start, это стандартное сообщение при запуске бота
//Поддержка %emoji_id% плейсхолдеров, создание строки \n, форматирование <b>Жырный</b> и <i>Курсив</i>

const API_URL = `https://api.telegram.org/bot${TOKEN}`;

function processText(text) {
    if (!text) return "";
    return text.replace(/%(\d+)%/g, '<tg-emoji emoji-id="$1">⭐️</tg-emoji>');
}

async function sendMessage(chatId, text, replyMarkup = null) {
    const payload = { chat_id: chatId, text: text, parse_mode: "HTML" };
    if (replyMarkup) payload.reply_markup = replyMarkup;
    
    await fetch(`${API_URL}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
}

async function sendMedia(chatId, method, fileId, caption) {
    const payload = { chat_id: chatId, parse_mode: "HTML", caption: caption };
    const mediaField = method.replace("send", "").toLowerCase();
    payload[mediaField] = fileId;

    await fetch(`${API_URL}/${method}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
}

export default {
    async fetch(request) {
        if (request.method !== "POST") return new Response("Бот работает!");

        try {
            const update = await request.json();
            if (!update.message) return new Response("OK");

            const message = update.message;
            const chatId = message.chat.id;
            let text = message.text || message.caption || "";

            if (text.startsWith("/start")) {
                const finalText = processText(START_TEXT);
                const markup = {
                    inline_keyboard: [[{ text: "🎁 Текст кнопки", url: SUPPORT_LINK }]] //Текст кнопки под приветсвтенным сообщением
                };
                await sendMessage(chatId, finalText, markup);
                return new Response("OK");
            }

            const finalText = processText(text);

            if (message.photo) {
                await sendMedia(chatId, "sendPhoto", message.photo[message.photo.length - 1].file_id, finalText);
            } else if (message.video) {
                await sendMedia(chatId, "sendVideo", message.video.file_id, finalText);
            } else if (message.animation) {
                await sendMedia(chatId, "sendAnimation", message.animation.file_id, finalText);
            } else if (message.document) {
                await sendMedia(chatId, "sendDocument", message.document.file_id, finalText);
            } else if (text) {
                await sendMessage(chatId, finalText);
            } else {
                await sendMessage(chatId, "⚠️ Этот тип сообщения не поддерживается!"); //Сообщение о формате который не поддерживаеться (Есть поддержка: фото, файлы, гиф, видео)
                return new Response("OK");
            }

            await sendMessage(chatId, "⚡ Сообщение готово! Теперь просто перешли его."); //Сообщение об успехе

        } catch (error) {
            console.error("❌ Непредвиденная ошибка:", error); //Сообщение для отлатки
        }

        return new Response("OK", { status: 200 });
    }
};
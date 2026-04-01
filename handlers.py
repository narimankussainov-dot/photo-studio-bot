import os
from aiogram import Router, F, Bot
from aiogram.types import Message
from database import add_user
from aiogram.filters import Command
from ai_service import process_audio_with_ai, process_text_with_ai, process_image_with_ai, reset_user_history

router = Router()


# Универсальная функция для записи юзера
def register_user(message: Message):
    add_user(message.from_user.id, message.from_user.username or message.from_user.first_name)


# Команда для сброса контекста (памяти)
@router.message(Command("reset"))
async def cmd_reset(message: Message):
    reset_user_history(message.from_user.id)
    await message.reply("🔄 Ваша история диалога очищена. Можем начать общение с чистого листа!")


# 1. Текст
@router.message(F.text)
async def handle_text(message: Message):
    register_user(message)
    status_msg = await message.reply("⏳ Печатаю ответ...")
    response = await process_text_with_ai(message.from_user.id, message.text, message.from_user.username)
    await status_msg.edit_text(response)


# 2. Аудио
@router.message(F.voice)
async def handle_voice(message: Message, bot: Bot):
    register_user(message)
    status_msg = await message.reply("⏳ Слушаю...")

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = f"temp_voice_{message.from_user.id}.ogg"
    await bot.download_file(file.file_path, file_path)

    response = await process_audio_with_ai(file_path)
    await status_msg.edit_text(response)


# 3. НОВОЕ: Фотографии (Референсы)
@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    register_user(message)
    status_msg = await message.reply("⏳ Рассматриваю фотографию...")

    # Берем самое высокое качество фото (последнее в списке)
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = f"temp_photo_{message.from_user.id}.jpg"
    await bot.download_file(file.file_path, file_path)

    # Получаем подпись к фото, если клиент ее написал
    caption = message.caption or ""

    response = await process_image_with_ai(file_path, caption)
    await status_msg.edit_text(response)
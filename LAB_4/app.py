from aiogram import Bot
from aiogram import Router, Dispatcher
import asyncio
import logging
import os

from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем роутер (вместо диспетчера)
router = Router()


# Команда /start
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Я помогу тебе подобрать сеанс в кинотеатр. \nНапиши /help если что-то пойдет не так."
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="yes")],
            [InlineKeyboardButton(text="Нет", callback_data="no")],
            [InlineKeyboardButton(text="🔗 Сайт", url="https://example.com")]
        ]
    )

    await message.answer(
        "Выберите кинотеатр:",
        reply_markup=keyboard
    )


# Команда /help
@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📋 <b>Доступные команды:</b>\n"
        "/start - Запуск бота\n"
        "/help - Помощь\n"
        "/menu - Показать меню\n\n"
        "Просто напиши мне что-нибудь!"
    )


# Команда /menu
@router.message(Command("menu"))
async def menu_handler(message: Message):
    # Создаем простую клавиатуру
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")],
            [KeyboardButton(text="Помощь"), KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=kb)


# Запуск бота
async def main():
    # Создаем бота
    bot = Bot(
        token=BOT_TOKEN
    )

    # Создаем диспетчер и подключаем роутер
    dp = Dispatcher()
    dp.include_router(router)

    # Устанавливаем команды в меню
    await bot.set_my_commands([
        {"command": "start", "description": "Запустить бота"},
        {"command": "help", "description": "Помощь"},
        {"command": "menu", "description": "Показать меню"},
    ])

    print("✅ Бот запущен!")

    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

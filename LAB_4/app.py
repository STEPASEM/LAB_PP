from aiogram import Bot
from aiogram import Router, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import asyncio
import logging
import os

from parser import Parser

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем роутер
router = Router()

# Глобальные переменные для хранения фильмов
movies_cache = []

def create_movies_keyboard(movies_list, page=0, items_per_page=5):
    """Создает клавиатуру с кнопками фильмов"""
    builder = InlineKeyboardBuilder()

    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    current_movies = movies_list[start_idx:end_idx]

    for i, movie in enumerate(current_movies, start=start_idx + 1):
        # Обрезаем длинные названия
        title = movie
        if len(title) > 30:
            title = title[:27] + "..."

        button_text = f"{i}. {title}"
        builder.button(text=button_text, callback_data=f"movie_{i - 1}")

    builder.adjust(1)

    total_pages = (len(movies_list) + items_per_page - 1) // items_per_page

    navigation_buttons = []

    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}")
        )

    navigation_buttons.append(
        InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="current_page")
    )

    if page < total_pages - 1:
        navigation_buttons.append(
            InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"page_{page + 1}")
        )

    if navigation_buttons:
        builder.row(*navigation_buttons)

    # Кнопка обновления и закрытия
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
        InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    )

    return builder.as_markup()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Я помогу тебе подобрать сеанс в кинотеатр.\n"
        "Напиши /help если что-то пойдет не так."
    )

    # Загружаем фильмы
    movies = await Parser().parse_film()

    if not movies:
        await message.answer("❌ Не удалось загрузить фильмы. Попробуйте позже.")
        return

    # Сохраняем в кэш
    global movies_cache
    movies_cache = movies

    keyboard = create_movies_keyboard(movies, page=0)

    await message.answer(
        f"<b>🎥 Сейчас в кино (Москва):</b>\n"
        f"Найдено фильмов: {len(movies)}\n"
        f"Выберите фильм для подробной информации:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@router.message(Command("movies"))
async def movies_handler(message: Message):
    """Команда для показа фильмов"""
    movies = await Parser().parse_film()

    if not movies:
        await message.answer("❌ Не удалось загрузить фильмы. Попробуйте позже.")
        return

    # Сохраняем в кэш
    global movies_cache
    movies_cache = movies

    keyboard = create_movies_keyboard(movies, page=0)

    await message.answer(
        f"<b>🎥 Сейчас в кино:</b>\n"
        f"Найдено фильмов: {len(movies)}\n"
        f"Выберите фильм:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📋 <b>Доступные команды:</b>\n"
        "/start - Запуск бота и показ фильмов\n"
        "/movies - Показать фильмы\n"
        "/help - Помощь\n\n"
        "Просто нажмите на кнопку с фильмом для получения информации!"
    )

# Запуск бота
async def main():
    # Создаем бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Создаем диспетчер и подключаем роутер
    dp = Dispatcher()
    dp.include_router(router)

    # Устанавливаем команды в меню
    await bot.set_my_commands([
        {"command": "start", "description": "Запустить бота"},
        {"command": "movies", "description": "Показать фильмы"},
        {"command": "help", "description": "Помощь"},
    ])

    print("✅ Бот запущен!")

    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
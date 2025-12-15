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
movies_cache = {}


def create_movies_keyboard(movies_dict, page=0, items_per_page=5):
    """Создает клавиатуру с кнопками фильмов из словаря"""
    builder = InlineKeyboardBuilder()

    movie_titles = list(movies_dict.keys())

    # Определяем диапазон для текущей страницы
    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    current_movies = movie_titles[start_idx:end_idx]

    for i, title in enumerate(current_movies, start=start_idx + 1):
        # Обрезаем длинные названия
        display_title = title
        if len(display_title) > 30:
            display_title = display_title[:27] + "..."

        button_text = f"{i}. {display_title}"
        builder.button(text=button_text, callback_data=f"movie_{i - 1}")

    builder.adjust(1)

    total_pages = (len(movie_titles) + items_per_page - 1) // items_per_page

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
    movies_dict = await Parser().parse_film()

    if not movies_dict:
        await message.answer("❌ Не удалось загрузить фильмы. Попробуйте позже.")
        return

    # Сохраняем в кэш
    global movies_cache
    movies_cache = movies_dict

    # Создаем клавиатуру
    keyboard = create_movies_keyboard(movies_dict, page=0)

    await message.answer(
        f"<b>🎥 Сейчас в кино (Москва):</b>\n"
        f"Найдено фильмов: {len(movies_dict)}\n"
        f"Выберите фильм для подробной информации:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@router.message(Command("movies"))
async def movies_handler(message: Message):
    """Команда для показа фильмов"""
    movies_dict = await Parser().parse_film()

    if not movies_dict:
        await message.answer("❌ Не удалось загрузить фильмы. Попробуйте позже.")
        return

    # Сохраняем в кэш
    global movies_cache
    movies_cache = movies_dict

    keyboard = create_movies_keyboard(movies_dict, page=0)

    await message.answer(
        f"<b>🎥 Сейчас в кино:</b>\n"
        f"Найдено фильмов: {len(movies_dict)}\n"
        f"Выберите фильм:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("movie_"))
async def movie_detail_handler(callback: CallbackQuery):
    """Показывает детали фильма и ссылку"""
    movie_idx = int(callback.data.split("_")[1])

    global movies_cache

    # Получаем список названий из словаря
    movie_titles = list(movies_cache.keys())

    if movie_idx >= len(movie_titles):
        await callback.answer("Фильм не найден", show_alert=True)
        return

    # Получаем название и ссылку
    movie_title = movie_titles[movie_idx]
    movie_link = movies_cache[movie_title][0]
    movie_info = movies_cache[movie_title][1]
    movie_genres = movies_cache[movie_title][2]
    movie_time_location = movies_cache[movie_title][3]

    # Создаем клавиатуру для возврата
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад к списку", callback_data="back_to_list"),
                InlineKeyboardButton(text="🌐 Купить билет", url=movie_link)
            ]
        ]
    )

    await callback.message.edit_text(
        f"<b>🎬 {movie_title}</b>\n\n"
        f"<b>Жанры:</b> {movie_genres}\n"
        f"<b>Время и место:</b> {movie_time_location}\n\n"
        f"<b>Описание:</b> {movie_info}\n\n"
        f"<i>Нажмите кнопку ниже чтобы открыть страницу с расписанием сеансов.</i>",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(F.data.startswith("page_"))
async def page_handler(callback: CallbackQuery):
    """Обрабатывает переключение страниц"""
    page = int(callback.data.split("_")[1])

    global movies_cache

    if not movies_cache:
        await callback.answer("Нет данных о фильмах", show_alert=True)
        return

    keyboard = create_movies_keyboard(movies_cache, page=page)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "refresh")
async def refresh_handler(callback: CallbackQuery):
    """Обновляет список фильмов"""
    await callback.answer("Обновляю список...")

    movies_dict = await Parser().parse_film()

    if not movies_dict:
        await callback.message.edit_text("❌ Не удалось загрузить фильмы.")
        return

    # Обновляем кэш
    global movies_cache
    movies_cache = movies_dict

    keyboard = create_movies_keyboard(movies_dict, page=0)

    await callback.message.edit_text(
        f"<b>🎥 Обновленный список фильмов:</b>\n"
        f"Найдено фильмов: {len(movies_dict)}\n"
        f"Выберите фильм:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "back_to_list")
async def back_handler(callback: CallbackQuery):
    """Возвращает к списку фильмов"""
    global movies_cache

    if not movies_cache:
        await callback.message.edit_text("❌ Нет данных о фильмах.")
        return

    keyboard = create_movies_keyboard(movies_cache, page=0)

    await callback.message.edit_text(
        f"<b>🎥 Сейчас в кино:</b>\n"
        f"Найдено фильмов: {len(movies_cache)}\n"
        f"Выберите фильм:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "close")
async def close_handler(callback: CallbackQuery):
    """Закрывает меню"""
    await callback.message.delete()
    await callback.answer("Меню закрыто")


@router.callback_query(F.data == "current_page")
async def current_page_handler(callback: CallbackQuery):
    """Обработчик для кнопки текущей страницы"""
    await callback.answer(f"Текущая страница", show_alert=False)


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📋 <b>Доступные команды:</b>\n"
        "/start - Запуск бота и показ фильмов\n"
        "/movies - Показать фильмы\n"
        "/help - Помощь\n\n"
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
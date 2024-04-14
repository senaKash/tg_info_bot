import asyncio

import sys
from os import getenv

from aiogram.client.session.aiohttp import AiohttpSession

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import FSInputFile
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from excel_manager import ExcelManager
import re

from aiogram.filters import Command
from aiogram.filters import Command, CommandObject, CommandStart
from commands import set_default_commands

dp = Dispatcher()
file_name = "IT_LETI_DATA.xlsx"


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    excel_manager = ExcelManager(file_name)
    excel_manager.create_or_update_workbook(message.from_user.id, strip_html_tags(hbold(message.from_user.full_name)))
    await message.answer(f"Привет, {hbold(message.from_user.full_name)} ты успешно зарегестрирован!(id: {message.from_user.id}) \nТелега ввела ограничение 1 тык \ 30 сек", reply_markup=build_keyboard().as_markup(resize_keyboard=True))
    print(f"{message.from_user.full_name} нажал start")



@dp.callback_query(F.data == "zapisi_lekcii")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    excel_manager = ExcelManager(file_name)
    urls = excel_manager.lektsionnie_url()
    msg = "Лекции\n"
    print(f"{callback.from_user.full_name} посмотрел список лекций")
    #ids = excel_manager.get_all_ids()
    #print(ids)
    #for user_id in ids:
    #    await callback.bot.send_message(user_id, "Лекция загружена(Дз кста тоже посмотрите)")
    #await callback.bot.send_message(541020016, "Хуй")
    await callback.message.answer(f"{msg}{urls}", reply_markup=build_keyboard().as_markup(resize_keyboard=True))


@dp.callback_query(F.data == "homework")
async def send_homework(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    msg = "Дз\n"

    print(f"{callback.from_user.full_name} посмотрел дз")
    await callback.message.answer(f"{msg}Повторить то, что я написал на практике(p.s. кому сильно лень - кину в начале след пары, но это -rep)", reply_markup=build_keyboard().as_markup(resize_keyboard=True))

@dp.callback_query(F.data == "timetable")
async def send_homework(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    dates = ["07.04;18:00", "14.04;18:00"]
    formatted_message = format_schedule(dates)

    print(f"{callback.from_user.full_name} посмотрел расписание")
    msg = "Расписание\n"
    await callback.message.answer(f"{msg}{formatted_message}", reply_markup=build_keyboard().as_markup(resize_keyboard=True))

@dp.callback_query(F.data == "files")
async def send_materials(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    print(f"{callback.from_user.full_name} посмотрел материалы")
    msg = "Материалы\n"
    await callback.message.answer(f"{msg}Сюда залью презентации, книжки и т.д.", reply_markup=build_keyboard().as_markup(resize_keyboard=True))

@dp.callback_query(F.data == "mark")
async def update_poseshuaemost(callback: types.CallbackQuery):  #время устанавливается вручную
    excel_manager = ExcelManager(file_name)
    mark = excel_manager.check_and_update_attendance(callback.from_user.id)
    print("mark = ", mark)
    if mark == 2:
        await callback.answer(
        text="Уже отметился",
        show_alert=True
        )
    elif mark == 1:
        await callback.answer(
        text="Отметился",
        show_alert=True
        )
    elif mark == 0:
        await callback.answer(
        text="ошибка id или exel",
        show_alert=True
        )
    elif mark == 3:
        await callback.answer(
        text="Отмечатся можно только во время пары",
        show_alert=True
        )


@dp.message(Command('addlectureurl'))#commands=['addLectureUrl'])
async def add_lecture_url(message: types.Message, command: CommandObject) -> None:
    if message.from_user.id == 541020016:
        command_text = command.args
        if not command_text:
            await message.answer("Пожалуйста, укажите ссылку после команды.")
            return

        link = command_text.strip()  # Удаляем лишние пробелы по краям
        excel_manager = ExcelManager(file_name)
        excel_manager.lektsionnie_url(link)
        await message.answer(f"Вы добавили ссылку: {link}")

        excel_manager = ExcelManager(file_name)
        ids = excel_manager.get_all_ids()
        print("link")
        for user_id in ids:
            await callback.bot.send_message(user_id, "Лекция загружена")

    else:
        await message.answer("У вас нет прав для выполнения этой команды.")


@dp.message(Command('spam'))#commands=['addLectureUrl'])
async def add_lecture_url(message: types.Message, command: CommandObject) -> None:
    if message.from_user.id == 541020016:
        command_text = command.args
        if not command_text:
            await message.answer("Добавьте текст сообщения")
            return
        msg = command_text.strip()
        excel_manager = ExcelManager(file_name)
        urls = excel_manager.lektsionnie_url()
        #msg = "Лекции\n"
        ids = excel_manager.get_all_ids()
        print(ids, msg)
        #user_id = 541020016
        #await message.bot.send_message(user_id, msg)
        for user_id in ids:
            await message.bot.send_message(user_id, msg)
        #link = command_text.strip()  # Удаляем лишние пробелы по краям
        #excel_manager = ExcelManager(file_name)
        #excel_manager.lektsionnie_url(link)
        #await message.answer(f"Вы добавили ссылку: {link}")
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.message()
async def handle_message(message: types.Message) -> None:
    if message.text == '1':
        photo_path = "12.jpg"
        await message.answer_photo(FSInputFile(photo_path))



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    #session = AiohttpSession(proxy='http://proxy.server:3128')
    #bot = Bot('', session=session)
    bot = Bot('', parse_mode=ParseMode.HTML)
    await set_default_commands(bot)
    #dp = Dispatcher(bot) ???
    # And the run events dispatching
    await dp.start_polling(bot)


def strip_html_tags(text):
    """Функция для удаления HTML тегов из строки."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def format_schedule(dates):
    # Находим максимальную длину даты и времени
    max_date_length = max(len(date_time.split(";")[0]) for date_time in dates)
    max_time_length = max(len(date_time.split(";")[1]) for date_time in dates)

    # Заголовок таблицы
    header = "Дата".ljust(max_date_length + 4)
    time_row = "Время".ljust(max_time_length + 2)
    for date_time in dates:
        date, time = date_time.split(";")
        header += date.ljust(max_date_length + 2)
        time_row += time.ljust(max_time_length + 2)

    # Разделитель
    separator = "-" * (len(header) + 10)
    # Формируем сообщение
    message = header + "\n" + separator + "\n"+ time_row
    return message

def build_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Лекции", callback_data="zapisi_lekcii"),
        types.InlineKeyboardButton(text="Дз", callback_data="homework")
    )
    builder.row(
        types.InlineKeyboardButton(text="Расписание", callback_data="timetable"),

    )
    builder.row(
        types.InlineKeyboardButton(text="Всякое полезное", callback_data="files"),
        types.InlineKeyboardButton(text="Я на паре", callback_data="mark")
    )
    #builder.as_markup(resize_keyboard=True)
    return builder



if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
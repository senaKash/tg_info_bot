import asyncio

import sys
from os import getenv

#from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import FSInputFile
#from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from excel_manager import ExcelManager
import re



dp = Dispatcher()
file_name = "IT_LETI_DATA.xlsx"  


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    
    
    #await message.answer(f"Привет, {hbold(message.from_user.full_name)}!"
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
    
    excel_manager = ExcelManager(file_name)
    #excel_manager.create_or_update_workbook(1, "sadasd")
    excel_manager.create_or_update_workbook(message.from_user.id, strip_html_tags(hbold(message.from_user.full_name)))
    await message.answer(f"Привет, {hbold(message.from_user.full_name)} ты успешно зарегестрирован!(id: {message.from_user.id}) \nТелега ввела ограничение 1 тык \ 30 сек", reply_markup=builder.as_markup(resize_keyboard=True))



@dp.callback_query(F.data == "zapisi_lekcii")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("/записывается/")


@dp.callback_query(F.data == "homework")
async def send_homework(callback: types.CallbackQuery):
    await callback.message.answer("чилл")

@dp.callback_query(F.data == "timetable")
async def send_homework(callback: types.CallbackQuery):
    dates = ["07.04;18:00", "14.04;18:00"]
    formatted_message = format_schedule(dates)
    await callback.message.answer(f"{formatted_message}")

@dp.callback_query(F.data == "files")
async def send_materials(callback: types.CallbackQuery):
    await callback.message.answer("Сюда залью презентации, книжки и т.д.")

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
        #callback.answer("Уже отметился") 
    elif mark == 1:
        await callback.answer(
        text="Отметился",
        show_alert=True
        )
        #callback.answer("Отметился")      
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
        #callback.answer("ошибка id или exel")  
    '''
    now = datetime.now()
    async with state.proxy() as data:
        if "button_clicked" not in data:
            if now.weekday() == 6 and 15 <= now.hour < 19 and now.minute >= 0:
                await callback.answer("Кнопка активирована")
                data["button_clicked"] = True
            else:
                await callback.answer("Сейчас нет пары")
        else:
            if now.weekday() == 6 and (now.hour == 19 and now.minute >= 29) or now.hour >= 20:
                await callback.answer("Кнопка деактивирована")
                del data["button_clicked"]
            else:
                await callback.answer("Кнопка уже была активирована ранее")
    '''
#callback_data=""
'''
    kb = [
            [
                types.KeyboardButton(text="лекции"),
                types.KeyboardButton(text="Дз"),
                types.KeyboardButton(text="Расписание"),
                types.KeyboardButton(text="Всякое полезное"),
                types.KeyboardButton(text="Я на паре")
            ],
        ]
    keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Пикай что нужно и погнали"
        )
'''


'''
@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

@dp.callback_query(F.data == "zapisi_lekcii")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("112345678")
'''


@dp.message()
async def handle_message(message: types.Message) -> None:
    if message.text == '1':
        photo_path = "12.jpg"
        await message.answer_photo(FSInputFile(photo_path))

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot('', parse_mode=ParseMode.HTML)
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



if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
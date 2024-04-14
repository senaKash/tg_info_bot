from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import types



async def set_default_commands(bot):
    await bot.set_my_commands([
        types.BotCommand(command='help', description='Помощь'),
        types.BotCommand(command='addlectureurl', description='Загрузить лекцию'),
        types.BotCommand(command='spam', description='Отправить всем сообщение'),
    ], BotCommandScopeDefault())
'''
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='addlectureurl',
            description='льём'
        ),

        BotCommand(
            command='sadasdasd',
            description='льём'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
'''
# tg_info_bot
бот чтобы складировать информацию по курсу asp.net

Для запуска на хотинге:

1)pip install aiohttp-socks
2)from aiogram.client.session.aiohttp import AiohttpSession
3)session = AiohttpSession(proxy='http://proxy.server:3128')  #прокси в настройках хостинга смотрите
4)bot = Bot(token='...', session=session)


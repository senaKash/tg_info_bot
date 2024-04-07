# tg_info_bot
бот чтобы складировать информацию по курсу asp.net

Для запуска на хотинге:

1)pip install aiohttp-socks
2)from aiogram.client.session.aiohttp import AiohttpSession
3)session = AiohttpSession(proxy='http://proxy.server:3128')  #прокси в настройках хостинга смотрите
4)bot = Bot(token='...', session=session)


![image](https://github.com/senaKash/tg_info_bot/assets/62939178/cb6d553e-a5c8-4af2-9b6e-5b0f9788b851)

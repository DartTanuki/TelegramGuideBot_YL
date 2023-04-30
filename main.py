"""
TODO: YANDEX LUCEYM PROJECT: TELEGRAM BOT
TODO: Author: Saprikin Nikita
TODO: version: 1.0
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor

from bot.data.config import BOT_TOKEN
from bot.handlers.user_handlers import register_user_handlers_main

from create_bot import bot, dp


def register_handlers(dp: Dispatcher) -> None:
    register_user_handlers_main(dp=dp)


register_handlers(dp=dp)
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    try:
        executor.start_polling(dp)
    except Exception as _ex:
        print('Exception -', _ex)

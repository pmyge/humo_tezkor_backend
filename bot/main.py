"""Main bot file"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, language, orders

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register routers
dp.include_router(start.router)
dp.include_router(language.router)
dp.include_router(orders.router)


async def main():
    """Main function to start the bot"""
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

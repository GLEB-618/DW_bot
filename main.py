import asyncio
from bot import bot

if __name__ == "__main__":
    print("Запуск бота")
    asyncio.run(bot.run_bot())
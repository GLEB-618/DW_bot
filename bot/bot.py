import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.utils.chat_action import ChatActionMiddleware
from shared import settings
from bot.handlers import setup_all_routers


# # Всплывающий список команд бота
# async def set_commands(bot: Bot):
#     commands = [
#         types.BotCommand(command="talk", description="/talk <текст> | Нейро АбAIв ответит")
#     ]
#     await bot.set_my_commands(commands)


async def keep_alive(bot: Bot):
    while True:
        try:
            await bot.get_me()
            print("[keep_alive] Telegram жив")
        except Exception as e:
            print(f"[keep_alive] Ошибка: {e}")
        await asyncio.sleep(300)  # каждые 5 минут

# Запуск бота
async def run_bot():
    router = Router()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher() 

    setup_all_routers(router)
    dp.include_router(router)

    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    # await set_commands(bot)
    asyncio.create_task(keep_alive(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())
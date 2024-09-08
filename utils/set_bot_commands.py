from aiogram import types
from aiogram.types import BotCommandScopeDefault


async def set_default_commands(dp):
    await dp.bot.delete_my_commands(scope=BotCommandScopeDefault())
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Launch the bot"),
        ]
    )

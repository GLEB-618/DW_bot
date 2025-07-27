from aiogram import Router, F, flags
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.chat_type import ChatType
from aiogram.enums.chat_action import ChatAction

import tempfile

from downloader import download_audio, search_tracks, fetch_thumbnail
from shared import is_url, create_inline_keyboard, async_tempdir

track_links = {}  # глобально или внутри FSM контекста

def setup(r: Router):
    r.message.register(search, F.text)
    r.callback_query.register(download, F.data.startswith("track_"))


async def search(msg: Message):
    assert msg.text is not None
    query = msg.text.strip()
    results = search_tracks(query)

    if not results:
        await msg.answer("Ничего не найдено :(")
        return

    buttons = []
    for idx, track in enumerate(results):
        track_links[str(idx)] = track # сохраняем ссылку
        buttons.append([(f"{track['artist']} – {track['title']}", f"track_{idx}")])

    keyboard = create_inline_keyboard(buttons)
    await msg.answer("Выбери трек:", reply_markup=keyboard)

async def download(callback: CallbackQuery):
    assert callback.data and callback.message is not None
    msg = await callback.message.answer("Скачиваю...")
    if callback.data.startswith("track_"):
        idx = callback.data.split("_")[1]
        track = track_links.get(idx)
        if track:
            url = track['url']
            title = track['title']
            artist = track['artist']

            if not url:
                await callback.message.answer("Ошибка: ссылка не найдена")
                return
            
            async with async_tempdir() as tmpdir:
                query = f"{artist} - {title}"
                path = await download_audio(query, tmpdir)
                thumb = await fetch_thumbnail(track["cover"])
                if path:
                    await msg.delete()
                    await callback.message.answer_audio(audio=FSInputFile(path), title=title, performer=artist, thumbnail=thumb)
                else:
                    await callback.message.answer("Ошибка: путя нет")
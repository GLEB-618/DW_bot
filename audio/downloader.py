import asyncio
import aiohttp
from yt_dlp import YoutubeDL
from aiogram.types import BufferedInputFile


async def download_audio(query: str, tmpdir: str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'writethumbnail': True,       
            'embedthumbnail': True,        
            'addmetadata': True, 
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',
                },
                {
                    'key': 'FFmpegMetadata',
                },
            ],
        }

        def _run_dl():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)

                assert info is not None

                if info.get("_type") == "playlist":
                    info = info["entries"][0]

                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'

                return filename
            
        return await asyncio.to_thread(_run_dl)
    except Exception as e:
        print(f"Ошибка: {e}")
    
async def fetch_thumbnail(url: str) -> BufferedInputFile:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            return BufferedInputFile(data, filename="thumb.jpg")
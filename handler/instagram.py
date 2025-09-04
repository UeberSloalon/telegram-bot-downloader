from aiogram import Router, F
from aiogram.types import Message
from urllib.parse import urlparse
import instaloader

router = Router()

L = instaloader.Instaloader(
    download_videos=True,
    save_metadata=False,
    download_pictures=False,
    download_comments=False,
    post_metadata_txt_pattern=""
)

def extract_shortcode(url: str) -> str | None:

    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 2 and parts[0] in ("reel", "p", "tv"):  # reel / p / tv
        return parts[1]
    return None


@router.message(F.text.contains("instagram.com"))
async def handle_instagram(message: Message):
    shortcode = extract_shortcode(message.text)
    if not shortcode:
        await message.answer("Не удалось распознать ссылку")
        return

    status_message = await message.answer("Идет скачивание")

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            await message.answer_video(post.video_url, caption="Скачано в @")
        else:
            await message.answer("Это не видео")
    except Exception as e:
        await message.answer(f"Ошибка при загрузке: {e}")

    finally:
        await status_message.delete()

import asyncio
from aiogram import Router, F, types
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultVideo
from urllib.parse import urlparse
import instaloader
import uuid

router = Router()

L = instaloader.Instaloader(
    download_videos=True,
    save_metadata=False,
    download_pictures=False,
    download_comments=False,
    post_metadata_txt_pattern=""
)

def extract_shortcode(url: str) -> str | None:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    valid_types = ("reel", "reels", "p", "tv")  # 👈 добавил reels

    if len(parts) >= 2 and parts[0] in valid_types:
        return parts[1].split("?")[0]
    return None




@router.message(F.text)
async def handle_instagram(message: Message):
    text = message.text.strip()

    if "instagram.com" not in text:
        return

    shortcode = extract_shortcode(text)
    if not shortcode:
        await message.answer("Не удалось распознать ссылку")
        return

    status_message = await message.answer("Скачиваю Instagram видео...")

    try:
        post = await asyncio.to_thread(instaloader.Post.from_shortcode, L.context, shortcode)

        if post.is_video:
            await message.answer_video(post.video_url, caption="Скачано в @")
        else:
            await message.answer(" Это не видео")
    except Exception as e:
        await message.answer(f"Ошибка при загрузке: {e}")
    finally:
        await status_message.delete()

@router.inline_query()
async def instagram_inline(query: InlineQuery):
    text = query.query.strip()

    if not text or "instagram.com" not in text:
        return

    try:
        shortcode = extract_shortcode(text)
        if not shortcode:
            raise Exception("Не удалось распознать ссылку")

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if not post.is_video:
            raise Exception("Это не видео")

        video_url = post.video_url

        result = InlineQueryResultVideo(
            id=str(uuid.uuid4()),
            video_url=video_url,
            mime_type="video/mp4",
            thumbnail_url="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
            title="Видео с Instagram",
            caption="Скачано в @uebersloalon_bot"
        )

        await query.answer([result], cache_time=0)

    except Exception as e:
        error_result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Ошибка",
            input_message_content=InputTextMessageContent(
                message_text=f"Не удалось скачать видео: {e}"
            )
        )
        await query.answer([error_result], cache_time=0)
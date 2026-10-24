import io
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8673596837:AAE99JE1fWV7XyBVDl8HZQXGNc3GjfSq9SI"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def create_text_sticker(text: str, size=(512, 512), font_size=70):
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (size[0] - text_w) / 2
    y = (size[1] - text_h) / 2

    # Gölge efekti
    shadow_offset = 4
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 200))
    # Ana altın/gold rengi
    draw.text((x, y), text, font=font, fill=(255, 215, 0, 255))

    output = io.BytesIO()
    image.save(output, format="WEBP")
    output.seek(0)
    return output.getvalue()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Yazı stiker botuna hoş geldin!\nKullanım: `/yaz Metniniz`", parse_mode="Markdown")

@dp.message(Command("yaz"))
async def make_sticker(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Lütfen bir metin girin. Örnek: `/yaz Aysha`")
        return

    text = args[1]
    sticker_bytes = create_text_sticker(text, size=(512, 512))
    file = BufferedInputFile(sticker_bytes, filename="sticker.webp")
    await message.answer_sticker(sticker=file)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

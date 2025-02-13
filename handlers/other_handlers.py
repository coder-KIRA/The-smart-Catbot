from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU, CAT_PHRASES, CAT_FACTS
import aiohttp
import random

# Инициализируем роутер уровня модуля
router = Router()

API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'

def get_random_cat_phrase():
    return random.choice(CAT_FACTS)

# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_CATS_URL) as response:
                if response.status == 200:
                    cat_data = await response.json()
                    cat_url = cat_data[0]['url']
                    cat_phrase = get_random_cat_phrase()
                    await message.answer_photo(cat_url, caption=cat_phrase, parse_mode="HTML")
                else:
                    await message.answer(text=LEXICON_RU['ERROR_TEXT'])
    except Exception as e:
        await message.answer(text=LEXICON_RU['ERROR_TEXT'])
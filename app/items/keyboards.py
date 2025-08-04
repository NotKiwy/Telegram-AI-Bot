from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()
supp = os.getenv("SUPPORT")
comm = os.getenv("COMM")

wkb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="_prof")
        ],
        [
            InlineKeyboardButton(text="🛠️ Поддержка", url=supp),
            InlineKeyboardButton(text="🤝 Комьюнити", url=comm)
        ]
    ]
)

prkb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💸 Пополнить баланс", callback_data="_add_bal")
        ]
    ]
)


from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from dotenv import load_dotenv
from aiosend import CryptoPay

from api import openrouter
from items.texts import *
from database.creator import __db__

import items.keyboards as kb
import database.utils as dbu

import asyncio
import os


load_dotenv()

token = os.getenv("TOKEN")
PROMPT = os.getenv("PROMPT")
cpt = os.getenv("CRYPTOBOT")

bot = Bot(
    token=token,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()
cp = CryptoPay(cpt)

class Request(StatesGroup):
    prompt = State()

class CryptoBot(StatesGroup):
    cns = State()

@dp.message(Command('start'))
async def _cmd_start_(m: types.Message):
    uid = m.from_user.id

    await dbu._reg_(uid)
    await m.reply(wtext.format(
        FN=m.from_user.first_name
    ), reply_markup=kb.wkb)

@dp.callback_query(F.data == "_prof")
async def _call_prof_(call: CallbackQuery):
    uid = call.from_user.id

    data = await dbu._get_info_(uid)

    if data:
        coins, admin = data
        await call.message.reply(proftext.format(
            UID=uid,
            STAT="Админ" if admin == 1 else "Пользователь",
            COINS=coins
        ), reply_markup=kb.prkb)

@dp.callback_query(F.data == "_add_bal")
async def _call_add_bal_(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id

    await call.message.reply(addb)
    await state.set_state(CryptoBot.cns)

@dp.message(CryptoBot.cns)
async def _payment_(msg: types.Message, state: FSMContext):
    try:
        amount = int(msg.text)
        tdata = await state.get_data()
        uid = msg.from_user.id

        await state.update_data(
            cns=amount,
            uid=uid,
            cid=msg.chat.id,
            invid=None
        )

        invoice = await cp.create_invoice(amount * 0.05, "USDT")
        await state.update_data(invid=invoice.invoice_id)

        paykb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💳 Оплатить", url=invoice.bot_invoice_url)
                ],
                [
                    InlineKeyboardButton(text="💸 Проверить оплату", callback_data="_check")
                ]
            ]
        )

        await msg.reply(payment.format(
            TCOINS=amount,
            REQ=amount * 0.05
        ), reply_markup=paykb)

        invoice.poll(message=msg)

    except ValueError:
        await msg.reply("err")


@dp.callback_query(F.data == "_check")
async def _check_payment_(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    try:
        invoice = await cp.get_invoice(data['invid'])

        if invoice.status == 'paid':
            amount = data['cns']
            uid = data['uid']

            await dbu._add_coins_(amount, uid)
            await call.message.edit_text(
                succpayment.format(
                    INV=invoice.invoice_id,
                    COINS=amount
                ), reply_markup=None)

            await state.clear()
        else:
            await call.message.reply(nopayment)
    except Exception as e:
        await call.message.reply(errwhchck)
        print(e)

@dp.message()
async def _send_request_(msg: types.Message):
    uid = msg.from_user.id
    prompt = msg.text
    data = await dbu._get_info_(uid)

    if data:
        coins, admin = data
        if coins >= 1:
            await dbu._remove_coins_(1, uid)
            bmsg = await msg.reply(que)
            ans = await openrouter._request(prompt, system_prompt=PROMPT)
            await bmsg.edit_text(ans)
        else:
            await msg.reply(nocoins)

async def setup():
    await asyncio.gather(
        __db__(),
        dp.start_polling(bot),
        cp.start_polling()
    )
if __name__ == "__main__":
    try:
        asyncio.run(setup())
    except  KeyboardInterrupt:
        print("Stopped.")
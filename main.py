import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
import keyboard as kb
from dropmail import Dropmail, EMail

import json
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def texthandler(m: types.Message):
    if m.text != 'استلام البريد':
        await m.answer(f'مرحبا, {m.from_user.mention}\nتم تصميم هذا الروبوت لتلقي رسائل  البريد المؤقت بسرعة. انقر فوق الزر أدناه', reply_markup=kb.menu)
    elif m.text == 'استلام البريد':
        mail = Dropmail("randomtoken")
        mail.NewSession()

        email = mail.Address
        await m.answer(f'➕ ها هو بريدك الإلكتروني: {email}\nارسل رسالة. فحص البريد تلقائيًا ، كل 4 ثوانٍ ، إذا وصلت رسالة جديدة ، فسوف نخطرك')
        while True:
            mails = mail.GetEmails()
            if isinstance(mails, list):
                for x in mails:

                    return await m.answer(f"From: {x.From}\nTo: {x.To}\n\nSubject: {x.Subject}\nText: {x.Text}")
                    # break
                    # await m.answer(f'💬 رسالة جديدة:\n<b>من عند</b>: {fromm}\n<b>موضوع</b>: {theme}\n<b>رسالة</b>: {mes}', reply_markup=kb.menu, parse_mode='HTML')
 
            else:
                pass
            await asyncio.sleep(4)
 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

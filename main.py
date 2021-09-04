import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
import keyboard as kb
from onesec_api import Mailbox
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
        ma = Mailbox('')
        email = f'{ma._mailbox_}@1secmail.com'
        await m.answer(f'➕ ها هو بريدك الإلكتروني: {email}\nارسل رسالة.\nيتم فحص البريد تلقائيًا ، كل 4 ثوانٍ ، إذا وصلت رسالة جديدة ، فسوف نخطرك!\nملاحظة: يمكنك تلقي فقط رسالة واحدة - لكل بريد إلكتروني  ')
        while True:
            mb = ma.filtred_mail()
            if isinstance(mb, list):
                mf = ma.mailjobs('read',mb[0])
                js = mf.json()
                fromm = js['from']
                theme = js['subject']
                mes = js['textBody']
                await m.answer(f'💬 رسالة جديدة:\n<b>من عند</b>: {fromm}\n<b>موضوع</b>: {theme}\n<b>رسالة</b>: {mes}', reply_markup=kb.menu, parse_mode='HTML')
                break
            else:
                pass
            await asyncio.sleep(4)
 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

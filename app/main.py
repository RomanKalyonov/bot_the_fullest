import logging
import ssl
from aiogram.utils.executor import start_webhook

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import telegram
import random
import telebot
import flask

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1141021151:AAEdcx1odj9l0TiDxhC5WgwekX5-LLsWkS8'

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class LetsPlay(StatesGroup):
    FirstForm = State()

async def irr_verbs_training():
  irr_verbs={1:["to be","was/were","been"],
           2:["to beat","beat","beaten"],
           3:["to become","became","become"],
           4:["to begin","began","begun"],
           5:["to bend","bent","bent"],
           6:["to bet","bet","bet"],
           7:["to bite","bit","bitten"],
           8:["to blow","blew","blown"],
           9:["to break","broke","broken"],
           10:["to bring","brought","brought"],
           11:["to build","built","built"],
           12:["to burn","burnt","burnt"],
           13:["to burst","burst","burst"],
           14:["to buy","bought","bought"],
           15:["to catch","caught","caught"],
           16:["to choose","chose","chosen"],
           17:["to come","came","come"],
           18:["to cost","cost","cost"],
           19:["to cut","cut","cut"],
           20:["to deal","dealt","dealt"],
           21:["to dig","dug","dug"],
           22:["to do","did","done"],
           23:["to draw","drew","drawn"],
           24:["to dream","dreamt","dreamt"],
           25:["to drink","drank","drunk"],
           26:["to drive","drove","driven"],
           27:["to eat","ate","eaten"],
           28:["to fall","fell","fallen"],
           29:["to feed","fed","fed"],
           30:["to feel","felt","felt"],
           31:["to fight","fought","fought"],
           32:["to find","found","found"],
           33:["to fly","flew","flown"],
           34:["to forget","forgot","forgotten"],
           35:["to forgive","forgave","forgiven"],
           36:["to freeze","froze","frozen"],
           37:["to get","got","got"],
           38:["to give","gave","given"],
           39:["to go","went","gone"],
           40:["to grow","grew","grown"],
           41:["to hang","hung","hung"],
           42:["to have","had","had"],
           43:["to hear","heard","heard"],
           44:["to hide","hid","hidden"],
           45:["to hit","hit","hit"],
           46:["to hold","held","held"],
           47:["to hurt","hurt","hurt"],
           48:["to keep","kept","kept"],
           49:["to know","knew","known"],
           50:["to lay","laid","laid"],
           51:["to lead","led","led"],
           52:["to learn","learnt","learnt"],
           53:["to leave","left","left"],
           54:["to let","let","let"],
           55:["to lie","lay","lain"],
           56:["to light","lit","lit"],
           57:["to lose","lost","lost"],
           58:["to make","made","made"],
           59:["to mean","meant","meant"],
           60:["to meet","met","met"],
           61:["to mistake","mistook","mistaken"],
           62:["to pay","paid","paid"],
           63:["to put","put","put"],
           64:["to quit","quit","quit"],
           65:["to read","read","read"],
           66:["to ride","rode","riden"],
           67:["to ring","rang","rung"],
           68:["to rise","rose","risen"],
           69:["to run","ran","run"],
           70:["to say","said","said"],
           71:["to see","saw","seen"],
           72:["to seek","sought","sought"],
           73:["to sell","sold","sold"],
           74:["to send","sent","sent"],
           75:["to set","set","set"],
           76:["to shake","shook","shaken"],
           77:["to shine","shone","shone"],
           78:["to shoot","shot","shot"],
           79:["to show","showed","shown"],
           80:["to sing","sang","sung"],
           81:["to sink","sank","sunk"],
           82:["to sit","sat","sat"],
           83:["to sleep","slept","slept"],
           84:["to speak","spoke","spoken"],
           85:["to spell","spelt","spelt"],
           86:["to spend","spent","spent"],
           87:["to stand","stood","stood"],
           88:["to steal","stole","stolen"],
           89:["to swim","swam","swum"],
           90:["to take","took","taken"],
           91:["to teach","taught","taught"],
           92:["to tear","tore","torn"],
           93:["to tell","told","told"],
           94:["to think","thought","thought"],
           95:["to throw","threw","thrown"],
           96:["to understand","understood","understood"],
           97:["to wake","woke","woken"],
           98:["to wear","wore","worn"],
           99:["to win","won","won"],
           100:["to write","wrote","written"]}
  return irr_verbs.pop(random.randint(2,100))


@dp.message_handler(commands = 'start', state='*')
async def start_cmd_handler(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard_markup = types.InlineKeyboardMarkup (
        inline_keyboard=[[types.InlineKeyboardMarkup(text='Sure!', callback_data='lets_play')]]
    )
    reply = 'Hi! Wanna play with irregular verbs?'
    await message.answer(text=reply, reply_markup=keyboard_markup)

@dp.callback_query_handler(text='lets_play')
async def users_help(call: types.CallbackQuery, state: FSMContext):
    await LetsPlay.FirstForm.set()
    chosen_verb = await irr_verbs_training()
    first_form = chosen_verb[0]
    second_form = chosen_verb[1]
    await state.update_data(first_form=first_form, second_form=second_form)
    reply = f"Dear User, what's the past form of the verb «{first_form}» ?"
    await call.message.answer(text=reply)

@dp.message_handler(state=LetsPlay.FirstForm)
async def users_help(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    first_form = data['first_form']
    second_form = data['second_form']
    if answer == second_form:
        await state.finish()
        keyboard_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text='More!', callback_data='lets_play')]]
        )
        reply = f"You're awesome! The past form of the verb «{first_form}» is «{second_form}»! Want more?"
        await message.answer(text=reply, reply_markup=keyboard_markup)
    else:
        reply = f"Not quite! Try again!"
        await message.answer(text=reply)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

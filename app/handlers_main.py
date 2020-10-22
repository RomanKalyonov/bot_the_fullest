from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from functions import irr_verbs_training
from load_all import dp
from states import LetsPlay


@dp.message_handler(CommandStart(), state='*')  # ловим команду старт /start из любого состояния
async def start_cmd_handler(message: Message, state: FSMContext):
    # Cancel any state
    await state.finish()
    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Let`s play!', callback_data='lets_play')]]
    )
    reply = 'Hi! Press button Let`s play'
    await message.answer(text=reply, reply_markup=keyboard_markup)


# ловим хэндлер с коллбэкдатой let`s play
@dp.callback_query_handler(text='lets_play')
async def users_help(call: CallbackQuery, state: FSMContext):
    await LetsPlay.FirstForm.set()  # вводим пользователя в состояние
    chosen_verb = await irr_verbs_training()  # получаем список глаголов
    first_form = chosen_verb[1]
    second_form = chosen_verb[2]
    await state.update_data(first_form=first_form, second_form=second_form)  # сохраняем данные в состояние
    reply = f"Dear User, what's the past form of the verb {first_form} ?"
    await call.message.answer(text=reply)


# ловим любое сообщение в состояние LetsPlay.FirstForm
@dp.message_handler(state=LetsPlay.FirstForm)
async def users_help(message: Message, state: FSMContext):
    answer = message.text  # получаем ответ
    data = await state.get_data()  # загружаем данные из состояния
    first_form = data['first_form']
    second_form = data['second_form']
    if answer == second_form:
        await state.finish()  # выходим из состояние
        keyboard_markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Let`s play again!', callback_data='lets_play')]]
        )
        reply = f"Cool! You are right! The past form of the verb {first_form} is {second_form}! Let`s play again?"
        await message.answer(text=reply, reply_markup=keyboard_markup)
    else:
        # а здесь, поскольку мы всё ещё в состояние LetsPlay.FirstForm, просим ввести сообщение повторно,
        # тогда снова его поймаем этим хэндлером.
        reply = f"Not quite! Try again!"
        await message.answer(text=reply)

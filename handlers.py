from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import *

import keyboards
from gpt import ChatGptServices
from util import load_prompt, load_message, send_answer

router = Router()
chat_gpt = ChatGptServices()


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    """
    Обработчик команды /start отправляет список команд сообщением
    """
    await state.clear()

    image = FSInputFile("resources/images/main.jpg")
    message = load_message('main')

    await msg.answer_photo(photo=image, caption=message)


@router.message(Command('random'))
async def random(msg: Message, state: FSMContext):
    """
    Обработчик команды /random отправляет случайный факт сообщением
    """
    await state.clear()

    image = FSInputFile("resources/images/random.jpg")

    await msg.answer_photo(photo=image)
    message = await msg.answer('ChatGPT думает...')

    prompt = load_prompt('random')

    chat_gpt.set_prompt(prompt)

    answer = await chat_gpt.add_message(msg.text)
    await message.edit_text(answer)

@router.message(Command('gpt'))
async def gpt(msg: Message, state: FSMContext):
    """
    Обработчик команды /gpt переводит бот в режим свободного общения с chatGPT

    """
    await state.clear()

    await state.set_state(GptState.gpt)

    image = FSInputFile("resources/images/gpt.jpg")
    prompt = load_prompt('gpt')
    message = load_message('gpt')

    chat_gpt.set_prompt(prompt)
    await msg.answer_photo(photo=image, caption=message, reply_markup=keyboards.inline_exit_button)



@router.callback_query(F.data == 'exit_gpt')
async def exit_gpt(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки выхода из режимов общения с chatGPT
    """
    await state.clear()
    await start(callback.message, state)


@router.message(Command('talk'))
async def talk(msg: Message,  state: FSMContext):
    """
    Обработчик команды /talk возвращает список известных личностей
    """
    await state.clear()
    await msg.answer('Выберите известную личность', reply_markup=keyboards.inline_famous_person_button)



@router.callback_query(F.data.startswith('talk_'))
async def talk(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки выбора известной личности.
    Переводит бот в режим общения с известной личностью в chatGPT
    """

    await state.set_state(GptState.talk)

    prompt = load_prompt(callback.data)
    image = FSInputFile(f"resources/images/{callback.data}.jpg")

    chat_gpt.set_prompt(prompt)
    person = {
        'talk_cobain': 'Курт Кобейн - Солист группы Nirvana 🎸',
        'talk_queen': 'Елизавета II - Королева Соединённого Королевства 👑',
        'talk_tolkien': 'Джон Толкиен - Автор книги "Властелин Колец" 📖',
        'talk_nietzsche': 'Фридрих Ницше - Философ 🧠',
        'talk_hawking': 'Стивен Хокинг - Физик 🔬',
    }

    message = person[callback.data]
    GptState.person = message[:message.find("-")-1]
    await callback.message.answer_photo(photo=image, caption=message, reply_markup=keyboards.inline_exit_button)


@router.message(Command('quiz'))
async def quiz(msg: Message, state: FSMContext):
    """
    Обработчик команды /quiz переводит бот в режим викторины с chatGPT
    """
    await state.clear()
    await state.set_state(GptState.question)
    prompt = load_prompt('quiz')
    image = FSInputFile(f"resources/images/quiz.jpg")
    message = load_message('quiz')

    chat_gpt.set_prompt(prompt)

    await msg.answer_photo(photo=image, caption=message, reply_markup=keyboards.reply_quiz_button)


@router.message(GptState.question)
async def quiz(msg: Message, state: FSMContext):
    theme = {
        'программирования на языке python': 'quiz_prog',
        'теорий алгоритмов, теории множеств и матанализа': 'quiz_math',
        'биология': 'quiz_biology',
        'вопрос на ту же тему': 'quiz_more',
    }
    if msg.text in theme:
        message = await msg.answer('ChatGPT придумывает вопрос...')
        answer = await chat_gpt.add_message(theme[msg.text])
        await state.clear()
        await state.set_state(GptState.result)
        await message.edit_text(answer, reply_markup=keyboards.inline_exit_button)
    else:
        answer = 'Выберите тему'
        await msg.answer(answer, reply_markup=keyboards.inline_exit_button)

@router.message(Command('translator'))
async def translator(msg: Message, state: FSMContext):
    """
    Обработчик команды /translator переводит бот в режим переводчика с chatGPT
    """
    await state.clear()
    await state.set_state(GptState.translator)
    prompt = load_prompt('translator')
    image = FSInputFile(f"resources/images/translator.jpg")
    chat_gpt.set_prompt(prompt)

    await msg.answer_photo(photo=image, caption="Введите язык на который хотите переводить")


@router.message(Command('idea'))
async def idea(msg: Message, state: FSMContext):
    """
    Обработчик команды /idea переводит бот в режим генератора идей с chatGPT
    """
    await state.clear()
    await state.set_state(GptState.idea)
    prompt = load_prompt('idea')
    image = FSInputFile(f"resources/images/idea.jpg")

    chat_gpt.set_prompt(prompt)

    await msg.answer_photo(photo=image, caption='Введите тему чтобы получить список идей')


@router.message(StateFilter(GptState.gpt, GptState.talk, GptState.result, GptState.translator, GptState.idea))
async def gpt_answer(msg: Message, state: FSMContext):
    cur_state = await state.get_state()

    match cur_state:
        case GptState.gpt | GptState.translator | GptState.idea:
            message = await msg.answer('ChatGPT думает...')
            await send_answer(msg, message, chat_gpt)
        case GptState.talk:
            message = await msg.answer(f'{GptState.person} отвечает...')
            await send_answer(msg, message, chat_gpt)
        case GptState.result:
            message = await msg.answer('ChatGPT проверяет ответ...')
            await state.clear()
            await state.set_state(GptState.question)
            await send_answer(msg, message, chat_gpt)





@router.message()
async def echo(msg: Message):
    """
    Эхо
    """
    await msg.answer(msg.text)

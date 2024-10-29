
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


import keyboards
from gpt import ChatGptServices
from util import load_prompt, load_message

router = Router()
chat_gpt = ChatGptServices()

#машины состояний
class GptState(StatesGroup):
    active = State()


class TalkState(StatesGroup):
    active = State()


class QuizState(StatesGroup):
    active = State()


class TranslatorState(StatesGroup):
    active = State()

class IdeaState(StatesGroup):
    active = State()


@router.message(CommandStart())
async def start(msg: Message):
    """
    Обработчик команды /start отправляет список команд сообщением
    """
    image = FSInputFile("resources/images/main.jpg")
    message = load_message('main')
    await msg.answer_photo(photo=image, caption=message)



@router.message(Command('random'))
async def random(msg: Message):
    """
    Обработчик команды /random отправляет случайный факт сообщением
    """
    image = FSInputFile("resources/images/random.jpg")

    await msg.answer_photo(photo=image)
    message = await msg.answer('чат gpt думает...')

    prompt = load_prompt('random')
    answer = await chat_gpt.send_question(prompt, '')
    await message.edit_text(answer)



@router.message(Command('gpt'))
async def gpt(msg: Message, state: FSMContext):
    """
    Обработчик команды /gpt переводит бот в режим свободного общения с chatGPT
    """
    await state.set_state(GptState.active)

    image = FSInputFile("resources/images/gpt.jpg")
    prompt = load_prompt('gpt')
    message = load_message('gpt')

    chat_gpt.set_prompt(prompt)
    await msg.answer_photo(photo=image, caption=message, reply_markup=keyboards.inline_exit_button)


@router.callback_query(F.data=='exit_gpt')
async def exit_gpt(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки выхода из режимов общения с chatGPT
    """
    await state.clear()
    await start(callback.message)


@router.message(Command('talk'))
async def talk(msg: Message):
    """
    Обработчик команды /talk возвращает список известных личностей
    """
    await msg.answer('Выберите известную личность', reply_markup=keyboards.inline_famous_person_button)



@router.callback_query(F.data.startswith('talk_'))
async def talk(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки выбора известной личности.
    Переводит бот в режим общения с известной личностью в chatGPT
    """

    await state.set_state(TalkState.active)

    prompt = load_prompt(callback.data)
    image = FSInputFile(f"resources/images/{callback.data}.jpg")

    chat_gpt.set_prompt(prompt)
    if callback.data == 'talk_cobain':
        message = 'Курт Кобейн - Солист группы Nirvana 🎸'
    elif callback.data == 'talk_queen':
        message = 'Елизавета II - Королева Соединённого Королевства 👑'
    elif callback.data == 'talk_tolkien':
        message = 'Джон Толкиен - Автор книги "Властелин Колец" 📖'
    elif callback.data == 'talk_nietzsche':
        message = 'Фридрих Ницше - Философ 🧠'
    elif callback.data == 'talk_hawking':
        message = 'Стивен Хокинг - Физик 🔬'

    await callback.message.answer_photo(photo=image, caption=message, reply_markup=keyboards.inline_exit_button)



@router.message(Command('quiz'))
async def quiz(msg: Message, state: FSMContext):
    """
    Обработчик команды /quiz переводит бот в режим викторины с chatGPT
    """
    await state.set_state(QuizState.active)
    prompt = load_prompt('quiz')
    image = FSInputFile(f"resources/images/quiz.jpg")
    message = load_message('quiz')

    chat_gpt.set_prompt(prompt)

    await msg.answer_photo(photo=image, caption=message, reply_markup=keyboards.inline_quiz_button)


@router.message(Command('translator'))
async def translator(msg: Message, state: FSMContext):
    """
    Обработчик команды /translator переводит бот в режим переводчика с chatGPT
    """
    await state.set_state(TranslatorState.active)
    prompt = load_prompt('translator')
    image = FSInputFile(f"resources/images/translator.jpg")
    chat_gpt.set_prompt(prompt)

    await msg.answer_photo(photo=image, caption="Введите текс для перевода и укажите язык для перевода\n"
                                                "(по умолчанию Английский/Русский)")


@router.message(Command('idea'))
async def idea(msg: Message, state: FSMContext):
    """
    Обработчик команды /idea переводит бот в режим генератора идей с chatGPT
    """
    await state.set_state(IdeaState.active)
    prompt = load_prompt('idea')
    image = FSInputFile(f"resources/images/idea.jpg")
    chat_gpt.set_prompt(prompt)

    await msg.answer_photo(photo=image, caption='Задайте тему или область интересов')

@router.message()
async def text_handler(msg: Message, state: FSMContext):
    """
    Обработчик текстовых сообщений по состоя́нию.
    """
    if await state.get_state() == GptState.active:
        answer = await chat_gpt.add_message(msg.text)
        await msg.answer(answer, reply_markup=keyboards.inline_exit_button)

    elif await state.get_state() == TalkState.active:
        answer = await chat_gpt.add_message(msg.text)
        await msg.answer(answer, reply_markup=keyboards.inline_exit_button)

    elif await state.get_state() == QuizState.active:
        if msg.text == 'программирования на языке python':
            answer = await chat_gpt.add_message('quiz_prog')
        elif msg.text == 'теорий алгоритмов, теории множеств и матанализа':
            answer = await chat_gpt.add_message('quiz_math')
        elif msg.text == 'биология':
            answer = await chat_gpt.add_message('quiz_biology')
        elif msg.text == 'вопрос на ту же тему':
            answer = await chat_gpt.add_message('quiz_more')
        else:
            answer = await chat_gpt.add_message(msg.text)

        await msg.answer(answer, reply_markup=keyboards.inline_exit_button)

    elif await state.get_state() == TranslatorState.active:
        answer = await chat_gpt.add_message(msg.text)
        await msg.answer(answer, reply_markup=keyboards.inline_exit_button)

    elif await state.get_state() == IdeaState.active:
        answer = await chat_gpt.add_message(msg.text)
        await msg.answer(answer, reply_markup=keyboards.inline_exit_button)
    else:
        await msg.answer(msg.text)
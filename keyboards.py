from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


inline_famous_person_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Курт Кобейн - Солист группы Nirvana 🎸', callback_data='talk_cobain')],
    [InlineKeyboardButton(text='Елизавета II - Королева Соединённого Королевства 👑', callback_data='talk_queen')],
    [InlineKeyboardButton(text='Джон Толкиен - Автор книги "Властелин Колец" 📖', callback_data='talk_tolkien')],
    [InlineKeyboardButton(text='Фридрих Ницше - Философ 🧠', callback_data='talk_nietzsche')],
    [InlineKeyboardButton(text='Стивен Хокинг - Физик 🔬', callback_data='talk_hawking')],
],
)

reply_quiz_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='программирования на языке python')],
    [KeyboardButton(text='теорий алгоритмов, теории множеств и матанализа')],
    [KeyboardButton(text='биология')],
    [KeyboardButton(text='вопрос на ту же тему')],
],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

inline_exit_button =InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text='закончить', callback_data='exit_gpt')]
    ]

)

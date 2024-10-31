import keyboards
from aiogram.types import Message


def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


def load_message(name):
    with open("resources/messages/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()

async def send_answer(msg: Message, message, chat_gpt):
    answer = await chat_gpt.add_message(msg.text)
    await message.edit_text(answer, reply_markup=keyboards.inline_exit_button)

    # await msg.answer(answer, reply_markup=keyboards.inline_exit_button)
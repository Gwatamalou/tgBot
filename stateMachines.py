from aiogram.fsm.state import StatesGroup, State

#машины состояний
class GptState(StatesGroup):
    active = State()


class TalkState(StatesGroup):
    active = State()
    person = str


class QuizState(StatesGroup):
    question = State()
    result = State()


class TranslatorState(StatesGroup):
    active = State()


class IdeaState(StatesGroup):
    active = State()

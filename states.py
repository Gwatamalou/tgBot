from aiogram.fsm.state import StatesGroup, State

#машины состояний
class GptState(StatesGroup):
    """
    Машины состояний для взаимодействия с ChatGPT
    """

    active = State()

    #свободное общение
    gpt = State()


    #общения с известной личностью
    talk = State()
    person = str

    #викторина
    question = State()
    result = State()

    #переводчик
    translator = State()

    #генератор идей
    idea = State()


# class TalkState(StatesGroup):
#     active = State()
#     person = str

#
# class QuizState(StatesGroup):
#     question = State()
#     result = State()


# class TranslatorState(StatesGroup):
#     active = State()
#

# class IdeaState(StatesGroup):
#     active = State()
